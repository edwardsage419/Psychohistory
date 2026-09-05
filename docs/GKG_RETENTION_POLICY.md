# Evidence retention and near-zero-cost compatibility

This is a design, not a deletion implementation. It applies project-wide; the
96-batch Phase 2/3 research corpus is an explicit permanent research fixture
exception and remains intact locally. No acquisition frequency, fields or
historical sampling are reduced. GKG candidate gates are unchanged.

| Class | Retain | Phase 3 representation |
| --- | --- | --- |
| Irreplaceable evidence | Permanently, with backups | Exact quarantine row bytes in base64, locators, source/member/row hashes, reasons, parser and contract versions; exact manifest; acquisition receipts; code and schema revisions; replay and promotion decisions; documentation references |
| Derived data | Normally retain | Accepted-row provenance/field-vector hashes and batch quality ledgers; future normalized records in local files or a lightweight analytical store |
| Public raw artifacts | Configurable only in a future policy | ZIP revision keyed by SHA-256, source URL, source batch time, acquisition clocks, transport headers/status/size, member hash and parser/schema revision |

Public accessibility does not guarantee replaceability. Ordinary future raw ZIPs
may be eligible for expiration only under a separately evaluated policy. URLs
may disappear or return changed bytes. A retained hash proves identity if matching
bytes are recovered; it cannot reconstruct bytes or guarantee full future replay.
If raw is unavailable, mark full accepted-row replay unavailable, never passed.
Quarantine byte-level reinspection still works without the ZIP because complete
raw rows are embedded. Verifying their original membership again requires the
archive; the retained acquisition/row locator evidence documents that prior check.
Accepted field hashes alone cannot reconstruct accepted field values. A future
retention policy must preserve actual normalized field values if later analytical
use requires them; Phase 3 creates no normalized observation database.

The committed Phase 2 study records all acquisition timestamps, HTTP metadata,
source references and hashes. Phase 3 publishes a compact provenance receipt set
bound to that report hash; quarantine source identity joins by batch ID and archive
SHA-256. Runtime clocks are retained in receipts and run metadata, outside semantic
comparison; parser/schema versions and code fingerprints remain stable evidence.

Raw ZIPs and full accepted-row ledgers remain local because storing every raw or
large generated ledger in Git history scales poorly. Compact receipts, quarantines,
results, manifests and code are suitable for Git review. No hosted database,
object storage, paid compute or API is introduced. SQLite/DuckDB/Parquet and free
Actions remain compatible future options, without promising free-tier capacity.

The final storage evidence separates compressed raw archives, quarantine evidence,
derived accepted-row ledgers (not normalized field values), and manifests/provenance.
Any daily/30-day/yearly scenario uses measured recent-batch mean times 96/2880/35040;
these are biased 18-hour sample extrapolations, not quotas or full-year measurements.
Quarantine incidence and row sizes may change. Normalized record storage remains
unknown until a concrete full-field layout is measured. Backups, Git history,
replication and future index overhead are additional costs, not hidden in estimates.

No cleanup code exists in Phase 3. Preserve both replay directories, all raw inputs
and original Phase 2 evidence. Local disk failure remains a risk; a backup target
has not been configured or purchased. Near-zero recurring service cost does not
mean zero local disk, electricity, bandwidth or maintenance cost.
