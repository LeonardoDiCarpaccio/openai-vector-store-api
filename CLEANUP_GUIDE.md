# 🧹 Guide de Nettoyage - Fichiers Orphelins

## ⚠️ Problème

Quand vous supprimez des vector stores avec `DELETE /vector_stores`, les **fichiers à l'intérieur ne sont PAS supprimés automatiquement** ! Ils restent dans votre compte OpenAI et continuent à occuper de l'espace.

---

## ✅ Solution 1: Nettoyer TOUS les fichiers restants (Simple)

Si vous avez déjà supprimé les vector stores et que vous voulez nettoyer tous les fichiers orphelins :

### Étape 1: Lister tous les fichiers

```bash
GET http://localhost:8000/files

Headers:
  x-openai-api-key: sk-votre_clé
```

**Réponse:**
```json
[
  "file-abc123",
  "file-def456",
  "file-ghi789"
]
```

### Étape 2: Supprimer tous les fichiers

```bash
DELETE http://localhost:8000/files

Headers:
  x-openai-api-key: sk-votre_clé
  Content-Type: application/json

Body:
{
  "file_ids": ["file-abc123", "file-def456", "file-ghi789"]
}
```

**Réponse:**
```json
{
  "success": ["file-abc123", "file-def456", "file-ghi789"],
  "failed": []
}
```

---

## ✅ Solution 2: Supprimer Vector Stores ET Fichiers en une fois (Recommandé)

Si vous n'avez PAS encore supprimé les vector stores, utilisez le nouvel endpoint :

### Endpoint: DELETE /vector_stores/with-files ⚡

Cet endpoint fait tout automatiquement :
1. Liste tous les fichiers de chaque vector store
2. Supprime les vector stores
3. Supprime tous les fichiers trouvés

**Requête:**
```bash
DELETE http://localhost:8000/vector_stores/with-files

Headers:
  x-openai-api-key: sk-votre_clé
  Content-Type: application/json

Body:
{
  "vector_store_ids": ["vs_abc123", "vs_def456"],
  "delete_files": true
}
```

**Réponse:**
```json
{
  "vector_stores_deleted": ["vs_abc123", "vs_def456"],
  "vector_stores_failed": [],
  "files_deleted": ["file-abc123", "file-def456", "file-ghi789"],
  "files_failed": [],
  "total_files_found": 3
}
```

---

## 🔥 Workflow Complet: Nettoyage Total

### Scénario A: Vector stores déjà supprimés

```bash
# 1. Lister tous les fichiers orphelins
GET /files
→ ["file-1", "file-2", "file-3", ...]

# 2. Supprimer tous les fichiers
DELETE /files
Body: {"file_ids": ["file-1", "file-2", "file-3", ...]}
```

### Scénario B: Vector stores encore présents

```bash
# 1. Lister tous les vector stores
GET /vector_stores
→ ["vs-1", "vs-2", "vs-3", ...]

# 2. Supprimer vector stores ET leurs fichiers en une fois
DELETE /vector_stores/with-files
Body: {
  "vector_store_ids": ["vs-1", "vs-2", "vs-3", ...],
  "delete_files": true
}
```

---

## 📱 Exemples Postman

### Nettoyer tous les fichiers orphelins

**Requête 1: Liste**
```
GET {{base_url}}/files
Headers: x-openai-api-key: {{api_key}}
```

**Requête 2: Suppression**
```
DELETE {{base_url}}/files
Headers: 
  x-openai-api-key: {{api_key}}
  Content-Type: application/json
Body (raw JSON):
{
  "file_ids": [COLLER_ICI_L_ARRAY_DE_LA_REQUETE_1]
}
```

### Supprimer vector stores avec fichiers

```
DELETE {{base_url}}/vector_stores/with-files
Headers: 
  x-openai-api-key: {{api_key}}
  Content-Type: application/json
Body (raw JSON):
{
  "vector_store_ids": ["vs_id1", "vs_id2"],
  "delete_files": true
}
```

