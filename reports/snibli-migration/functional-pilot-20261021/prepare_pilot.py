"""Offline, case-specific proposal for human review; no network or persistence in DSpace."""

import hashlib
import json
import zipfile
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ITEM = "ba2d355b-a2de-4c29-8fbf-0c9c335c6452"
COLLECTION = "3ce3afb3-94ed-4f60-bfda-0a1242c4d689"
PUBLISHER = "https://ela.enallt.unam.mx/index.php/ela/article/view/632"
RC2 = "c1680bf6b452097e6d8b6e4263043f991676015a3173b3a9673bc1f520660cae"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, data):
    (HERE / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name"):
            self.values.setdefault(attrs["name"], []).append(attrs.get("content"))


def main():
    package = (
        ROOT
        / "skills/dspace-cataloger/versions/v3.9.3-rc.2/dspace-cataloger-v3.9.3-rc.2.skill"
    )
    assert digest(package.read_bytes()) == RC2
    with zipfile.ZipFile(package) as archive:

        def asset(name):
            return json.loads(archive.read("dspace-cataloger/assets/" + name))

        contract = asset("dspace-form-contract-v1.json")
        vocab = asset("controlled-vocabulary-index.json")
        schema = asset("catalog-draft.schema.json")
    item_bytes = (HERE / "item.response").read_bytes()
    item = json.loads(item_bytes)
    assert item["uuid"] == ITEM and item["handle"] == "123456789/733"
    owner = json.loads((HERE / "collection.response").read_bytes())
    mapped = json.loads((HERE / "mapped-collections.response").read_bytes())
    collections = mapped["_embedded"]["mappedCollections"]
    assert mapped["page"]["totalPages"] == 1
    assert mapped["page"]["totalElements"] == len(collections)
    assert COLLECTION in {entry["uuid"] for entry in collections}
    publisher_bytes = (HERE / "publisher.response").read_bytes()
    meta = Metadata()
    meta.feed(publisher_bytes.decode("utf-8"))
    assert meta.values["DC.Type.articleType"] == ["Reseñas"]
    metadata = item["metadata"]

    def current(key):
        return [entry["value"] for entry in metadata.get(key, [])]

    def binding(key, vocabulary=None):
        return next(
            f
            for f in contract["fields"]
            if f["metadataField"] == key
            and (vocabulary is None or f["controlledVocabulary"] == vocabulary)
        )

    fields = []

    def propose(
        key,
        value,
        state,
        explanation,
        *,
        vocabulary=None,
        source_value=None,
        source=None,
    ):
        bound = binding(key, vocabulary)
        name = bound["controlledVocabulary"]
        values = value if isinstance(value, list) else [value]
        valid = (
            all(v in vocab[name]["values"] for v in values)
            if value is not None and name
            else None
        )
        if valid is not None:
            assert valid
        field = {
            "field": key,
            "bindingId": bound["bindingId"],
            "formId": bound["formId"],
            "uiLabel": bound["uiLabel"],
            "renderOrder": bound["renderOrder"],
            "currentValue": current(key),
            "sourceValue": source_value,
            "suggestedValue": value,
            "finalValue": None,
            "evidenceStatus": state,
            "mappingStatus": "MAPPED" if value is not None else "POLICY_REVIEW",
            "vocabulary": name,
            "vocabularyValidated": valid,
            "requiresHumanApproval": True,
            "humanDecision": "PENDING",
            "explanation": explanation,
            "evidence": source
            or [{"file": "item.response", "pointer": "/metadata/" + key}],
        }
        fields.append(field)
        return field

    assert current("dc.type") == ["Article"]
    document_type = propose(
        "dc.type",
        ["Reseña"],
        "VERIFICADO",
        "La fuente editorial declara DC.Type.articleType=Reseñas. La naturaleza documental se conserva frente al contenedor revista; propuesta sin aplicar.",
        source_value="Reseñas",
        source=[
            {
                "file": "publisher.response",
                "url": PUBLISHER,
                "locator": 'meta[name="DC.Type.articleType"]',
            }
        ],
    )
    comparative = propose(
        "dc.type.genre",
        None,
        "PENDIENTE",
        "No se consultó el texto completo. Ni la ausencia del campo ni las múltiples lenguas en el registro prueban ninguna de las tres respuestas; no elegir No por defecto.",
    )
    language = propose(
        "dc.description.registeredLanguage",
        current("dc.description.registeredLanguage"),
        "EXTRAÍDO",
        "Conservar el Español declarado en DSpace; extraído del registro, no verificación independiente de toda la lengua de redacción. No añadir lenguas objeto ni deducirla del idioma de la interfaz editorial.",
        source_value=current("dc.description.registeredLanguage"),
    )
    grouping = propose(
        "dc.subject.linguiscgroup",
        None,
        "PENDIENTE",
        "El registro contiene ocho agrupaciones. Su pertinencia como objetos primarios no se verifica con el resumen o la pertenencia a colecciones; conservar como evidencia sin proponer adiciones o eliminaciones.",
        source_value=current("dc.subject.linguiscgroup"),
    )
    assert "Sociolingüística" in current("dc.subject")
    assert "Sociolingüística" in vocab["topicsPairs"]["values"]
    assert "Sociolingüística" not in vocab["srsc"]["values"]
    keywords = propose(
        "dc.subject",
        None,
        "PENDIENTE",
        vocabulary="srsc",
        explanation="La clave compartida dc.subject no revela qué control originó cada valor. No traducir Sociolingüística a una categoría srsc por aproximación ni asignarla a ambos controles.",
    )
    topics = propose(
        "dc.subject",
        ["Sociolingüística"],
        "EXTRAÍDO",
        vocabulary="topicsPairs",
        source_value="Sociolingüística",
        explanation="Valor literal ya presente en dc.subject y permitido en topicsPairs; candidato para este control, no identificación del widget original. Revisión humana antes de reubicar o copiar; no sustituye los demás valores existentes.",
    )
    extent = propose(
        "dc.format.extent",
        current("dc.format.extent"),
        "EXTRAÍDO",
        "Conservar páginas 207-213 de la reseña. Las 802 páginas del título corresponden al libro reseñado y no deben reemplazar su extensión.",
        source_value=current("dc.format.extent"),
    )
    draft = {
        "status": "REQUIERE-REVISIÓN",
        "formContractVersion": contract["contractVersion"],
        "skillVersion": "3.9.3-rc.2",
        "scope": "Focused real-record pilot; not full recataloging",
        "source": {
            "primary": PUBLISHER,
            "accessedAt": datetime.now(UTC).isoformat(),
            "itemUuid": ITEM,
            "handle": item["handle"],
            "itemSha256": digest(item_bytes),
            "publisherSha256": digest(publisher_bytes),
        },
        "collectionContext": {
            "selectedCollection": COLLECTION,
            "owningCollection": owner["uuid"],
            "membership": "MAPPED_COLLECTION_NOT_OWNER",
        },
        "fields": fields,
        "qa": [
            {
                "code": "PILOT-DOCUMENT-TYPE",
                "severity": "REVIEW",
                "status": "FAIL",
                "fields": ["dc.type"],
                "explanation": "Article en DSpace frente a Reseñas en fuente editorial; corrección pendiente.",
            }
        ],
        "governance": {
            "humanApprovalRequired": True,
            "humanApprovalGranted": False,
            "dspaceWriteEnabled": False,
            "applied": False,
        },
    }
    Draft202012Validator(schema).validate(draft)
    checks = {
        "rc2_integrity": digest(package.read_bytes()) == RC2,
        "draft_schema": True,
        "new_document_type_exact_match": document_type["suggestedValue"] == ["Reseña"]
        and document_type["vocabularyValidated"],
        "comparative_abstention": comparative["suggestedValue"] is None
        and comparative["evidenceStatus"] == "PENDIENTE",
        "language_separation": language["suggestedValue"] == ["Español"]
        and grouping["suggestedValue"] is None,
        "shared_metadata_separate_bindings": keywords["bindingId"]
        != topics["bindingId"]
        and keywords["suggestedValue"] is None,
        "extent_not_borrowed_from_reviewed_book": extent["suggestedValue"]
        == ["páginas 207-213"],
        "pending_human_review_no_final_values": all(
            f["humanDecision"] == "PENDING" and f["finalValue"] is None for f in fields
        ),
        "no_dspace_writes": not draft["governance"]["applied"]
        and not draft["governance"]["dspaceWriteEnabled"],
    }
    assert all(checks.values()), checks
    save("proposal.json", draft)
    save(
        "validation.json",
        {
            "status": "TECHNICAL_PASS_HUMAN_REVIEW_REQUIRED",
            "checks": checks,
            "skillSha256": RC2,
            "existingRecordIssue": "DOCUMENT_TYPE_MISMATCH",
            "humanAcceptance": "PENDING",
            "stableReleasePromotion": "NOT_PERFORMED",
            "scope": "One focused case; no independent adjudication, full-text evaluation or global migration certification",
        },
    )
    files = (
        "item.response",
        "publisher.response",
        "collection.response",
        "mapped-collections.response",
    )
    save(
        "source-manifest.json",
        {
            "methods": ["GET"],
            "credentialsUsed": False,
            "files": {
                name: {
                    "sha256": digest((HERE / name).read_bytes()),
                    "bytes": (HERE / name).stat().st_size,
                }
                for name in files
            },
        },
    )
    print(
        json.dumps(
            {
                "status": "TECHNICAL_PASS_HUMAN_REVIEW_REQUIRED",
                "checks": len(checks),
                "draftFields": len(fields),
            }
        )
    )


if __name__ == "__main__":
    main()
