# SNIBLI migration audit

2026-10-21T04:48:39.869284+00:00

Coverage: PUBLIC_REST_AND_REGISTRY_PARTIAL

PASS applies only to the named check, never to full migration equivalence.

- **PASS** `release_v3.9.2_integrity`: {"sha256": "b6c435a28f8bb1a8faab237258161edf0233b2ce3608ff4e025a8ae2a11acede", "bytes": 118470, "files": 86, "json_files": 36}
- **PASS** `local_master_contract`: {"bindings": 56, "unique_metadata_keys": 54, "contract_version": "dspace-cataloger-v3.9.1"}
- **PASS** `local_governance`: {"draftable_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "controlled_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "profile_fields": ["dc.description.registeredLanguage", "dc.subject.linguiscgroup", "dc.subject.linguisticFamily", "dc.subject.linguisticBranch", "dc.subject.linguisticVariant"], "profile_relationships": [["dc.subject.linguisticFamily", "dc.subject.linguiscgroup"], ["dc.subject.linguiscgroup", "dc.subject.linguisticVariant"], ["dc.subject.linguisticFamily", "dc.subject.linguisticBranch"], ["dc.subject.linguisticBranch", "dc.subject.linguiscgroup"]], "clin_relationships": [["dc.subject.linguisticFamily", "dc.subject.linguiscgroup"], ["dc.subject.linguiscgroup", "dc.subject.linguisticVariant"]], "branch_is_optional_enrichment": true, "registered_language_is_independent": true, "dspace_write_enabled": false, "human_approval_required": true}
- **PASS** `local_language_separation`: "Local contract only; no live semantic equivalence asserted"
- **PASS** `public_url`: "Public HTTP reachability only"
- **PASS** `api_hal`: "HAL_RESPONSE_OBSERVED"
- **FAIL** `pilot_collection`: "HTTP_404"
- **UNKNOWN** `instance_identity`: "UUID/handle alone cannot prove database identity"
- **NOT_TESTED** `vertical_022_comparison`: "Supply --baseline and --observed raw exports; no database job executed"
- **NOT_TESTED** `live_56_bindings_54_keys`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_form_order_labels_controls`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_vocabulary_values`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `live_language_rules`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **NOT_TESTED** `golden_GR01_GR23`: "Requires dedicated contract/semantic evidence; public HAL is insufficient"
- **PASS** `public_registry_54_keys`: {"scope": "Presence, IDs, element/qualifier and scope notes against preserved v3.9.2 profile only", "counts": {"schemas": 18, "metadata_fields": 293, "collections": 455, "expected_contract_keys": 54, "present_contract_keys": 54, "exact_registry_matches": 54}, "captured_at": "2026-10-21T05:17:29.102474+00:00", "evidence": "public-registry/inventory.json", "diff": "public-registry/diff.json", "full_contract_comparison": false}
- **FAIL** `historical_pilot_in_public_inventory`: {"public_collections_observed": 455, "matches_by_uuid_or_handle": [], "interpretation": "No public match for historical UUID or Handle; deletion is not established", "evidence": "public-registry/inventory.json"}

## Warnings

- No full migration equivalence established.
- Executable contract declares dspace-cataloger-v3.9.1; current preserved release is v3.9.2. Review version alignment separately.
- Public registry comparison covers 54 keys against the preserved release, not the ACTIVE runtime snapshot.
- 18 schemas and 293 metadata fields were fully paginated; the historical 292-field global raw baseline is unavailable.
- No historical pilot UUID or Handle match among 455 public collections; an authorized operator must confirm collection identity.

## Configuration, endpoints and errors

