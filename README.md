# 🚀 OpenAI Vector Store Management API

API REST complète pour gérer vos vector stores et fichiers OpenAI. Passez votre clé API en paramètre et gérez facilement vos ressources depuis Postman ou n'importe quel client HTTP.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/LeonardoDiCarpaccio/openai-vector-store-api)

---

## ✨ Fonctionnalités

- ✅ **Liste tous les vector stores** - Retourne un array simple d'IDs
- ✅ **Suppression en masse** - Supprimez plusieurs vector stores en une requête
- ✅ **Gestion des fichiers** - Listez et supprimez les fichiers de vos vector stores
- ✅ **Pagination automatique** - Récupère tous les résultats automatiquement
- ✅ **Documentation interactive** - Swagger UI intégré
- ✅ **Gestion d'erreurs** - Rapports détaillés des succès et échecs

---

## 🎯 Endpoints

### 1. GET /vector_stores
Retourne un array de tous les IDs de vector stores de votre compte.

**Réponse :**
```json
[
  "vs_68f61de174e08191991f7b341db64921",
  "vs_68f61d408d488191a8251dd627526adc",
  "vs_68f61c61aa208191a28f0fe2bd7cfe7d"
]
```

### 2. DELETE /vector_stores
Supprime plusieurs vector stores en une seule requête.

**Body :**
```json
{
  "vector_store_ids": ["vs_id1", "vs_id2", "vs_id3"]
}
```

**Réponse :**
```json
{
  "success": ["vs_id1", "vs_id2"],
  "failed": [
    {
      "id": "vs_id3",
      "error": "...",
      "status_code": 404
    }
  ]
}
```

### 3. GET /vector_stores/{id}/files
Liste tous les fichiers d'un vector store.

### 4. DELETE /vector_stores/{id}/files/{file_id}
Supprime un fichier d'un vector store.

---

## 🚀 Déploiement

### Option 1 : Déploiement en un clic sur Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/LeonardoDiCarpaccio/openai-vector-store-api)

### Option 2 : Déploiement manuel

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/LeonardoDiCarpaccio/openai-vector-store-api.git
   cd openai-vector-store-api
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer le serveur**
   ```bash
   uvicorn vector_store_api:app --host 0.0.0.0 --port 8000
   ```

4. **Accéder à la documentation**
   ```
   http://localhost:8000/docs
   ```

---

## 📖 Utilisation avec Postman

### Configuration de base

Pour toutes les requêtes, ajoutez le header :
- **Key:** `x-openai-api-key`
- **Value:** `sk-votre_clé_openai`

### Workflow typique

**1. Lister tous les vector stores**
```
GET https://votre-api.onrender.com/vector_stores
Header: x-openai-api-key: sk-votre_clé
```

**2. Supprimer plusieurs vector stores**
```
DELETE https://votre-api.onrender.com/vector_stores
Header: x-openai-api-key: sk-votre_clé
Header: Content-Type: application/json
Body: {"vector_store_ids": ["vs_id1", "vs_id2"]}
```

---

## 🛠️ Technologies

- **FastAPI** - Framework web moderne et rapide
- **Uvicorn** - Serveur ASGI haute performance
- **Requests** - Client HTTP pour appeler l'API OpenAI
- **Pydantic** - Validation des données

---

## 📝 Documentation

- [Guide de déploiement complet](DEPLOYMENT_GUIDE.md)
- [Guide de déploiement rapide](DEPLOY_NOW.md)
- [Guide Postman détaillé](POSTMAN_GUIDE_FINAL.md)
- [Exemples cURL](CURL_EXAMPLES.md)

---

## 🔒 Sécurité

- ✅ La clé API OpenAI est passée dans les headers (jamais dans l'URL)
- ✅ Pas de stockage de clés API
- ✅ Chaque utilisateur utilise sa propre clé
- ✅ HTTPS automatique avec Render

---

## 💰 Coûts

**Gratuit** avec Render.com :
- 750 heures/mois
- HTTPS inclus
- Déploiement automatique depuis GitHub
- Pas de carte de crédit requise

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

---

## 📄 Licence

MIT License - Utilisez librement ce projet.

---

## 🎉 Auteur

Créé pour simplifier la gestion des vector stores OpenAI.

---

## 🔗 Liens utiles

- [Documentation OpenAI Vector Stores](https://platform.openai.com/docs/api-reference/vector-stores)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Render.com](https://render.com)

---

## ⭐ Support

Si ce projet vous aide, n'hésitez pas à lui donner une étoile sur GitHub ! ⭐

