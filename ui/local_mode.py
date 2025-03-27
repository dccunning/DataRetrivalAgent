# UI for local mode usage
import streamlit as st
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from local_storage.credentials import load_credentials, save_credentials
from core.clients.database import Database
from local_storage.dbt_metadata import (
    load_manifest, load_catalog,
    save_manifest, save_catalog,
    parse_and_save_metadata
)

st.set_page_config(page_title="Data Retrieval Agent", layout="wide")
st.title("Data Retrieval Agent")

# Load saved config
config = load_credentials()

# Initialize session state
if "manifest_json" not in st.session_state:
    st.session_state.manifest_json = None
if "catalog_json" not in st.session_state:
    st.session_state.catalog_json = None

# Tabs
tab1, tab2 = st.tabs(["⚙️ Settings", "💬 Query Runner"])

# -------------------------
# ⚙️ Settings Tab
# -------------------------
with tab1:
    st.header("Credentials & Metadata")

    with st.expander("🔐 Credentials", expanded=True):
        openai_key = st.text_input("OpenAI API Key", value=config.get("openai_api_key", ""), type="password")
        host = st.text_input("DB Host", value=config.get("db", {}).get("host", ""))
        user = st.text_input("DB User", value=config.get("db", {}).get("user", ""))
        password = st.text_input("DB Password", value=config.get("db", {}).get("password", ""), type="password")
        database = st.text_input("DB Name", value=config.get("db", {}).get("database", ""))
        port = st.text_input("DB Port", value=str(config.get("db", {}).get("port", "5432")))

        if st.button("Save Config"):
            save_credentials({
                "openai_api_key": openai_key,
                "db": {
                    "host": host,
                    "port": port,
                    "user": user,
                    "password": password,
                    "database": database
                }
            })
            st.success("✅ Config saved.")

    with st.expander("📦 DBT Metadata", expanded=True):
        uploaded_manifest = st.file_uploader("Upload manifest.json", type="json")
        uploaded_catalog = st.file_uploader("Upload catalog.json", type="json")

        manifest_json = None
        catalog_json = None

        if uploaded_manifest and uploaded_catalog:
            manifest_json = json.load(uploaded_manifest)
            catalog_json = json.load(uploaded_catalog)
            st.success("✅ Uploaded and saved to local storage.")

        else:
            # Try loading from ~/.data-retrival-agent/
            try:
                manifest_json = load_manifest()
                catalog_json = load_catalog()
                if manifest_json and catalog_json:
                    st.success("✅ Loaded metadata from local storage.")
                else:
                    st.info("Upload manifest.json and catalog.json to get started.")
            except Exception as e:
                st.error(f"❌ Failed to load metadata: {e}")

        dbt_table_summary = None
        dbt_table_descriptions = None

        if manifest_json and catalog_json:
            save_manifest(manifest_json)
            save_catalog(catalog_json)
            dbt_table_summary, dbt_table_descriptions = parse_and_save_metadata(manifest_json, catalog_json)

        st.write(f"- manifest.json: {'✅ Provided' if manifest_json else '❌ Missing'}")
        st.write(f"- catalog.json: {'✅ Provided' if catalog_json else '❌ Missing'}")

# -------------------------
# 💬 Query Runner Tab
# -------------------------
with tab2:
    st.header("Query Runner")

    if not all([host, user, password, database]):
        st.warning("Please fill in DB credentials in the Settings tab.")
    else:
        query_text = st.text_area("Write your SQL query here", height=200)

        if st.button("Run Query"):
            try:
                db = Database(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port
                )
                results = db.run_query(query_text)
                if results:
                    st.success("✅ Query executed successfully.")
                    st.dataframe(results)
                else:
                    st.info("Query ran but returned no results.")
            except Exception as e:
                st.error(f"❌ Query failed: {e}")
