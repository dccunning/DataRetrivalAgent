from core.services.dbt_parser import DbtParser


class DbtParserCloud(DbtParser):
    def __init__(self, manifest: dict, catalog: dict, db, embed_func):
        super().__init__(manifest, catalog)
        self.db = db
        self.embed_func = embed_func  # A function that turns text -> vector

    def save_outputs(self):
        """
        Save the table summary and table description dicts to the database.
        """
        summary = self.build_table_summary()
        descriptions = self.build_table_descriptions()

        self.db_client.insert("table_summary", summary)
        self.db.run_query("insert into ")
        self.db_client.insert("table_descriptions", descriptions)

    def save_vectors_to_store(self, user_id: int, db_name: str):
        rows = []
        for desc in self.build_table_descriptions():
            table_name = desc["table_name"]
            table_description = desc["table_description"]
            text = f"{table_name}: {table_description}"
            vector = self.embed_func(text)

            rows.append({
                "user_id": user_id,
                "db_name": db_name,
                "vector": vector
            })

        self.db_client.insert("vs_table_descriptions", rows)
