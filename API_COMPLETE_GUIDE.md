# 📚 Guide Complet de l'API - Version 3.0

## 🎉 Nouveautés Version 3.0

L'API gère maintenant **TOUS les fichiers** de votre compte OpenAI, pas seulement ceux dans les vector stores !

### ✨ Nouveaux Endpoints

- ✅ **GET /files** - Liste tous les fichiers de votre compte
- ✅ **DELETE /files** - Supprime plusieurs fichiers en une seule requête

---

## 📋 Tous les Endpoints Disponibles

### 🗂️ Gestion des Vector Stores

#### 1. GET /vector_stores
Liste tous les IDs des vector stores de votre compte.

**URL:** `http://localhost:8000/vector_stores`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI

**Réponse:**
```json
[
  "vs_abc123",
  "vs_def456",
  "vs_ghi789"
]
```

---

#### 2. DELETE /vector_stores
Supprime plusieurs vector stores en une seule requête.

**URL:** `http://localhost:8000/vector_stores`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI
- `Content-Type`: application/json

**Body:**
```json
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

#### 3. GET /vector_stores/{vector_store_id}/files
Liste tous les fichiers d'un vector store spécifique.

**URL:** `http://localhost:8000/vector_stores/vs_abc123/files`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI

---

#### 4. DELETE /vector_stores/{vector_store_id}/files/{file_id}
Supprime un fichier d'un vector store.

**URL:** `http://localhost:8000/vector_stores/vs_abc123/files/file-xyz789`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI

---

### 📁 Gestion de TOUS les Fichiers (NOUVEAU !)

#### 5. GET /files ⭐ NOUVEAU
Liste tous les IDs des fichiers de votre compte OpenAI.

**URL:** `http://localhost:8000/files`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI

**Paramètres optionnels:**
- `limit` (integer): Nombre max de résultats (défaut: 10000)
- `order` (string): Ordre de tri - `asc` ou `desc` (défaut: desc)
- `purpose` (string): Filtrer par purpose - `assistants`, `fine-tune`, `batch`, etc.

**Exemple avec filtres:**
```
GET http://localhost:8000/files?purpose=assistants&limit=100
```

**Réponse:**
```json
[
  "file-abc123",
  "file-def456",
  "file-ghi789",
  "file-jkl012"
]
```

---

#### 6. DELETE /files ⭐ NOUVEAU
Supprime plusieurs fichiers en une seule requête.

**⚠️ IMPORTANT:** Supprimer un fichier le retire automatiquement de **TOUS** les vector stores où il est utilisé !

**URL:** `http://localhost:8000/files`

**Headers:**
- `x-openai-api-key`: Votre clé API OpenAI
- `Content-Type`: application/json

**Body:**
```json
{
  "file_ids": ["file-abc123", "file-def456", "file-ghi789"]
}
```

**Réponse:**
```json
{
  "success": ["file-abc123", "file-def456"],
  "failed": [
    {
      "id": "file-ghi789",
      "error": "File not found",
      "status_code": 404
    }
  ]
}
```

---

## 🔥 Workflows Complets

### Workflow 1: Nettoyer tous les vector stores

```bash
# 1. Lister tous les vector stores
GET /vector_stores

# 2. Supprimer tous les vector stores
DELETE /vector_stores
Body: {"vector_store_ids": [array_reçu_de_l_étape_1]}
```

---

### Workflow 2: Nettoyer tous les fichiers

```bash
# 1. Lister tous les fichiers
GET /files

# 2. Supprimer tous les fichiers
DELETE /files
Body: {"file_ids": [array_reçu_de_l_étape_1]}
```

**Note:** Cela supprime aussi les fichiers des vector stores automatiquement !

---

### Workflow 3: Nettoyer seulement les fichiers "assistants"

```bash
# 1. Lister tous les fichiers avec purpose=assistants
GET /files?purpose=assistants

# 2. Supprimer ces fichiers
DELETE /files
Body: {"file_ids": [array_reçu_de_l_étape_1]}
```

---

### Workflow 4: Nettoyer un vector store et ses fichiers

```bash
# 1. Lister les fichiers du vector store
GET /vector_stores/vs_abc123/files

# 2. Extraire les IDs des fichiers de la réponse

# 3. Supprimer le vector store
DELETE /vector_stores
Body: {"vector_store_ids": ["vs_abc123"]}

# 4. Supprimer les fichiers (optionnel, si vous voulez les supprimer complètement)
DELETE /files
Body: {"file_ids": [array_des_file_ids]}
```

---

## 📱 Exemples Postman

### Collection Postman Mise à Jour

#### Variables
- `base_url`: `http://localhost:8000`
- `api_key`: `sk-votre_clé_openai`

