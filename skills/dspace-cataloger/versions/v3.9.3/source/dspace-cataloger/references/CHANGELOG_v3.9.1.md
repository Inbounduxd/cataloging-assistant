> Carried forward from v3.9.2. For current SNIBLI instance, form counts, order, vocabulary values and runtime lock, use [SNIBLI_MIGRATION_2026.md](SNIBLI_MIGRATION_2026.md) and current assets. Historical release counts and verification claims do not certify this candidate.

# Changelog v3.9.1

Re-derived semantic patch carried forward from the repository-readable v3.9.1
contract mirror because the original v3.9.1 package failed integrity recovery.

- GR21: linguistic relevance for indexing.
- GR22: no genealogical propagation from secondary language mentions.
- Roles: `PRIMARY_SUBJECT_LANGUAGE`, `SECONDARY_LANGUAGE_MENTION`,
  `VARIANT_EVIDENCE`.
- QA: `CAT-LING-REL-001` through `CAT-LING-REL-004`.
