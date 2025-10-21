# 📊 Guide des Logs

L'API inclut maintenant un système de logs détaillé pour tracer toutes les opérations.

---

## 🎯 Types de Logs

### ✅ Logs de Succès (INFO)

Ces logs indiquent que tout fonctionne correctement :

```
2025-10-21 03:33:36 - __main__ - INFO - 🚀 OpenAI Vector Store Management API - Démarrage
2025-10-21 03:33:36 - __main__ - INFO - 📍 Endpoint appelé: GET /vector_stores
2025-10-21 03:33:36 - __main__ - INFO - ✅ Total récupéré: 15 vector stores
```

### ❌ Logs d'Erreur (ERROR)

Ces logs indiquent un problème :

```
2025-10-21 03:33:36 - __main__ - ERROR - ❌ Erreur OpenAI API: 401
2025-10-21 03:33:36 - __main__ - ERROR - ❌ Détails: Invalid API key
```

---

## 📋 Logs par Endpoint

### 1. GET / (Root)

```
2025-10-21 03:33:46 - __main__ - INFO - 📍 Endpoint appelé: GET /
2025-10-21 03:33:46 - __main__ - INFO - ✅ Retour des informations de l'API
```

### 2. GET /vector_stores

**Logs de démarrage :**
```
2025-10-21 03:35:12 - __main__ - INFO - ============================================================
2025-10-21 03:35:12 - __main__ - INFO - 📍 Endpoint appelé: GET /vector_stores
2025-10-21 03:35:12 - __main__ - INFO - 📊 Paramètres: limit=100, order=desc, after=None, before=None
2025-10-21 03:35:12 - __main__ - INFO - 🔑 Clé API fournie: sk-proj-xxxxxxxxxxxxx...
2025-10-21 03:35:12 - __main__ - INFO - 🔄 Début de la récupération des vector stores...
```

**Logs de pagination :**
```
2025-10-21 03:35:12 - __main__ - INFO - 📄 Page 1: Appel API OpenAI...
2025-10-21 03:35:13 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:35:13 - __main__ - INFO - 📦 15 vector stores trouvés sur cette page
2025-10-21 03:35:13 - __main__ - INFO - 🔍 Plus de résultats disponibles: False
```

**Logs de fin :**
```
2025-10-21 03:35:13 - __main__ - INFO - ✅ Total récupéré: 15 vector stores
2025-10-21 03:35:13 - __main__ - INFO - 📊 Nombre de pages parcourues: 1
2025-10-21 03:35:13 - __main__ - INFO - ============================================================
```

### 3. DELETE /vector_stores

**Logs de démarrage :**
```
2025-10-21 03:36:20 - __main__ - INFO - ============================================================
2025-10-21 03:36:20 - __main__ - INFO - 📍 Endpoint appelé: DELETE /vector_stores
2025-10-21 03:36:20 - __main__ - INFO - 🗑️  Nombre de vector stores à supprimer: 3
2025-10-21 03:36:20 - __main__ - INFO - 📋 IDs: ['vs_abc123', 'vs_def456', 'vs_ghi789']
2025-10-21 03:36:20 - __main__ - INFO - 🔑 Clé API fournie: sk-proj-xxxxxxxxxxxxx...
2025-10-21 03:36:20 - __main__ - INFO - 🔄 Début de la suppression...
```

**Logs de suppression :**
```
2025-10-21 03:36:20 - __main__ - INFO - 🗑️  [1/3] Suppression de: vs_abc123
2025-10-21 03:36:21 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:36:21 - __main__ - INFO - ✅ Supprimé avec succès: vs_abc123

2025-10-21 03:36:21 - __main__ - INFO - 🗑️  [2/3] Suppression de: vs_def456
2025-10-21 03:36:22 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:36:22 - __main__ - INFO - ✅ Supprimé avec succès: vs_def456

2025-10-21 03:36:22 - __main__ - INFO - 🗑️  [3/3] Suppression de: vs_ghi789
2025-10-21 03:36:23 - __main__ - INFO - 📡 Réponse OpenAI: Status 404
2025-10-21 03:36:23 - __main__ - ERROR - ❌ Échec de suppression: vs_ghi789
2025-10-21 03:36:23 - __main__ - ERROR - ❌ Erreur: {"error":{"message":"No such vector store"}}
```

