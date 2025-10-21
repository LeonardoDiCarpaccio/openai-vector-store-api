# Guide d'utilisation avec Postman - Version Finale

## URL de l'API

**URL publique:** `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer`

**Documentation interactive:** https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/docs

---

## 📋 Endpoint 1: Lister tous les IDs des vector stores

### Configuration dans Postman

**Méthode:** `GET`

**URL:** `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores`

### Headers

| Key | Value |
|-----|-------|
| `x-openai-api-key` | `sk-votre_clé_openai_ici` |

### Réponse - Simple Array d'IDs

```json
[
  "vs_68f61de174e08191991f7b341db64921",
  "vs_68f61d408d488191a8251dd627526adc",
  "vs_68f61c61aa208191a28f0fe2bd7cfe7d",
  "vs_68f61ae465d481919cf904a92645d3ba",
  "vs_68f61ad6fddc81918eb4ca456b04faec"
]
```

**✅ Avantages:**
- Format simple et direct
- Facile à copier-coller dans le DELETE
- Pagination automatique (récupère TOUS les IDs)
- Pas besoin d'extraire les IDs manuellement

---

## 🗑️ Endpoint 2: Supprimer plusieurs vector stores

### Configuration dans Postman

**Méthode:** `DELETE`

**URL:** `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores`

### Headers

| Key | Value |
|-----|-------|
| `x-openai-api-key` | `sk-votre_clé_openai_ici` |
| `Content-Type` | `application/json` |

### Body (raw JSON)

Vous pouvez copier-coller directement l'array reçu du GET:

```json
{
  "vector_store_ids": [
    "vs_68f61de174e08191991f7b341db64921",
    "vs_68f61d408d488191a8251dd627526adc",
    "vs_68f61c61aa208191a28f0fe2bd7cfe7d"
  ]
}
```

### Réponse

```json
{
  "success": [
    "vs_68f61de174e08191991f7b341db64921",
    "vs_68f61d408d488191a8251dd627526adc",
    "vs_68f61c61aa208191a28f0fe2bd7cfe7d"
  ],
  "failed": []
}
```

---

## 📁 Endpoint 3: Lister les fichiers d'un vector store

**Méthode:** `GET`

**URL:** `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores/{vector_store_id}/files`

### Headers

| Key | Value |
|-----|-------|
| `x-openai-api-key` | `sk-votre_clé_openai_ici` |

---

## 🗑️ Endpoint 4: Supprimer un fichier

**Méthode:** `DELETE`

**URL:** `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores/{vector_store_id}/files/{file_id}`

### Headers

| Key | Value |
|-----|-------|
| `x-openai-api-key` | `sk-votre_clé_openai_ici` |

---

## 🔥 Workflow Ultra-Simplifié

### Étape 1: Récupérer tous les IDs

```
GET /vector_stores
```

**Réponse:**
```json
[
  "vs_68f61de174e08191991f7b341db64921",
  "vs_68f61d408d488191a8251dd627526adc",
  "vs_68f61c61aa208191a28f0fe2bd7cfe7d",
  "vs_68f61ae465d481919cf904a92645d3ba"
]
```

### Étape 2: Copier l'array complet ou sélectionner les IDs

Vous pouvez:
- **Option A:** Copier l'array complet pour tout supprimer
- **Option B:** Sélectionner seulement certains IDs

### Étape 3: Supprimer en une seule requête

```
DELETE /vector_stores

Body:
{
  "vector_store_ids": [COLLER_ICI_L_ARRAY]
}
```

**C'est tout ! 🎉**

---

## 💡 Exemple Concret

### 1. GET tous les IDs

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: sk-proj-xxxxx"
```

**Réponse:**
```json
["vs_id1", "vs_id2", "vs_id3", "vs_id4", "vs_id5"]
```

### 2. DELETE les IDs sélectionnés

```bash
curl -X DELETE "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: sk-proj-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "vector_store_ids": ["vs_id1", "vs_id2", "vs_id3"]
  }'
```

**Réponse:**
```json
{
  "success": ["vs_id1", "vs_id2", "vs_id3"],
  "failed": []
}
```

---

## ⚡ Avantages de cette approche

1. **Simple:** Un array direct d'IDs, pas besoin d'extraire les données
2. **Rapide:** Copier-coller direct du GET vers le DELETE
3. **Automatique:** La pagination se fait automatiquement, vous obtenez TOUS les IDs
4. **Clair:** Vous voyez immédiatement combien de vector stores vous avez
5. **Flexible:** Vous pouvez supprimer tous les IDs ou juste une sélection

---

## 🎯 Collection Postman Recommandée

### Variables
- `base_url`: `https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer`
- `api_key`: `sk-votre_clé_ici`

### Requête 1: Get All Vector Store IDs
```
GET {{base_url}}/vector_stores
Headers: x-openai-api-key: {{api_key}}
```

### Requête 2: Delete Multiple Vector Stores
```
DELETE {{base_url}}/vector_stores
Headers: 
  x-openai-api-key: {{api_key}}
  Content-Type: application/json
Body:
{
  "vector_store_ids": []  // Coller ici l'array du GET
}
```

---

## 📝 Notes

- L'endpoint GET récupère automatiquement TOUS les vector stores (pagination automatique)
- Le format de réponse est maintenant un simple array d'IDs
- Vous pouvez copier-coller directement cet array dans le body du DELETE
- La suppression retourne les succès ET les échecs pour un suivi précis

