"""Phase 6A pinned-address HTTP transport. No proxy, cookies or credentials."""
from datetime import datetime,timezone
import http.client
import socket
import ssl
import time
from urllib.parse import urlsplit,urljoin
import gkg_semantics as s
from retrieve_gkg_semantics import check_public,verify_public_peer

class PinnedConnection(http.client.HTTPConnection):
    def __init__(self,host,port,addresses,timeout,tls):
        super().__init__(host,port,timeout=timeout);self.addresses=addresses;self.tls=tls;self.peer=None
    def connect(self):
        # Numeric literal only: no second hostname resolution between approval and connect.
        address=sorted(self.addresses)[0]
        self.sock=socket.create_connection((address,self.port),timeout=self.timeout)
        try:
            self.peer=verify_public_peer(self.sock,self.addresses)
            if self.tls:
                self.sock=ssl.create_default_context().wrap_socket(self.sock,server_hostname=self.host)
                verify_public_peer(self.sock,self.addresses)
        except Exception:
            self.close();raise

def fetch(url,cfg):
    started=time.monotonic();deadline=started+cfg['request_deadline_seconds'];hops=[];current=url
    result={'requested_url':url,'final_url':None,'retrieved_at':datetime.now(timezone.utc).isoformat(),
        'status':None,'failure':None,'hops':hops,'bytes':0,'content_sha256':None,'content_type':None,'charset':'utf-8'}
    blob=None
    try:
        for hop in range(cfg['max_redirects']+1):
            approved=check_public(current);u=urlsplit(current)
            remaining=deadline-time.monotonic();s.require(remaining>0,'deadline')
            conn=PinnedConnection(u.hostname,u.port or (443 if u.scheme=='https' else 80),approved,min(cfg['socket_timeout_seconds'],remaining),u.scheme=='https')
            try:
                conn.connect() # peer validation occurs before request bytes are sent
                conn.request('GET',(u.path or '/')+('?' +u.query if u.query else ''),headers={'User-Agent':'Psychohistory-research/0.6','Accept-Encoding':'identity','Connection':'close'})
                response=conn.getresponse()
                hops.append({'url':current,'status':response.status,'approved_ips':sorted(approved),'peer_ip':conn.peer})
                result.update(final_url=current,status=response.status,content_type=response.headers.get_content_type(),charset=response.headers.get_content_charset() or 'utf-8')
                if response.status in (301,302,303,307,308):
                    location=response.getheader('Location');s.require(location and hop<cfg['max_redirects'],'redirect_limit_or_missing_location')
                    current=urljoin(current,location);continue
                s.require(response.status==200,'http_'+str(response.status))
                chunks=[];n=0
                while True:
                    remaining=deadline-time.monotonic();s.require(remaining>0,'deadline')
                    # HTTPConnection may detach its socket on Connection: close; raw stream still owns it.
                    sock=getattr(getattr(response.fp,'raw',None),'_sock',None)
                    if sock:sock.settimeout(min(cfg['socket_timeout_seconds'],remaining))
                    chunk=response.read1(min(65536,cfg['max_bytes']+1-n))
                    if not chunk:break
                    chunks.append(chunk);n+=len(chunk);s.require(n<=cfg['max_bytes'],'response_size_limit')
                blob=b''.join(chunks);result.update(bytes=len(blob),content_sha256=s.sha(blob))
                return result,blob
            finally:conn.close()
    except (OSError,http.client.HTTPException,s.Invalid,ValueError) as exc:
        result['failure']=str(exc) if isinstance(exc,s.Invalid) else type(exc).__name__
    finally:result['duration_seconds']=round(time.monotonic()-started,6)
    return result,None