**Logs de résumé :**
```
2025-10-21 03:36:23 - __main__ - INFO - ============================================================
2025-10-21 03:36:23 - __main__ - INFO - 📊 Résumé de la suppression:
2025-10-21 03:36:23 - __main__ - INFO -   ✅ Succès: 2
2025-10-21 03:36:23 - __main__ - INFO -   ❌ Échecs: 1
2025-10-21 03:36:23 - __main__ - INFO - ============================================================
```

### 4. GET /vector_stores/{id}/files

```
2025-10-21 03:37:10 - __main__ - INFO - ============================================================
2025-10-21 03:37:10 - __main__ - INFO - 📍 Endpoint appelé: GET /vector_stores/vs_abc123/files
2025-10-21 03:37:10 - __main__ - INFO - 📊 Paramètres: limit=20, order=desc, filter=None
2025-10-21 03:37:10 - __main__ - INFO - 🔑 Clé API fournie: sk-proj-xxxxxxxxxxxxx...
2025-10-21 03:37:10 - __main__ - INFO - 🔄 Appel API OpenAI pour lister les fichiers...
2025-10-21 03:37:11 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:37:11 - __main__ - INFO - ✅ 5 fichiers trouvés
2025-10-21 03:37:11 - __main__ - INFO - ============================================================
```

### 5. DELETE /vector_stores/{id}/files/{file_id}

```
2025-10-21 03:38:05 - __main__ - INFO - ============================================================
2025-10-21 03:38:05 - __main__ - INFO - 📍 Endpoint appelé: DELETE /vector_stores/vs_abc123/files/file-xyz789
2025-10-21 03:38:05 - __main__ - INFO - 🗑️  Vector Store: vs_abc123
2025-10-21 03:38:05 - __main__ - INFO - 📄 Fichier: file-xyz789
2025-10-21 03:38:05 - __main__ - INFO - 🔑 Clé API fournie: sk-proj-xxxxxxxxxxxxx...
2025-10-21 03:38:05 - __main__ - INFO - 🔄 Appel API OpenAI pour supprimer le fichier...
2025-10-21 03:38:06 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:38:06 - __main__ - INFO - ✅ Fichier supprimé avec succès: file-xyz789
2025-10-21 03:38:06 - __main__ - INFO - ============================================================
```

---

## 🔍 Comment Voir les Logs

### Option 1 : Dans le Terminal

Les logs s'affichent automatiquement dans le terminal où vous avez lancé le serveur.

### Option 2 : Suivre les Logs en Temps Réel

**Linux / Mac :**
```bash
tail -f api.log
```

**Windows (PowerShell) :**
```powershell
Get-Content api.log -Wait
```

### Option 3 : Voir les Derniers Logs

```bash
tail -50 api.log
```

---

## 🎨 Signification des Émojis

| Émoji | Signification |
|-------|---------------|
| 🚀 | Démarrage / Lancement |
| 📍 | Endpoint appelé |
| 🔑 | Clé API |
| 📊 | Statistiques / Paramètres |
| 🔄 | Opération en cours |
| 📡 | Réponse API |
| ✅ | Succès |
| ❌ | Erreur |
| 📦 | Données reçues |
| 🗑️ | Suppression |
| 📄 | Page / Fichier |
| 🔍 | Recherche / Vérification |
| ➡️ | Pagination |
| 📁 | Fichiers |
| 🛑 | Arrêt |

---

## 🐛 Déboguer avec les Logs

### Problème : Pas de réponse de l'API

**Cherchez dans les logs :**
```
❌ Erreur de connexion
```

**Solution :** Vérifiez votre connexion internet.

### Problème : Erreur 401

**Cherchez dans les logs :**
```
❌ Erreur OpenAI API: 401
❌ Détails: Invalid API key
```

**Solution :** Vérifiez que votre clé API OpenAI est correcte.

### Problème : Erreur 404

**Cherchez dans les logs :**
```
❌ Erreur OpenAI API: 404
❌ Détails: No such vector store
```

