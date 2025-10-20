# API OpenAI Vector Store Management - Version 2.0

Cette API FastAPI vous permet de gérer les vector stores et leurs fichiers OpenAI en passant votre clé API en paramètre depuis Postman.

## 🆕 Nouveautés Version 2.0

- ✅ **Liste tous les vector stores** de votre compte en une seule requête
- ✅ **Suppression en masse** de plusieurs vector stores via un array d'IDs
- ✅ Gestion des erreurs améliorée avec rapports détaillés
- ✅ Support de la pagination pour tous les endpoints de liste

## Endpoints disponibles

### 1. Lister tous les vector stores

**Endpoint:** `GET /vector_stores`

**Headers requis:**
- `x-openai-api-key`: Votre clé API OpenAI

**Paramètres de requête (optionnels):**
- `after` (string): Curseur pour la pagination
- `before` (string): Curseur pour la pagination
- `limit` (integer): Nombre de résultats (1-100, défaut: 20)
- `order` (string): Ordre de tri (`asc` ou `desc`, défaut: `desc`)

**Exemple de requête Postman:**
```
GET http://localhost:8000/vector_stores
Headers:
  x-openai-api-key: sk-votre_clé_ici
```

**Réponse:** Array de tous vos vector stores avec leurs détails (ID, nom, description, nombre de fichiers, etc.)

---

### 2. Supprimer plusieurs vector stores (Bulk Delete)

**Endpoint:** `DELETE /vector_stores`

**Headers requis:**
- `x-openai-api-key`: Votre clé API OpenAI
- `Content-Type`: application/json

**Body (JSON):**
```json
{
  "vector_store_ids": ["vs_abc123", "vs_def456", "vs_ghi789"]
}
```

**Exemple de requête Postman:**
```
DELETE http://localhost:8000/vector_stores
Headers:
  x-openai-api-key: sk-votre_clé_ici
  Content-Type: application/json
Body (raw JSON):
{
  "vector_store_ids": ["vs_abc123", "vs_def456"]
}
```

**Réponse:** 
```json
{
  "success": ["vs_abc123", "vs_def456"],
  "failed": []
}
```

---

### 3. Lister les fichiers d'un vector store

**Endpoint:** `GET /vector_stores/{vector_store_id}/files`

**Headers requis:**
- `x-openai-api-key`: Votre clé API OpenAI

**Paramètres de requête (optionnels):**
- `after` (string): Curseur pour la pagination
- `before` (string): Curseur pour la pagination
- `filter_status` (string): Filtrer par statut (`in_progress`, `completed`, `failed`, `cancelled`)
- `limit` (integer): Nombre de résultats (1-100, défaut: 20)
- `order` (string): Ordre de tri (`asc` ou `desc`, défaut: `desc`)

**Exemple de requête Postman:**
```
GET http://localhost:8000/vector_stores/vs_abc123/files
Headers:
  x-openai-api-key: sk-votre_clé_ici
```

---

### 4. Supprimer un fichier d'un vector store

**Endpoint:** `DELETE /vector_stores/{vector_store_id}/files/{file_id}`

**Headers requis:**
- `x-openai-api-key`: Votre clé API OpenAI

**Exemple de requête Postman:**
```
DELETE http://localhost:8000/vector_stores/vs_abc123/files/file-abc456
Headers:
  x-openai-api-key: sk-votre_clé_ici
```

---

## Installation et démarrage

### 1. Installer les dépendances

```bash
pip3 install -r requirements.txt
```

### 2. Démarrer le serveur

```bash
python3 vector_store_api.py
```

Le serveur démarrera sur `http://localhost:8000`

### 3. Documentation interactive

Une fois le serveur démarré, vous pouvez accéder à:
- **Documentation Swagger UI**: http://localhost:8000/docs
- **Documentation ReDoc**: http://localhost:8000/redoc

## Utilisation avec Postman

### Configuration de base

Pour toutes les requêtes, vous devez ajouter le header:
- **Key:** `x-openai-api-key`
- **Value:** `sk-votre_clé_openai_ici`

### Workflow recommandé

1. **Lister tous vos vector stores**
   ```
   GET /vector_stores
   ```
   Cela vous retourne un array de tous vos vector stores avec leurs IDs.

2. **Supprimer plusieurs vector stores en une fois**
   ```
   DELETE /vector_stores
   Body: {"vector_store_ids": ["vs_id1", "vs_id2", "vs_id3"]}
   ```

3. **Lister les fichiers d'un vector store spécifique**
   ```
   GET /vector_stores/vs_abc123/files
   ```

4. **Supprimer un fichier spécifique**
   ```
   DELETE /vector_stores/vs_abc123/files/file-abc123
   ```

### Exemple de réponse pour List Vector Stores

```json
{
  "object": "list",
  "data": [
    {
      "id": "vs_abc123",
      "object": "vector_store",
      "created_at": 1699061776,
      "name": "Support FAQ",
      "description": "Contains commonly asked questions",
      "bytes": 139920,
      "file_counts": {
        "in_progress": 0,
        "completed": 3,
        "failed": 0,
        "cancelled": 0,
        "total": 3
      }
    }
  ],
  "first_id": "vs_abc123",
  "last_id": "vs_abc123",
  "has_more": false
}
```

### Exemple de réponse pour Bulk Delete

```json
{
  "success": ["vs_abc123", "vs_def456"],
  "failed": [
    {
      "id": "vs_ghi789",
      "error": "{\"error\":{\"message\":\"No such vector store\"}}",
      "status_code": 404
    }
  ]
}
```

## Notes importantes

- **Sécurité**: Ne partagez jamais votre clé API OpenAI publiquement
- **Suppression en masse**: Le endpoint DELETE /vector_stores accepte un array d'IDs et retourne les succès ET les échecs
- **Suppression de fichiers**: La suppression d'un fichier du vector store ne supprime pas le fichier lui-même de votre compte OpenAI
- **Rate limiting**: Respectez les limites de taux de l'API OpenAI
- **Erreurs**: L'API retournera des codes d'erreur HTTP appropriés en cas de problème

## Structure du projet

```
.
├── vector_store_api.py       # Code principal de l'API (v2.0)
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
├── POSTMAN_GUIDE_V2.md       # Guide détaillé pour Postman
├── CURL_EXAMPLES.md          # Exemples de requêtes cURL
└── openai_api_notes.md       # Notes sur la documentation OpenAI
```

## Codes d'erreur possibles

- `400`: Requête invalide
- `401`: Clé API invalide ou manquante
- `404`: Vector store ou fichier non trouvé
- `422`: Validation échouée (header manquant, body invalide, etc.)
- `500`: Erreur serveur

## Support

Pour plus d'informations sur l'API OpenAI Vector Stores, consultez:
- https://platform.openai.com/docs/api-reference/vector-stores
- https://platform.openai.com/docs/api-reference/vector-stores-files

## Changelog

### Version 2.0
- ✅ Ajout de `GET /vector_stores` pour lister tous les vector stores
- ✅ Ajout de `DELETE /vector_stores` pour suppression en masse
- ✅ Amélioration de la gestion des erreurs
- ✅ Documentation enrichie

### Version 1.0
- ✅ `GET /vector_stores/{id}/files` - Lister les fichiers
- ✅ `DELETE /vector_stores/{id}/files/{file_id}` - Supprimer un fichier

