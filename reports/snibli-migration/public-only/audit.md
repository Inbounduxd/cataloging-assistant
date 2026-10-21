# SNIBLI migration audit

2026-10-21T03:32:24.906185+00:00

Coverage: LOCAL_AND_PUBLIC_PARTIAL

PASS applies only to the named check, never to full migration equivalence.

- **PASS** `release_v3.9.2_integrity`: {"sha256": "b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede", "bytes": 118470, "files": 86, "json_files": 36}
- **PASS** `local_master_contract`: {"bindings": 56, "unique_metadata_keys": 54, "contract_version": "dspace-cataloger-v3.9.1"}
- **PASS** `local_governance`: {"draftable_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "controlled_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "profile_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "profile_relationships": [["dc.subject.linguisticFamily", "dc.subject.linguiscgroup"], ["dc.subject.linguiscgroup", "dc.subject.linguisticVariant"], ["dc.subject.linguisticFamily", "dc.subject.linguisticBranch"], ["dc.subject.linguisticBranch", "dc.subject.linguiscgroup"]], "clin_relationships": [["dc.subject.linguisticFamily", "dc.subject.linguiscgroup"], ["dc.subject.linguiscgroup", "dc.subject.linguisticVariant"]], "branch_is_optional_enrichment": true, "registered_language_is_independent": true, "dspace_write_enabled": false, "human_approval_required": true}
- **PASS** `local_language_separation`: "Local contract only; no live semantic equivalence asserted"
- **NOT_TESTED** `api_hal`: "API base not supplied; no route inferred"
- **PASS** `public_url`: "Public HTTP reachability only"
- **UNKNOWN** `instance_identity`: "UUID/handle alone cannot prove database identity"
- **NOT_TESTED** `vertical_022_comparison`: "Supply --baseline and --observed raw exports; no database job executed"
- **NOT_TESTED** `live_56_bindings_54_keys`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_form_order_labels_controls`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_vocabulary_values`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_language_rules`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `golden_GR01_GR23`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"

## Warnings

- No full migration equivalence established.
- Executable contract declares dspace-cataloger-v3.9.1; current preserved release is v3.9.2. Review version alignment separately.

## Configuration, endpoints and errors

```json
{
  "configuration": {
    "public_url": "https://www.iifl.unam.mx/SNIBLI/home",
    "api_base": null,
    "timeout": 5.0,
    "offline": false,
    "credentials_used": false,
    "max_response_bytes": 4194304,
    "max_requests_per_endpoint": 4,
    "baseline_supplied": false,
    "observed_supplied": false
  },
  "endpoints": [
    {
      "endpoint": "https://www.iifl.unam.mx/SNIBLI/home",
      "redirects": [
        {
          "url": "https://www.iifl.unam.mx/SNIBLI/home",
          "status": 200
        }
      ],
      "http_status": 200,
      "content_type": "text/html; charset=utf-8",
      "body_sha256": "50f06e29dcdfacb388dd744bc904911c0457316be2d8843fdc51b92b88173e0c"
    }
  ],
  "errors": []
}
```
