# Guide de Déploiement Permanent

Votre API est maintenant disponible sur GitHub et prête à être déployée de façon permanente.

## 📦 Dépôt GitHub

**URL:** https://github.com/LeonardoDiCarpaccio/openai-vector-store-api

Le code source complet est maintenant versionné et accessible publiquement.

---

## 🚀 Options de Déploiement Gratuit

### Option 1: Render.com (Recommandé) ⭐

**Avantages:**
- ✅ Gratuit (750 heures/mois)
- ✅ Déploiement automatique depuis GitHub
- ✅ HTTPS inclus
- ✅ Logs en temps réel
- ✅ Redémarrage automatique

**Étapes:**

1. **Créer un compte sur Render.com**
   - Allez sur https://render.com
   - Inscrivez-vous avec votre compte GitHub

2. **Créer un nouveau Web Service**
   - Cliquez sur "New +" → "Web Service"
   - Connectez votre dépôt GitHub: `openai-vector-store-api`

3. **Configuration du service**
   - **Name:** `openai-vector-store-api`
   - **Region:** Choisissez la région la plus proche
   - **Branch:** `master`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn vector_store_api:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

4. **Déployer**
   - Cliquez sur "Create Web Service"
   - Attendez 2-3 minutes pour le déploiement

5. **Obtenir votre URL**
   - Render vous donnera une URL permanente comme:
   - `https://openai-vector-store-api.onrender.com`

---

### Option 2: Railway.app

**Avantages:**
- ✅ Gratuit (500 heures/mois)
- ✅ Déploiement ultra-rapide
- ✅ HTTPS inclus

**Étapes:**

1. Allez sur https://railway.app
2. Connectez-vous avec GitHub
3. Cliquez sur "New Project" → "Deploy from GitHub repo"
4. Sélectionnez `openai-vector-store-api`
5. Railway détecte automatiquement Python et déploie
6. Obtenez votre URL dans les settings

---

### Option 3: Fly.io

**Avantages:**
- ✅ Gratuit (3 petites VMs)
- ✅ Déploiement global
- ✅ Très rapide

**Étapes:**

1. Installez Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Connectez-vous:
   ```bash
   flyctl auth login
   ```

3. Déployez:
   ```bash
   cd /home/ubuntu
   flyctl launch
   flyctl deploy
   ```

---

### Option 4: Vercel (Alternative)

**Note:** Vercel est optimisé pour les sites statiques, mais peut héberger des APIs Python avec quelques configurations supplémentaires.

---

## 🎯 Recommandation

**Je recommande Render.com** pour les raisons suivantes:

1. **Simplicité:** Configuration en 5 minutes
2. **Fiabilité:** Service stable et reconnu
3. **Gratuit:** Plan gratuit généreux
4. **Auto-deploy:** Chaque push sur GitHub redéploie automatiquement
5. **Logs:** Interface web pour voir les logs en temps réel

---

## 📝 Après le Déploiement

Une fois déployé sur Render (ou autre), vous obtiendrez une URL permanente comme:

```
https://openai-vector-store-api.onrender.com
```

### Utilisation avec Postman

Remplacez simplement l'URL temporaire par la nouvelle URL permanente:

**Avant:**
```
https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores
```

**Après:**
```
https://openai-vector-store-api.onrender.com/vector_stores
```

### Endpoints disponibles

- `GET https://votre-url.onrender.com/vector_stores`
- `DELETE https://votre-url.onrender.com/vector_stores`
- `GET https://votre-url.onrender.com/vector_stores/{id}/files`
- `DELETE https://votre-url.onrender.com/vector_stores/{id}/files/{file_id}`
- `GET https://votre-url.onrender.com/docs` (Documentation interactive)

---

## 🔄 Mises à Jour Automatiques

Avec Render.com configuré:

1. Modifiez le code localement
2. Faites un commit: `git commit -am "Update"`
3. Push sur GitHub: `git push origin master`
4. Render redéploie automatiquement ! ✨

---

## 🛡️ Sécurité

**Important:** 
- Ne committez JAMAIS votre clé API OpenAI dans le code
- L'API actuelle demande la clé dans les headers (sécurisé)
- Les utilisateurs passent leur propre clé API

---

## 📊 Monitoring

Sur Render.com, vous pouvez:
- Voir les logs en temps réel
- Monitorer l'utilisation CPU/RAM
- Voir les requêtes HTTP
- Configurer des alertes

---

## 💰 Coûts

**Plan Gratuit Render.com:**
- 750 heures/mois (suffisant pour un usage continu)
- 512 MB RAM
- Partage de CPU
- HTTPS gratuit
- Pas de carte de crédit requise

**Note:** Le service peut s'endormir après 15 minutes d'inactivité (plan gratuit). La première requête après inactivité prendra ~30 secondes pour réveiller le service.

---

## 🎉 Résumé

Votre API est maintenant:
- ✅ Versionnée sur GitHub
- ✅ Prête pour le déploiement permanent
- ✅ Documentée
- ✅ Testée

**Prochaine étape:** Déployez sur Render.com en suivant les étapes ci-dessus !