#### Requête 1: Liste tous les fichiers
```
GET {{base_url}}/files
Headers:
  x-openai-api-key: {{api_key}}
```

#### Requête 2: Liste les fichiers "assistants"
```
GET {{base_url}}/files?purpose=assistants
Headers:
  x-openai-api-key: {{api_key}}
```

#### Requête 3: Supprime plusieurs fichiers
```
DELETE {{base_url}}/files
Headers:
  x-openai-api-key: {{api_key}}
  Content-Type: application/json
Body (raw JSON):
{
  "file_ids": ["file-abc123", "file-def456"]
}
```

---

## 💡 Différences Importantes

### Vector Store Files vs Files

| Aspect | Vector Store Files | Files |
|--------|-------------------|-------|
| Endpoint | `/vector_stores/{id}/files` | `/files` |
| Scope | Fichiers d'un vector store spécifique | TOUS les fichiers du compte |
| Suppression | Retire le fichier du vector store | Supprime le fichier ET le retire de tous les vector stores |
| Purpose | Toujours `assistants` | Peut être `assistants`, `fine-tune`, `batch`, etc. |

### Quand utiliser quoi ?

**Utilisez `/vector_stores/{id}/files`** quand :
- Vous voulez voir les fichiers d'un vector store spécifique
- Vous voulez retirer un fichier d'un vector store sans le supprimer

**Utilisez `/files`** quand :
- Vous voulez voir TOUS vos fichiers
- Vous voulez supprimer définitivement des fichiers
- Vous voulez filtrer par `purpose`
- Vous voulez nettoyer votre compte

---

## ⚠️ Avertissements Importants

### Suppression de Fichiers

**DELETE /files** supprime **définitivement** les fichiers ET les retire de **TOUS** les vector stores.

**DELETE /vector_stores/{id}/files/{file_id}** retire seulement le fichier du vector store, mais ne supprime pas le fichier lui-même.

### Exemple

```bash
# Scénario: file-abc123 est dans vs_store1 et vs_store2

# Option A: Retirer de vs_store1 seulement
DELETE /vector_stores/vs_store1/files/file-abc123
# Résultat: file-abc123 existe toujours et est toujours dans vs_store2

# Option B: Supprimer complètement
DELETE /files
Body: {"file_ids": ["file-abc123"]}
# Résultat: file-abc123 est supprimé ET retiré de vs_store1 ET vs_store2
```

---

## 🎯 Cas d'Usage Réels

### Cas 1: Nettoyer tout le compte

```bash
# 1. Supprimer tous les vector stores
GET /vector_stores
DELETE /vector_stores (avec tous les IDs)

# 2. Supprimer tous les fichiers
GET /files
DELETE /files (avec tous les IDs)
```

### Cas 2: Nettoyer seulement les fichiers inutilisés

```bash
# 1. Lister tous les fichiers
GET /files

# 2. Lister tous les vector stores
GET /vector_stores

# 3. Pour chaque vector store, lister ses fichiers
GET /vector_stores/{id}/files

# 4. Comparer et identifier les fichiers non utilisés

# 5. Supprimer les fichiers non utilisés
DELETE /files (avec les IDs non utilisés)
```

### Cas 3: Migrer vers de nouveaux vector stores

```bash
# 1. Créer de nouveaux vector stores (via OpenAI API)

# 2. Uploader de nouveaux fichiers

# 3. Supprimer les anciens vector stores
DELETE /vector_stores (avec les anciens IDs)

# 4. Supprimer les anciens fichiers
DELETE /files (avec les anciens file IDs)
```

---

## 📊 Résumé des Endpoints

| Méthode | Endpoint | Description | Retour |
|---------|----------|-------------|--------|
| GET | `/vector_stores` | Liste vector stores | Array d'IDs |
| DELETE | `/vector_stores` | Supprime vector stores | Succès/Échecs |
| GET | `/vector_stores/{id}/files` | Liste fichiers d'un VS | Objet complet |
| DELETE | `/vector_stores/{id}/files/{file_id}` | Retire fichier d'un VS | Statut |
| GET | `/files` | Liste TOUS les fichiers | Array d'IDs |
| DELETE | `/files` | Supprime fichiers | Succès/Échecs |

---

## 🚀 Documentation Interactive

Une fois le serveur lancé, accédez à :

**Swagger UI:** http://localhost:8000/docs

Vous pouvez tester tous les endpoints directement depuis votre navigateur !

---

## ✨ Version 3.0 - Résumé

- ✅ Gestion complète des vector stores
- ✅ Gestion complète des fichiers
- ✅ Suppression en masse
- ✅ Filtrage par purpose
- ✅ Pagination automatique
- ✅ Logs détaillés
- ✅ Gestion d'erreurs robuste

**Tout ce dont vous avez besoin pour gérer votre compte OpenAI ! 🎉**