```json
{
  "configuration": {
    "public_url": "https://www.iifl.unam.mx/SNIBLI/home",
    "api_base": "https://www.iifl.unam.mx/server/api",
    "timeout": 10.0,
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
    },
    {
      "endpoint": "https://www.iifl.unam.mx/server/api",
      "redirects": [
        {
          "url": "https://www.iifl.unam.mx/server/api",
          "status": 200
        }
      ],
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "body_sha256": "13dd53629e044cf3837a06150e592b6665d405d0694293e4d6965a5c695a2094",
      "raw_hal": {
        "dspaceUI": "https://www.iifl.unam.mx/SNIBLI",
        "dspaceName": "Respositorio Ind",
        "dspaceServer": "https://www.iifl.unam.mx/server",
        "dspaceVersion": "DSpace 7.6.6",
        "type": "root",
        "_links": {
          "actuator": {
            "href": "https://www.iifl.unam.mx/server/actuator"
          },
          "authn": {
            "href": "https://www.iifl.unam.mx/server/api/authn"
          },
          "authorizations": {
            "href": "https://www.iifl.unam.mx/server/api/authz/authorizations"
          },
          "bitstreamformats": {
            "href": "https://www.iifl.unam.mx/server/api/core/bitstreamformats"
          },
          "bitstreams": {
            "href": "https://www.iifl.unam.mx/server/api/core/bitstreams"
          },
          "browses": {
            "href": "https://www.iifl.unam.mx/server/api/discover/browses"
          },
          "bulkaccessconditionoptions": {
            "href": "https://www.iifl.unam.mx/server/api/config/bulkaccessconditionoptions"
          },
          "bundles": {
            "href": "https://www.iifl.unam.mx/server/api/core/bundles"
          },
          "claimedtasks": {
            "href": "https://www.iifl.unam.mx/server/api/workflow/claimedtasks"
          },
          "claimedtasks-search": {
            "href": "https://www.iifl.unam.mx/server/api/workflow/claimedtasks/search"
          },
          "collections": {
            "href": "https://www.iifl.unam.mx/server/api/core/collections"
          },
          "communities": {
            "href": "https://www.iifl.unam.mx/server/api/core/communities"
          },
          "discover": {
            "href": "https://www.iifl.unam.mx/server/api/discover"
          },
          "dso": {
            "href": "https://www.iifl.unam.mx/server/api/dso/find{?uuid}",
            "templated": true
          },
          "entitytypes": {
            "href": "https://www.iifl.unam.mx/server/api/core/entitytypes"
          },
          "eperson-registration": {
            "href": "https://www.iifl.unam.mx/server/api/eperson/registrations"
          },
          "epersons": {
            "href": "https://www.iifl.unam.mx/server/api/eperson/epersons"
          },
          "externalsources": {
            "href": "https://www.iifl.unam.mx/server/api/integration/externalsources"
          },
          "features": {
            "href": "https://www.iifl.unam.mx/server/api/authz/features"
          },
          "feedbacks": {
            "href": "https://www.iifl.unam.mx/server/api/tools/feedbacks"
          },
          "groups": {
            "href": "https://www.iifl.unam.mx/server/api/eperson/groups"
          },
          "identifiers": {
            "href": "https://www.iifl.unam.mx/server/api/pid/identifiers"
          },
          "itemrequests": {
            "href": "https://www.iifl.unam.mx/server/api/tools/itemrequests"
          },
          "items": {
            "href": "https://www.iifl.unam.mx/server/api/core/items"
          },
          "itemtemplates": {
            "href": "https://www.iifl.unam.mx/server/api/core/itemtemplates"
          },
          "metadatafields": {
            "href": "https://www.iifl.unam.mx/server/api/core/metadatafields"
          },
          "metadataschemas": {
            "href": "https://www.iifl.unam.mx/server/api/core/metadataschemas"
          },
          "oidc": {
            "href": "https://www.iifl.unam.mx/server/api/authn"
          },
          "pid": {
            "href": "https://www.iifl.unam.mx/server/api/pid/find{?id}",
            "templated": true
          },
          "pooltasks": {
            "href": "https://www.iifl.unam.mx/server/api/workflow/pooltasks"
          },
          "pooltasks-search": {
            "href": "https://www.iifl.unam.mx/server/api/workflow/pooltasks/search"
          },
          "processes": {
            "href": "https://www.iifl.unam.mx/server/api/system/processes"
          },
          "properties": {
            "href": "https://www.iifl.unam.mx/server/api/config/properties"
          },
          "registrations": {
            "href": "https://www.iifl.unam.mx/server/api/eperson/registrations"
          },
          "relationships": {
            "href": "https://www.iifl.unam.mx/server/api/core/relationships"
          },
          "relationshiptypes": {
            "href": "https://www.iifl.unam.mx/server/api/core/relationshiptypes"
          },
          "resourcepolicies": {
            "href": "https://www.iifl.unam.mx/server/api/authz/resourcepolicies"
          },
          "resourcepolicies-search": {
            "href": "https://www.iifl.unam.mx/server/api/authz/resourcepolicies/search"
          },
          "scripts": {
            "href": "https://www.iifl.unam.mx/server/api/system/scripts"
          },
          "self": {
            "href": "https://www.iifl.unam.mx/server/api"
          },
          "sites": {
            "href": "https://www.iifl.unam.mx/server/api/core/sites"
          },
          "statistics": {
            "href": "https://www.iifl.unam.mx/server/api/statistics"
          },
          "submissionaccessoptions": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissionaccessoptions"
          },
          "submissioncclicenseUrls": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissioncclicenseUrls"
          },
          "submissioncclicenseUrls-search": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissioncclicenseUrls/search"
          },
          "submissioncclicenses": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissioncclicenses"
          },
          "submissiondefinitions": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissiondefinitions"
          },
          "submissionforms": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissionforms"
          },
          "submissionsections": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissionsections"
          },
          "submissionuploads": {
            "href": "https://www.iifl.unam.mx/server/api/config/submissionuploads"
          },
          "subscriptions": {
            "href": "https://www.iifl.unam.mx/server/api/core/subscriptions"
          },
          "subscriptions-search": {
            "href": "https://www.iifl.unam.mx/server/api/core/subscriptions/search"
          },
          "supervisionorders": {
            "href": "https://www.iifl.unam.mx/server/api/core/supervisionorders"
          },
          "systemwidealerts": {
            "href": "https://www.iifl.unam.mx/server/api/system/systemwidealerts"
          },
          "usagereports": {
            "href": "https://www.iifl.unam.mx/server/api/statistics/usagereports"
          },
          "versionhistories": {
            "href": "https://www.iifl.unam.mx/server/api/versioning/versionhistories"
          },
          "versions": {
            "href": "https://www.iifl.unam.mx/server/api/versioning/versions"
          },
          "vocabularies": {
            "href": "https://www.iifl.unam.mx/server/api/submission/vocabularies"
          },
          "vocabularyEntryDetails": {
            "href": "https://www.iifl.unam.mx/server/api/submission/vocabularyEntryDetails"
          },
          "vocabularyEntryDetails-search": {
            "href": "https://www.iifl.unam.mx/server/api/submission/vocabularyEntryDetails/search"
          },
          "workflowactions": {
            "href": "https://www.iifl.unam.mx/server/api/config/workflowactions"
          },
          "workflowdefinitions": {
            "href": "https://www.iifl.unam.mx/server/api/config/workflowdefinitions"
          },
          "workflowitems": {
            "href": "https://www.iifl.unam.mx/server/api/workflow/workflowitems"
          },
          "workflowsteps": {
            "href": "https://www.iifl.unam.mx/server/api/config/workflowsteps"
          },
          "workspaceitems": {
            "href": "https://www.iifl.unam.mx/server/api/submission/workspaceitems"
          }
        }
      }
    },
    {
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections/e9a8f44f-a8d3-4d22-b02a-cf590285bac6",
      "redirects": [
        {
          "url": "https://www.iifl.unam.mx/server/api/core/collections/e9a8f44f-a8d3-4d22-b02a-cf590285bac6",
          "status": 404
        }
      ],
      "http_status": 404,
      "content_type": "application/hal+json;charset=UTF-8",
      "body_sha256": "b149e2ef4e3a837e9ed382bc66b37ef8bca86195d8f8451cb3150ceb07ddf4fb"
    }
  ],
  "errors": []
}
```
