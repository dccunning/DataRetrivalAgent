import streamlit as st
import json
import os
from core.config import load_config, save_config
from core.clients.database import Database  # Assumes you have this

st.set_page_config(page_title="Data Retrieval Agent", layout="wide")
st.title("Data Retrieval Agent")

# Load saved config
config = load_config()

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
            save_config({
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

        if uploaded_manifest and uploaded_catalog:
            st.session_state.manifest_json = json.load(uploaded_manifest)
            st.session_state.catalog_json = json.load(uploaded_catalog)
            st.success("✅ Files uploaded and stored in session.")

        elif os.getenv("DRA_MANIFEST_PATH") and os.getenv("DRA_CATALOG_PATH"):
            try:
                with open(os.getenv("DRA_MANIFEST_PATH")) as f:
                    st.session_state.manifest_json = json.load(f)
                with open(os.getenv("DRA_CATALOG_PATH")) as f:
                    st.session_state.catalog_json = json.load(f)
                st.success("✅ Loaded DBT metadata from environment paths.")
            except Exception as e:
                st.error(f"Failed to load metadata: {e}")

        # Display status
        manifest_status = "✅ Provided" if st.session_state.manifest_json else "❌ Missing"
        catalog_status = "✅ Provided" if st.session_state.catalog_json else "❌ Missing"

        st.write(f"- manifest.json: {manifest_status}")
        st.write(f"- catalog.json: {catalog_status}")

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
