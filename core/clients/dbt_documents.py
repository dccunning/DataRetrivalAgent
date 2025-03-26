import os
import json
from typing import List, Dict
from collections import defaultdict



class DbtDocuments:
    def __init__(self, manifest: dict, catalog: dict):
        self.manifest = manifest
        self.catalog = catalog
        self.accepted_values_map = self._build_accepted_values()

    def _build_accepted_values(self) -> Dict:
        """
        Create each columns list of accepted values.
        """
        accepted_values_map = defaultdict(list)
        for key, test in self.manifest.get("nodes", {}).items():
            if test.get("resource_type") != "test":
                continue
            if test.get("test_metadata", {}).get("name") == "accepted_values":
                model_id = test.get("depends_on", {}).get("nodes", [None])[0]
                column_name = test.get("test_metadata", {}).get("kwargs", {}).get("column_name")
                values = test.get("test_metadata", {}).get("kwargs", {}).get("values", [])
                if model_id and column_name:
                    accepted_values_map[(model_id, column_name)] = values
        return accepted_values_map

    @staticmethod
    def _simplify_type(raw_type: str) -> str:
        raw_type = raw_type.lower()
        if any(t in raw_type for t in ["char", "text", "string"]):
            return "string"
        if any(t in raw_type for t in ["int", "decimal", "numeric", "float", "double", "number"]):
            return "number"
        if "bool" in raw_type:
            return "boolean"
        if "date" in raw_type or "time" in raw_type:
            return "datetime"
        return "other"

    def build_table_summary(self) -> List[Dict]:
        """
        Create a list of dicts for all table details with column names, descriptions,
        types and enums.

        :return: [ {"table_name": "", "table_description": "", "columns": []}, ... ]
        """
        summary = []
        for node_id, node in self.manifest.get("nodes", {}).items():
            if node.get("resource_type") != "model":
                continue

            model_catalog = self.catalog["nodes"].get(node_id)
            if not model_catalog:
                continue

            model_name = node.get("alias") or node.get("name")
            model_description = node.get("description", "")
            model_columns = node.get("columns", {})
            catalog_columns = model_catalog.get("columns", {})

            table_info = {
                "table_name": model_name,
                "table_description": model_description,
                "columns": []
            }

            for col_name, col_meta in model_columns.items():
                raw_type = catalog_columns.get(col_name, {}).get("type", "")
                col_info = {
                    "name": col_name,
                    "type": self._simplify_type(raw_type),
                    "description": col_meta.get("description", "")
                }

                enums = self.accepted_values_map.get((node_id, col_name))
                if enums:
                    col_info["enums"] = enums

                table_info["columns"].append(col_info)

            summary.append(table_info)
        return summary

    def build_table_descriptions(self) -> List[Dict]:
        """
        Create a list of dicts for all table names with their descriptions.

        :return: [ {"table_name": "", "table_description": ""}, ... ]
        """
        descriptions = []
        for node_id, node in self.manifest.get("nodes", {}).items():
            if node.get("resource_type") != "model":
                continue

            model_name = node.get("alias") or node.get("name")
            model_description = node.get("description", "")
            descriptions.append({
                "table_name": model_name,
                "table_description": model_description
            })
        return descriptions

    def save_outputs(self):
        """
        Save the table summary and table description lists to the local package folder:
        .data-retrival-agent/
        """
        output_dir = os.path.expanduser("~/.data-retrival-agent/table_meta_data/")
        os.makedirs(output_dir, exist_ok=True)

        summary = self.build_table_summary()
        descriptions = self.build_table_descriptions()

        with open(os.path.join(output_dir, "dbt_table_summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

        with open(os.path.join(output_dir, "dbt_table_descriptions.json"), "w") as f:
            json.dump(descriptions, f, indent=2)
