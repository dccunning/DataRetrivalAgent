import json
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from cloud_backend.models.user import User
from core.clients.database import Database
from cloud_backend.utils.auth import get_current_user
from cloud_backend.utils.config import fernet
from core.services.dbt_metadata_parser import DbtMetadataParser

router = APIRouter()
db = Database()


class MetadataRequest(BaseModel):
    data: dict


class ParseMetadataRequest(BaseModel):
    manifest: dict
    catalog: dict


@router.get("/manifest")
def get_manifest(current_user: User = Depends(get_current_user)) -> dict:
    query = "SELECT manifest_json FROM backend.user_metadata WHERE user_id = %s"
    result = db.run_query(query, (current_user.id,))
    if not result or not result[0]["manifest_json"]:
        raise HTTPException(status_code=404, detail="No manifest found")

    return json.loads(fernet.decrypt(result[0]["manifest_json"]).decode())


@router.post("/manifest")
def save_manifest(data: MetadataRequest, current_user: User = Depends(get_current_user)):
    encrypted = fernet.encrypt(json.dumps(data.data).encode())
    query = """
        INSERT INTO backend.user_metadata (user_id, manifest_json, updated_at)
        VALUES (%s, %s, NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET manifest_json = EXCLUDED.manifest_json, updated_at = NOW()
    """
    db.run_query(query, (current_user.id, encrypted))
    return {"status": "✅ Manifest saved"}


@router.get("/catalog")
def get_catalog(current_user: User = Depends(get_current_user)) -> dict:
    query = "SELECT catalog_json FROM backend.user_metadata WHERE user_id = %s"
    result = db.run_query(query, (current_user.id,))
    if not result or not result[0]["catalog_json"]:
        raise HTTPException(status_code=404, detail="No catalog found")

    return json.loads(fernet.decrypt(result[0]["catalog_json"]).decode())


@router.post("/catalog")
def save_catalog(data: MetadataRequest, current_user: User = Depends(get_current_user)):
    encrypted = fernet.encrypt(json.dumps(data.data).encode())
    query = """
        INSERT INTO backend.user_metadata (user_id, catalog_json, updated_at)
        VALUES (%s, %s, NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET catalog_json = EXCLUDED.catalog_json, updated_at = NOW()
    """
    db.run_query(query, (current_user.id, encrypted))
    return {"status": "✅ Catalog saved"}


@router.get("/summary_and_descriptions")
def get_summary_and_descriptions(current_user: User = Depends(get_current_user)) -> dict:
    query = """
        SELECT table_summary_json, table_descriptions_json
        FROM backend.user_metadata
        WHERE user_id = %s
    """
    result = db.run_query(query, (current_user.id,))
    if not result or not (result[0]["table_summary_json"] and result[0]["table_descriptions_json"]):
        raise HTTPException(status_code=404, detail="No summary or descriptions found")

    summary = json.loads(fernet.decrypt(result[0]["table_summary_json"]).decode())
    descriptions = json.loads(fernet.decrypt(result[0]["table_descriptions_json"]).decode())

    return {"table_summary": summary, "table_descriptions": descriptions}


@router.post("/summary_and_descriptions")
def save_parsed_summary_and_descriptions(data: ParseMetadataRequest, current_user: User = Depends(get_current_user)) -> dict:
    dbt_metadata = DbtMetadataParser(manifest=data.manifest, catalog=data.catalog)
    summary = dbt_metadata.build_table_summary()
    descriptions = dbt_metadata.build_table_descriptions()

    encrypted_summary = fernet.encrypt(json.dumps(summary).encode())
    encrypted_descriptions = fernet.encrypt(json.dumps(descriptions).encode())

    query = """
        INSERT INTO backend.user_metadata (user_id, table_summary_json, table_descriptions_json, updated_at)
        VALUES (%s, %s, %s, NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET 
            table_summary_json = EXCLUDED.table_summary_json,
            table_descriptions_json = EXCLUDED.table_descriptions_json,
            updated_at = NOW()
    """
    db.run_query(query, (current_user.id, encrypted_summary, encrypted_descriptions))

    return {"table_summary": summary, "table_descriptions": descriptions}