**Solution :** Le vector store n'existe pas ou a déjà été supprimé.

### Problème : Aucun vector store trouvé

**Cherchez dans les logs :**
```
✅ Total récupéré: 0 vector stores
```

**Solution :** Votre compte n'a pas de vector stores, ou la clé API n'a pas accès à ce projet.

---

## 📝 Niveaux de Logs

### INFO (par défaut)

Affiche toutes les opérations normales.

### DEBUG (détaillé)

Pour activer les logs DEBUG, modifiez `vector_store_api.py` :

```python
logging.basicConfig(
    level=logging.DEBUG,  # Changez INFO en DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

Cela affichera chaque ID de vector store récupéré :

```
2025-10-21 03:35:13 - __main__ - DEBUG -   ✓ vs_abc123
2025-10-21 03:35:13 - __main__ - DEBUG -   ✓ vs_def456
2025-10-21 03:35:13 - __main__ - DEBUG -   ✓ vs_ghi789
```

---

## 💡 Astuces

### Sauvegarder les Logs dans un Fichier

Au lieu de `python vector_store_api.py`, utilisez :

```bash
python vector_store_api.py > api.log 2>&1
```

Tous les logs seront sauvegardés dans `api.log`.

### Filtrer les Logs

**Voir seulement les erreurs :**
```bash
grep "ERROR" api.log
```

**Voir seulement les succès :**
```bash
grep "✅" api.log
```

**Voir les appels d'endpoints :**
```bash
grep "📍 Endpoint" api.log
```

---

## 🎯 Exemple Complet de Logs

Voici à quoi ressemblent les logs pour une session complète :

```
2025-10-21 03:33:36 - __main__ - INFO - ============================================================
2025-10-21 03:33:36 - __main__ - INFO - 🚀 OpenAI Vector Store Management API - Démarrage
2025-10-21 03:33:36 - __main__ - INFO - ============================================================
2025-10-21 03:33:36 - __main__ - INFO - 📅 Date: 2025-10-21 03:33:36
2025-10-21 03:33:36 - __main__ - INFO - 🌐 Base URL OpenAI: https://api.openai.com/v1
2025-10-21 03:33:36 - __main__ - INFO - 📖 Documentation: http://localhost:8000/docs
2025-10-21 03:33:36 - __main__ - INFO - ============================================================
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

2025-10-21 03:35:12 - __main__ - INFO - ============================================================
2025-10-21 03:35:12 - __main__ - INFO - 📍 Endpoint appelé: GET /vector_stores
2025-10-21 03:35:12 - __main__ - INFO - 📊 Paramètres: limit=100, order=desc, after=None, before=None
2025-10-21 03:35:12 - __main__ - INFO - 🔑 Clé API fournie: sk-proj-xxxxxxxxxxxxx...
2025-10-21 03:35:12 - __main__ - INFO - 🔄 Début de la récupération des vector stores...
2025-10-21 03:35:12 - __main__ - INFO - 📄 Page 1: Appel API OpenAI...
2025-10-21 03:35:13 - __main__ - INFO - 📡 Réponse OpenAI: Status 200
2025-10-21 03:35:13 - __main__ - INFO - 📦 15 vector stores trouvés sur cette page
2025-10-21 03:35:13 - __main__ - INFO - 🔍 Plus de résultats disponibles: False
2025-10-21 03:35:13 - __main__ - INFO - ✅ Total récupéré: 15 vector stores
2025-10-21 03:35:13 - __main__ - INFO - 📊 Nombre de pages parcourues: 1
2025-10-21 03:35:13 - __main__ - INFO - ============================================================
INFO:     127.0.0.1:52996 - "GET /vector_stores HTTP/1.1" 200 OK
```

---

## ✅ Vérification Rapide

Pour vérifier que les logs fonctionnent :

1. Lancez le serveur
2. Appelez `http://localhost:8000/`
3. Vous devriez voir dans les logs :

```
📍 Endpoint appelé: GET /
✅ Retour des informations de l'API
```

Si vous voyez ces logs, tout fonctionne parfaitement ! 🎉

