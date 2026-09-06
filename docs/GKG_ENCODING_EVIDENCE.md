# GKG encoding evidence: facts, observations, policy and unknowns

## Provider documentation (retrieved 2026-09-05 UTC)

The [GKG 2.1 codebook, 2015-02-19](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)
describes a tab-delimited record per line (page 1), and the final V2EXTRASXML field
as customizable XML (page 15). Its old description of that field predates later
news metadata additions. No UTF/ASCII character-encoding declaration was located
in the searchable text of this codebook. This is a bounded search finding, not
proof that no GDELT document anywhere defines an encoding.

The [2016-04-22 article metadata announcement](https://blog.gdeltproject.org/new-gkg-2-0-article-metadata-fields/)
places extracted metadata in the last XMLExtras column, including PAGE_ALTURL_AMP.
It says non-ASCII author names use HTML UTF8 escaping; that statement is specific
to author metadata and is not a whole-file encoding guarantee or an AMP URL codec
specification. Exact PDF/HTML snapshots are local; hashes, URLs and retrieval
clocks are committed in the Phase 3 source-documents.json evidence.

Provider-domain searches for GKG UTF-8, invalid encoding and character encoding
also returned documentation about Visual GKG, Global Frontpage Graph and Global
Embedded Metadata Graph. Those are different products; their UTF-8/escaping or
repair policies are not attributed to the sampled GKG 2.1 feed. No authoritative
explanation of these five particular malformed rows was located. No alternative
codec has been established or used for acceptance.

## Empirical observations

The five known malformed rows were independently found from the original corpus.
They contain single-byte f1 (two rows), e4 (one), and a0 (two), rejected by strict
UTF-8. All five lie within field 27 PAGE_ALTURL_AMP blocks. This identifies where
the bytes occur, not their intended characters, upstream encoding, or cause.
Similar-looking URL text is insufficient evidence to choose a codec. Raw row
SHA-256, archive SHA-256, member, line, byte range and invalid spans are preserved
in quarantine.json; base64 reconstructs the complete original row exactly.

## Engineering policy

Accept only strict UTF-8 rows satisfying the versioned structural/timestamp/ID
policy, retaining opaque fields without interpreting their semantics. Quarantine
an entire undecodable row, including valid-looking prefix fields. Do not remove
field 27 or repair a URL to salvage that row. Other independently valid rows in a
fully verified, completely accounted batch may remain syntactically eligible.
The codebook does not validate Psychohistory theme semantics or indicator use.

## Unresolved factual questions

The provider's intended whole-file character set; whether AMP metadata can retain
upstream bytes; whether these files have been corrected remotely; frequency in
other periods/languages; and any provider guarantee about malformed data remain
unknown. These unknowns are contained by exact quarantine, not declared solved.
