"""
API FastAPI pour gérer les vector stores et leurs fichiers OpenAI
Vous pouvez tester ces endpoints depuis Postman en passant la clé API OpenAI en paramètre
"""

from fastapi import FastAPI, HTTPException, Header
from typing import Optional, List
import requests
from pydantic import BaseModel
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OpenAI Vector Store & Files Management API",
    description="API pour gérer les vector stores, leurs fichiers, et tous les fichiers OpenAI",
    version="3.0.0"
)

BASE_URL = "https://api.openai.com/v1"


class DeleteResponse(BaseModel):
    """Modèle de réponse pour la suppression"""
    id: str
    object: str
    deleted: bool


class VectorStoreFile(BaseModel):
    """Modèle représentant un fichier de vector store"""
    id: str
    object: str
    created_at: int
    vector_store_id: str


class ListFilesResponse(BaseModel):
    """Modèle de réponse pour la liste des fichiers"""
    object: str
    data: List[VectorStoreFile]
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: bool


class VectorStoreDeleteRequest(BaseModel):
    """Modèle de requête pour supprimer plusieurs vector stores"""
    vector_store_ids: List[str]


class BulkDeleteResponse(BaseModel):
    """Modèle de réponse pour la suppression en masse"""
    success: List[str]
    failed: List[dict]


class VectorStoreDeleteWithFilesRequest(BaseModel):
    """Modèle de requête pour supprimer plusieurs vector stores ET leurs fichiers"""
    vector_store_ids: List[str]
    delete_files: bool = True  # Par défaut, on supprime aussi les fichiers


class BulkDeleteWithFilesResponse(BaseModel):
    """Modèle de réponse pour la suppression en masse avec fichiers"""
    vector_stores_deleted: List[str]
    vector_stores_failed: List[dict]
    files_deleted: List[str]
    files_failed: List[dict]
    total_files_found: int


@app.on_event("startup")
async def startup_event():
    """Événement au démarrage de l'application"""
    logger.info("=" * 60)
    logger.info("🚀 OpenAI Vector Store Management API - Démarrage")
    logger.info("=" * 60)
    logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🌐 Base URL OpenAI: {BASE_URL}")
    logger.info(f"📖 Documentation: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Événement à l'arrêt de l'application"""
    logger.info("=" * 60)
    logger.info("🛑 OpenAI Vector Store Management API - Arrêt")
    logger.info("=" * 60)


@app.get("/")
def read_root():
    """Endpoint racine avec les instructions d'utilisation"""
    logger.info("📍 Endpoint appelé: GET /")
    logger.info("✅ Retour des informations de l'API")
    
    return {
        "message": "API OpenAI Vector Store & Files Management",
        "version": "3.0.0",
        "endpoints": {
            "vector_stores": {
                "GET /vector_stores": "Lister tous les vector stores de votre compte",
                "DELETE /vector_stores": "Supprimer plusieurs vector stores (array d'IDs dans le body)",
                "DELETE /vector_stores/with-files": "⚡ Supprimer vector stores ET leurs fichiers (recommandé)",
                "GET /vector_stores/{vector_store_id}/files": "Lister tous les fichiers d'un vector store",
                "DELETE /vector_stores/{vector_store_id}/files/{file_id}": "Supprimer un fichier d'un vector store"
            },
            "files": {
                "GET /files": "Lister tous les fichiers de votre compte OpenAI",
                "DELETE /files": "Supprimer plusieurs fichiers (array d'IDs dans le body)"
            }
        },
        "usage": {
            "header_required": "x-openai-api-key: votre_clé_api_openai",
            "example": "Passez votre clé OpenAI dans le header 'x-openai-api-key'"
        },
        "note": "Supprimer un fichier le retire automatiquement de TOUS les vector stores"
    }


@app.get("/vector_stores")
def list_vector_stores(
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI"),
    after: Optional[str] = None,
    before: Optional[str] = None,
    limit: Optional[int] = 100,
    order: Optional[str] = "desc"
):
    """
    Liste tous les IDs des vector stores de votre compte OpenAI.
    
    Args:
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
        after: Curseur pour la pagination
        before: Curseur pour la pagination
        limit: Nombre maximum de résultats (1-100, défaut: 100)
        order: Ordre de tri (asc ou desc, défaut: desc)
    
    Returns:
        Array simple d'IDs de vector stores: ["vs_id1", "vs_id2", ...]
    """
    logger.info("=" * 60)
    logger.info("📍 Endpoint appelé: GET /vector_stores")
    logger.info(f"📊 Paramètres: limit={limit}, order={order}, after={after}, before={before}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    url = f"{BASE_URL}/vector_stores"
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    all_ids = []
    page_count = 0
    
    # Récupérer tous les vector stores avec pagination automatique
    params = {
        "limit": limit,
        "order": order
    }
    
    if after:
        params["after"] = after
    if before:
        params["before"] = before
    
    try:
        logger.info("🔄 Début de la récupération des vector stores...")
        
        while True:
            page_count += 1
            logger.info(f"📄 Page {page_count}: Appel API OpenAI...")
            
            response = requests.get(url, headers=headers, params=params)
            
            logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"❌ Erreur OpenAI API: {response.status_code}")
                logger.error(f"❌ Détails: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erreur OpenAI API: {response.text}"
                )
            
            data = response.json()
            
            # Extraire les IDs
            items_count = len(data.get("data", []))
            logger.info(f"📦 {items_count} vector stores trouvés sur cette page")
            
            for item in data.get("data", []):
                vector_store_id = item.get("id")
                all_ids.append(vector_store_id)
                logger.debug(f"  ✓ {vector_store_id}")
            
            # Vérifier s'il y a plus de résultats
            has_more = data.get("has_more", False)
            logger.info(f"🔍 Plus de résultats disponibles: {has_more}")
            
            if not has_more:
                break
            
            # Utiliser le dernier ID pour la pagination
            params["after"] = data.get("last_id")
            logger.info(f"➡️  Pagination: after={params['after']}")
        
        logger.info(f"✅ Total récupéré: {len(all_ids)} vector stores")
        logger.info(f"📊 Nombre de pages parcourues: {page_count}")
        logger.info("=" * 60)
        
        return all_ids
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erreur de connexion: {str(e)}")
        logger.error("=" * 60)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de connexion: {str(e)}"
        )


