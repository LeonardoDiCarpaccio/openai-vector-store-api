# 🚀 Déploiement en Un Clic

## Déployer sur Render.com (Gratuit)

Cliquez sur le bouton ci-dessous pour déployer automatiquement votre API sur Render.com :

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/LeonardoDiCarpaccio/openai-vector-store-api)

---

## Ou déployez manuellement :

### 1. Créer un compte Render

Allez sur https://render.com et créez un compte gratuit avec GitHub.

### 2. Nouveau Web Service

1. Cliquez sur **"New +"** → **"Web Service"**
2. Connectez votre dépôt GitHub
3. Cherchez et sélectionnez : `LeonardoDiCarpaccio/openai-vector-store-api`

### 3. Configuration

Render détectera automatiquement le fichier `render.yaml` et configurera tout pour vous !

Si vous devez configurer manuellement :

- **Name:** `openai-vector-store-api`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn vector_store_api:app --host 0.0.0.0 --port $PORT`
- **Plan:** `Free`

### 4. Déployer

Cliquez sur **"Create Web Service"** et attendez 2-3 minutes.

### 5. Obtenir votre URL

Une fois déployé, Render vous donnera une URL permanente comme :

```
https://openai-vector-store-api.onrender.com
```

---

## ✅ Vérification

Testez votre API déployée :

```bash
curl https://votre-url.onrender.com/
```

Vous devriez voir :

```json
{
  "message": "API OpenAI Vector Store Management",
  "version": "2.0.0",
  "endpoints": { ... }
}
```

---

## 📖 Documentation Interactive

Une fois déployé, accédez à la documentation Swagger :

```
https://votre-url.onrender.com/docs
```

---

## 🎯 Utilisation avec Postman

Remplacez l'URL temporaire par votre nouvelle URL permanente :

**Endpoint 1 - Liste des IDs :**
```
GET https://votre-url.onrender.com/vector_stores
Header: x-openai-api-key: sk-votre_clé
```

**Endpoint 2 - Suppression en masse :**
```
DELETE https://votre-url.onrender.com/vector_stores
Header: x-openai-api-key: sk-votre_clé
Header: Content-Type: application/json
Body: {"vector_store_ids": ["vs_id1", "vs_id2"]}
```

---

## 🔄 Mises à Jour Automatiques

Chaque fois que vous poussez du code sur GitHub, Render redéploie automatiquement !

```bash
git add .
git commit -m "Update API"
git push origin master
```

Render détecte le push et redéploie en 1-2 minutes. ✨

---

## 💡 Astuce

Le plan gratuit de Render peut mettre le service en veille après 15 minutes d'inactivité. La première requête après inactivité prendra ~30 secondes pour réveiller le service.

Pour un service toujours actif 24/7, vous pouvez :
- Passer au plan payant ($7/mois)
- Utiliser un service de "ping" gratuit comme UptimeRobot pour garder l'API active

---

## 🎉 C'est tout !

Votre API est maintenant déployée de façon permanente et accessible depuis n'importe où dans le monde ! 🌍