---

## 💡 Conseils

### Option delete_files

Le paramètre `delete_files` dans `/vector_stores/with-files` peut être :
- `true` (défaut) : Supprime les fichiers
- `false` : Garde les fichiers (pour les réutiliser ailleurs)

**Exemple sans supprimer les fichiers:**
```json
{
  "vector_store_ids": ["vs_abc123"],
  "delete_files": false
}
```

### Filtrer par purpose

Si vous voulez supprimer seulement certains types de fichiers :

```bash
# Lister seulement les fichiers "assistants"
GET /files?purpose=assistants

# Lister seulement les fichiers "fine-tune"
GET /files?purpose=fine-tune
```

---

## 📊 Comparaison des Méthodes

| Méthode | Quand l'utiliser | Avantages | Inconvénients |
|---------|------------------|-----------|---------------|
| `DELETE /vector_stores` | Vector stores seulement | Simple | Laisse les fichiers orphelins |
| `DELETE /vector_stores/with-files` | Nettoyage complet | Tout en une fois | Nécessite que les VS existent encore |
| `DELETE /files` | Fichiers orphelins | Nettoie tout | Nécessite de lister d'abord |

---

## ⚠️ Avertissement

**La suppression de fichiers est DÉFINITIVE et IRRÉVERSIBLE !**

Assurez-vous de :
- ✅ Avoir une sauvegarde si nécessaire
- ✅ Vérifier la liste des fichiers avant suppression
- ✅ Utiliser le bon endpoint selon votre situation

---

## 🎯 Cas d'Usage Réels

### Cas 1: J'ai supprimé mes vector stores mais les fichiers sont toujours là

```bash
# Solution rapide
GET /files
DELETE /files (avec tous les IDs)
```

### Cas 2: Je veux tout nettoyer d'un coup

```bash
# Si vector stores existent encore
GET /vector_stores
DELETE /vector_stores/with-files (avec tous les IDs et delete_files=true)

# Sinon
GET /files
DELETE /files (avec tous les IDs)
```

### Cas 3: Je veux garder certains fichiers

```bash
# 1. Lister tous les fichiers
GET /files

# 2. Identifier ceux à garder manuellement

# 3. Supprimer seulement les autres
DELETE /files (avec les IDs à supprimer)
```

---

## 🚀 Résumé

**Pour votre cas (vector stores déjà supprimés) :**

1. Utilisez `GET /files` pour lister tous les fichiers orphelins
2. Utilisez `DELETE /files` avec l'array complet pour tout nettoyer

**Pour la prochaine fois :**

Utilisez `DELETE /vector_stores/with-files` pour tout supprimer en une seule requête ! ⚡

---

## 📝 Logs

Tous les endpoints affichent des logs détaillés :

```
📋 Endpoint appelé: DELETE /vector_stores/with-files
🗑️  Nombre de vector stores à supprimer: 2
📁 Supprimer les fichiers: true

🔄 Étape 1: Collecte des fichiers des vector stores...
📂 Récupération des fichiers de: vs_abc123
  📦 3 fichiers trouvés dans vs_abc123
✅ Total de fichiers uniques trouvés: 3

🔄 Étape 2: Suppression des vector stores...
🗑️  [1/2] Suppression de: vs_abc123
✅ Supprimé avec succès: vs_abc123

🔄 Étape 3: Suppression des fichiers...
🗑️  [1/3] Suppression de: file-abc123
✅ Fichier supprimé: file-abc123

📊 Résumé:
  🗄️ Vector Stores:
    ✅ Succès: 2
    ❌ Échecs: 0
  📁 Fichiers:
    🔍 Trouvés: 3
    ✅ Supprimés: 3
    ❌ Échecs: 0
```

Vous pouvez suivre toute l'opération en temps réel ! 🎉