@app.delete("/vector_stores", response_model=BulkDeleteResponse)
def delete_multiple_vector_stores(
    request: VectorStoreDeleteRequest,
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI")
):
    """
    Supprime plusieurs vector stores en une seule requête.
    
    Args:
        request: Objet contenant un array de vector_store_ids à supprimer
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
    
    Returns:
        Résultat de la suppression avec les IDs réussis et échoués
    
    Example body:
        {
            "vector_store_ids": ["vs_abc123", "vs_def456", "vs_ghi789"]
        }
    """
    logger.info("=" * 60)
    logger.info("📍 Endpoint appelé: DELETE /vector_stores")
    logger.info(f"🗑️  Nombre de vector stores à supprimer: {len(request.vector_store_ids)}")
    logger.info(f"📋 IDs: {request.vector_store_ids}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    success = []
    failed = []
    
    logger.info("🔄 Début de la suppression...")
    
    for index, vector_store_id in enumerate(request.vector_store_ids, 1):
        logger.info(f"🗑️  [{index}/{len(request.vector_store_ids)}] Suppression de: {vector_store_id}")
        
        url = f"{BASE_URL}/vector_stores/{vector_store_id}"
        
        try:
            response = requests.delete(url, headers=headers)
            
            logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
            
            if response.status_code in (200, 204):
                success.append(vector_store_id)
                logger.info(f"✅ Supprimé avec succès: {vector_store_id}")
            else:
                failed.append({
                    "id": vector_store_id,
                    "error": response.text,
                    "status_code": response.status_code
                })
                logger.error(f"❌ Échec de suppression: {vector_store_id}")
                logger.error(f"❌ Erreur: {response.text}")
        except requests.exceptions.RequestException as e:
            failed.append({
                "id": vector_store_id,
                "error": str(e),
                "status_code": 500
            })
            logger.error(f"❌ Erreur de connexion pour {vector_store_id}: {str(e)}")
    
    logger.info("=" * 60)
    logger.info(f"📊 Résumé de la suppression:")
    logger.info(f"  ✅ Succès: {len(success)}")
    logger.info(f"  ❌ Échecs: {len(failed)}")
    logger.info("=" * 60)
    
    return {
        "success": success,
        "failed": failed
    }


@app.delete("/vector_stores/with-files", response_model=BulkDeleteWithFilesResponse)
def delete_vector_stores_with_files(
    request: VectorStoreDeleteWithFilesRequest,
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI")
):
    """
    Supprime plusieurs vector stores ET leurs fichiers en une seule requête.
    
    Cette fonction:
    1. Liste tous les fichiers de chaque vector store
    2. Supprime les vector stores
    3. Supprime tous les fichiers trouvés (si delete_files=true)
    
    Args:
        request: Objet contenant un array de vector_store_ids et l'option delete_files
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
    
    Returns:
        Résultat détaillé de la suppression des vector stores et fichiers
    
    Example body:
        {
            "vector_store_ids": ["vs_abc123", "vs_def456"],
            "delete_files": true
        }
    """
    logger.info("=" * 60)
    logger.info("📋 Endpoint appelé: DELETE /vector_stores/with-files")
    logger.info(f"🗑️  Nombre de vector stores à supprimer: {len(request.vector_store_ids)}")
    logger.info(f"📋 IDs: {request.vector_store_ids}")
    logger.info(f"📁 Supprimer les fichiers: {request.delete_files}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    # Étape 1: Collecter tous les fichiers des vector stores
    all_file_ids = set()  # Utiliser un set pour éviter les doublons
    
    if request.delete_files:
        logger.info("🔄 Étape 1: Collecte des fichiers des vector stores...")
        
        for vs_id in request.vector_store_ids:
            logger.info(f"📂 Récupération des fichiers de: {vs_id}")
            
            url = f"{BASE_URL}/vector_stores/{vs_id}/files"
            params = {"limit": 100}
            
            try:
                while True:
                    response = requests.get(url, headers=headers, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        files = data.get("data", [])
                        
                        for file in files:
                            file_id = file.get("id")
                            all_file_ids.add(file_id)
                            logger.debug(f"  ✓ Fichier trouvé: {file_id}")
                        
                        logger.info(f"  📦 {len(files)} fichiers trouvés dans {vs_id}")
                        
                        if not data.get("has_more", False):
                            break
                        
                        params["after"] = data.get("last_id")
                    else:
                        logger.warning(f"⚠️  Impossible de lister les fichiers de {vs_id}: {response.status_code}")
                        break
                        
            except requests.exceptions.RequestException as e:
                logger.warning(f"⚠️  Erreur lors de la récupération des fichiers de {vs_id}: {str(e)}")
        
        logger.info(f"✅ Total de fichiers uniques trouvés: {len(all_file_ids)}")
    
    # Étape 2: Supprimer les vector stores
    logger.info("🔄 Étape 2: Suppression des vector stores...")
    
    vs_success = []
    vs_failed = []
    
    for index, vector_store_id in enumerate(request.vector_store_ids, 1):
        logger.info(f"🗑️  [{index}/{len(request.vector_store_ids)}] Suppression de: {vector_store_id}")
        
        url = f"{BASE_URL}/vector_stores/{vector_store_id}"
        
        try:
            response = requests.delete(url, headers=headers)
            
            logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
            
            if response.status_code in (200, 204):
                vs_success.append(vector_store_id)
                logger.info(f"✅ Supprimé avec succès: {vector_store_id}")
            else:
                vs_failed.append({
                    "id": vector_store_id,
                    "error": response.text,
                    "status_code": response.status_code
                })
                logger.error(f"❌ Échec de suppression: {vector_store_id}")
        except requests.exceptions.RequestException as e:
            vs_failed.append({
                "id": vector_store_id,
                "error": str(e),
                "status_code": 500
            })
            logger.error(f"❌ Erreur de connexion pour {vector_store_id}: {str(e)}")
    
    # Étape 3: Supprimer les fichiers
    files_success = []
    files_failed = []
    
    if request.delete_files and all_file_ids:
        logger.info("🔄 Étape 3: Suppression des fichiers...")
        
        file_list = list(all_file_ids)
        
        for index, file_id in enumerate(file_list, 1):
            logger.info(f"🗑️  [{index}/{len(file_list)}] Suppression de: {file_id}")
            
            url = f"{BASE_URL}/files/{file_id}"
            
            try:
                response = requests.delete(url, headers=headers)
                
                logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
                
                if response.status_code in (200, 204):
                    files_success.append(file_id)
                    logger.info(f"✅ Fichier supprimé: {file_id}")
                else:
                    files_failed.append({
                        "id": file_id,
                        "error": response.text,
                        "status_code": response.status_code
                    })
                    logger.error(f"❌ Échec suppression fichier: {file_id}")
            except requests.exceptions.RequestException as e:
                files_failed.append({
                    "id": file_id,
                    "error": str(e),
                    "status_code": 500
                })
                logger.error(f"❌ Erreur de connexion pour {file_id}: {str(e)}")
    
    # Résumé
    logger.info("=" * 60)
    logger.info(f"📊 Résumé de la suppression:")
    logger.info(f"  🗄️ Vector Stores:")
    logger.info(f"    ✅ Succès: {len(vs_success)}")
    logger.info(f"    ❌ Échecs: {len(vs_failed)}")
    logger.info(f"  📁 Fichiers:")
    logger.info(f"    🔍 Trouvés: {len(all_file_ids)}")
    logger.info(f"    ✅ Supprimés: {len(files_success)}")
    logger.info(f"    ❌ Échecs: {len(files_failed)}")
    logger.info("=" * 60)
    
    return {
        "vector_stores_deleted": vs_success,
        "vector_stores_failed": vs_failed,
        "files_deleted": files_success,
        "files_failed": files_failed,
        "total_files_found": len(all_file_ids)
    }


@app.get("/vector_stores/{vector_store_id}/files", response_model=ListFilesResponse)
def list_vector_store_files(
    vector_store_id: str,
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI"),
    after: Optional[str] = None,
    before: Optional[str] = None,
    filter_status: Optional[str] = None,
    limit: Optional[int] = 20,
    order: Optional[str] = "desc"
):
    """
    Liste tous les fichiers d'un vector store.
    
    Args:
        vector_store_id: L'ID du vector store
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
        after: Curseur pour la pagination
        before: Curseur pour la pagination
        filter_status: Filtrer par statut (in_progress, completed, failed, cancelled)
        limit: Nombre maximum de résultats (1-100, défaut: 20)
        order: Ordre de tri (asc ou desc, défaut: desc)
    
    Returns:
        Liste des fichiers du vector store
    """
    logger.info("=" * 60)
    logger.info(f"📍 Endpoint appelé: GET /vector_stores/{vector_store_id}/files")
    logger.info(f"📊 Paramètres: limit={limit}, order={order}, filter={filter_status}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    url = f"{BASE_URL}/vector_stores/{vector_store_id}/files"
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    params = {
        "limit": limit,
        "order": order
    }
    
    if after:
        params["after"] = after
    if before:
        params["before"] = before
    if filter_status:
        params["filter"] = filter_status
    
    try:
        logger.info("🔄 Appel API OpenAI pour lister les fichiers...")
        response = requests.get(url, headers=headers, params=params)
        
        logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            files_count = len(data.get("data", []))
            logger.info(f"✅ {files_count} fichiers trouvés")
            logger.info("=" * 60)
            return data
        else:
            logger.error(f"❌ Erreur OpenAI API: {response.status_code}")
            logger.error(f"❌ Détails: {response.text}")
            logger.error("=" * 60)
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erreur OpenAI API: {response.text}"
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erreur de connexion: {str(e)}")
        logger.error("=" * 60)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de connexion: {str(e)}"
        )


@app.delete("/vector_stores/{vector_store_id}/files/{file_id}", response_model=DeleteResponse)
def delete_vector_store_file(
    vector_store_id: str,
    file_id: str,
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI")
):
    """
    Supprime un fichier d'un vector store.
    
    Note: Cela supprime le fichier du vector store mais ne supprime pas le fichier lui-même.
    
    Args:
        vector_store_id: L'ID du vector store
        file_id: L'ID du fichier à supprimer
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
    
    Returns:
        Statut de la suppression
    """
    logger.info("=" * 60)
    logger.info(f"📍 Endpoint appelé: DELETE /vector_stores/{vector_store_id}/files/{file_id}")
    logger.info(f"🗑️  Vector Store: {vector_store_id}")
    logger.info(f"📄 Fichier: {file_id}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    url = f"{BASE_URL}/vector_stores/{vector_store_id}/files/{file_id}"
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    try:
        logger.info("🔄 Appel API OpenAI pour supprimer le fichier...")
        response = requests.delete(url, headers=headers)
        
        logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
        
        if response.status_code in (200, 204):
            logger.info(f"✅ Fichier supprimé avec succès: {file_id}")
            logger.info("=" * 60)
            return response.json()
        else:
            logger.error(f"❌ Erreur OpenAI API: {response.status_code}")
            logger.error(f"❌ Détails: {response.text}")
            logger.error("=" * 60)
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erreur OpenAI API: {response.text}"
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erreur de connexion: {str(e)}")
        logger.error("=" * 60)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de connexion: {str(e)}"
        )


@app.get("/files")
def list_all_files(
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI"),
    after: Optional[str] = None,
    limit: Optional[int] = 10000,
    order: Optional[str] = "desc",
    purpose: Optional[str] = None
):
    """
    Liste tous les IDs des fichiers de votre compte OpenAI.
    
    Args:
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
        after: Curseur pour la pagination
        limit: Nombre maximum de résultats (1-10000, défaut: 10000)
        order: Ordre de tri (asc ou desc, défaut: desc)
        purpose: Filtrer par purpose (assistants, fine-tune, batch, etc.)
    
    Returns:
        Array simple d'IDs de fichiers: ["file-id1", "file-id2", ...]
    """
    logger.info("=" * 60)
    logger.info("📋 Endpoint appelé: GET /files")
    logger.info(f"📊 Paramètres: limit={limit}, order={order}, purpose={purpose}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    url = f"{BASE_URL}/files"
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json"
    }
    
    all_ids = []
    page_count = 0
    
    params = {
        "limit": limit,
        "order": order
    }
    
    if after:
        params["after"] = after
    if purpose:
        params["purpose"] = purpose
    
    try:
        logger.info("🔄 Début de la récupération des fichiers...")
        
        while True:
            page_count += 1
            logger.info(f"📄 Page {page_count}: Appel API OpenAI...")
            
            response = requests.get(url, headers=headers, params=params)
            
            logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"❌ Erreur OpenAI API: {response.status_code}")
                logger.error(f"❌ Détails: {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Erreur OpenAI API: {response.text}"
                )
            
            data = response.json()
            
            items_count = len(data.get("data", []))
            logger.info(f"📦 {items_count} fichiers trouvés sur cette page")
            
            for item in data.get("data", []):
                file_id = item.get("id")
                all_ids.append(file_id)
                logger.debug(f"  ✓ {file_id}")
            
            has_more = data.get("has_more", False)
            logger.info(f"🔍 Plus de résultats disponibles: {has_more}")
            
            if not has_more:
                break
            
            params["after"] = data.get("last_id")
            logger.info(f"➡️  Pagination: after={params['after']}")
        
        logger.info(f"✅ Total récupéré: {len(all_ids)} fichiers")
        logger.info(f"📊 Nombre de pages parcourues: {page_count}")
        logger.info("=" * 60)
        
        return all_ids
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erreur de connexion: {str(e)}")
        logger.error("=" * 60)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de connexion: {str(e)}"
        )


class FileDeleteRequest(BaseModel):
    """Modèle de requête pour supprimer plusieurs fichiers"""
    file_ids: List[str]


@app.delete("/files", response_model=BulkDeleteResponse)
def delete_multiple_files(
    request: FileDeleteRequest,
    x_openai_api_key: str = Header(..., description="Votre clé API OpenAI")
):
    """
    Supprime plusieurs fichiers en une seule requête.
    Note: Supprimer un fichier le retire automatiquement de TOUS les vector stores.
    
    Args:
        request: Objet contenant un array de file_ids à supprimer
        x_openai_api_key: Votre clé API OpenAI (passée dans le header)
    
    Returns:
        Résultat de la suppression avec les IDs réussis et échoués
    
    Example body:
        {
            "file_ids": ["file-abc123", "file-def456", "file-ghi789"]
        }
    """
    logger.info("=" * 60)
    logger.info("📋 Endpoint appelé: DELETE /files")
    logger.info(f"🗑️  Nombre de fichiers à supprimer: {len(request.file_ids)}")
    logger.info(f"📋 IDs: {request.file_ids}")
    logger.info(f"🔑 Clé API fournie: {x_openai_api_key[:20]}..." if x_openai_api_key else "❌ Pas de clé API")
    
    headers = {
        "Authorization": f"Bearer {x_openai_api_key}",
        "Content-Type": "application/json"
    }
    
    success = []
    failed = []
    
    logger.info("🔄 Début de la suppression...")
    
    for index, file_id in enumerate(request.file_ids, 1):
        logger.info(f"🗑️  [{index}/{len(request.file_ids)}] Suppression de: {file_id}")
        
        url = f"{BASE_URL}/files/{file_id}"
        
        try:
            response = requests.delete(url, headers=headers)
            
            logger.info(f"📡 Réponse OpenAI: Status {response.status_code}")
            
            if response.status_code in (200, 204):
                success.append(file_id)
                logger.info(f"✅ Supprimé avec succès: {file_id}")
            else:
                failed.append({
                    "id": file_id,
                    "error": response.text,
                    "status_code": response.status_code
                })
                logger.error(f"❌ Échec de suppression: {file_id}")
                logger.error(f"❌ Erreur: {response.text}")
        except requests.exceptions.RequestException as e:
            failed.append({
                "id": file_id,
                "error": str(e),
                "status_code": 500
            })
            logger.error(f"❌ Erreur de connexion pour {file_id}: {str(e)}")
    
    logger.info("=" * 60)
    logger.info(f"📊 Résumé de la suppression:")
    logger.info(f"  ✅ Succès: {len(success)}")
    logger.info(f"  ❌ Échecs: {len(failed)}")
    logger.info("=" * 60)
    
    return {
        "success": success,
        "failed": failed
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Lancement du serveur Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

