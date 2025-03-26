import json
from collections import defaultdict


class DbtDocuments:
    pass


# Load manifest and catalog
with open("../../dbt/target/manifest.json") as f:
    manifest = json.load(f)


with open("../../dbt/target/catalog.json") as f:
    catalog = json.load(f)


# Map: (model_id, column_name) -> accepted values
accepted_values_map = defaultdict(list)
for key, test in manifest.get("nodes", {}).items():
    if test.get("resource_type") != "test":
        continue
    if test.get("test_metadata", {}).get("name") == "accepted_values":
        model_id = test.get("depends_on", {}).get("nodes", [None])[0]
        column_name = test.get("test_metadata", {}).get("kwargs", {}).get("column_name")
        values = test.get("test_metadata", {}).get("kwargs", {}).get("values", [])
        if model_id and column_name:
            accepted_values_map[(model_id, column_name)] = values

# Build table summaries
summary = []

for node_id, node in manifest.get("nodes", {}).items():
    if node.get("resource_type") != "model":
        continue

    model_catalog = catalog["nodes"].get(node_id)
    if not model_catalog:
        continue

    model_meta = node.get("description", "")
    model_name = node.get("alias") or node.get("name")
    model_columns = node.get("columns", {})
    catalog_columns = model_catalog.get("columns", {})

    table_info = {
        "table_name": model_name,
        "table_description": model_meta,
        "columns": []
    }

    for col_name, col_meta in model_columns.items():
        col_type = catalog_columns.get(col_name, {}).get("type", "").lower()
        col_info = {
            "name": col_name,
            "type": col_type,
            "description": col_meta.get("description", "")
        }

        enums = accepted_values_map.get((node_id, col_name))
        if enums:
            col_info["enums"] = enums

        table_info["columns"].append(col_info)

    summary.append(table_info)

# Save to file
with open("dbt_table_summary.json", "w") as out_file:
    json.dump(summary, out_file, indent=2)