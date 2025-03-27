import os
import json
from core.services.dbt_metadata_parser import DbtMetadataParser

OUTPUT_DIR = os.path.expanduser("~/.data-retrival-agent/dbt_metadata/")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "manifest.json")
CATALOG_PATH = os.path.join(OUTPUT_DIR, "catalog.json")
TABLE_SUMMARY_PATH = os.path.join(OUTPUT_DIR, "dbt_table_summary.json")
TABLE_DESCRIPTIONS_PATH = os.path.join(OUTPUT_DIR, "dbt_table_descriptions.json")


def load_manifest():
    """Load manifest.json to local file"""
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return {}


def load_catalog():
    """Load catalog.json to local file"""
    if os.path.exists(CATALOG_PATH):
        with open(CATALOG_PATH) as f:
            return json.load(f)
    return {}


def save_manifest(manifest: dict):
    """Save manifest.json to local file"""
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def save_catalog(catalog: dict):
    """Save catalog.json to local file"""
    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2)


def parse_and_save_metadata(manifest: dict, catalog: dict):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    dbt_metadata = DbtMetadataParser(manifest=manifest, catalog=catalog)

    summary = dbt_metadata.build_table_summary()
    descriptions = dbt_metadata.build_table_descriptions()

    with open(os.path.join(OUTPUT_DIR, "dbt_table_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "dbt_table_descriptions.json"), "w") as f:
        json.dump(descriptions, f, indent=2)

    return summary, descriptions
