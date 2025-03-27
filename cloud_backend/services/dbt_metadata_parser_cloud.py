from core.clients.database import Database
from core.services.dbt_metadata_parser import DbtMetadataParser


class DbtMetadataParserCloud(DbtMetadataParser):
    def __init__(self, manifest: dict, catalog: dict, db: Database, embed_func):
        super().__init__(manifest, catalog)
        self.db = db
        self.embed_func = embed_func  # A function that turns text -> vector

    def save_to_vector_store(self, user_id: int, dbt_table_descriptions: dict):
        rows = []
        for desc in dbt_table_descriptions:
            table_name = desc["table_name"]
            table_description = desc["table_description"]
            text = f"{table_name}: {table_description}"
            vector = self.embed_func(text)

            rows.append({
                "user_id": user_id,
                "vector": vector
            })

        query = ""
        self.db.run_query(query)
