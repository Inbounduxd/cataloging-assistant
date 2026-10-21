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

Human authorization covers preparing rc.2 with this captured evidence, not adopting,
publishing, installing or deploying it. No DSpace writes, automatic inference, agent
mutation, baseline promotion or synchronization are enabled. The application runtime
payload/hash remains unchanged from rc.1, as do the 57 bindings and 55 metadata keys.
Golden Set GR01–GR23 remains byte-for-byte unchanged; no new adjudication is claimed.

Direct binary parent: local v3.9.3-rc.1, verified checksum recorded in the manifests.
The adopted repository pointer still identifies preserved v3.9.2. Without a commit,
rc.2 is a local candidate and must not be described as preserved on GitHub.
