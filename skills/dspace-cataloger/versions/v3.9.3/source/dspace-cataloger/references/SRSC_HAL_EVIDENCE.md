# srsc HAL evidence in v3.9.3-rc.2

The public GET-only traversal captured the hierarchy currently exposed by SNIBLI:
665 nodes, 653 parent-child relations, 12 roots, 126 raw HAL responses, no login.
assets/srsc-tree.json retains literal IDs, labels, values, selectable flags and edges.
The vocabulary index exposes selectable values only; never infer selection permission
from being a parent or leaf. Retain non-selectable nodes as hierarchy context.

Original HAL bodies and export envelope are in evidence/srsc/. Their hashes, pagination
and reconstruction have been checked against the normalized tree. This is not an
atomic database snapshot or proof of nodes the API does not expose. Validate current
vocabulary availability before any future human-controlled copy to DSpace.

The prior UNKNOWN for the current reachable tree is resolved. Historical equivalence
remains UNKNOWN because the preserved historical release lacks the full tree. Active
sections HAL remains UNKNOWN_HTTP_204; full migration equivalence remains UNKNOWN.
This evidence supersedes rc.1's current-tree gap but does not rewrite rc.1 itself.

This evidence was first packaged in rc.2, preserved by merged PR #87.
Its original bodies, normalized tree and verified facts remain byte-identical.
Stable preparation and repository adoption are described in STABLE_RELEASE_3.9.3.md.
