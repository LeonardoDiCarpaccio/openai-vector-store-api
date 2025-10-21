# Exemples de requêtes cURL

Remplacez `YOUR_OPENAI_API_KEY` par votre vraie clé API OpenAI.

## 1. Lister tous les vector stores

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY"
```

Avec pagination:

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores?limit=10&order=desc" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY"
```

## 2. Supprimer plusieurs vector stores

```bash
curl -X DELETE "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vector_store_ids": ["vs_abc123", "vs_def456", "vs_ghi789"]
  }'
```

## 3. Lister les fichiers d'un vector store

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores/vs_abc123/files" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY"
```

Avec filtres:

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores/vs_abc123/files?limit=20&filter_status=completed" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY"
```

## 4. Supprimer un fichier d'un vector store

```bash
curl -X DELETE "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores/vs_abc123/files/file-abc123" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY"
```

## 5. Tester l'endpoint racine (sans clé API)

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/"
```

## Workflow complet

### Étape 1: Lister tous vos vector stores

```bash
curl -X GET "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY" | jq '.'
```

### Étape 2: Copier les IDs des vector stores à supprimer

Depuis la réponse, copiez les IDs des vector stores que vous voulez supprimer.

### Étape 3: Supprimer les vector stores sélectionnés

```bash
curl -X DELETE "https://8000-iafdd7rrl46x0l16k9q5m-cbe93295.manusvm.computer/vector_stores" \
  -H "x-openai-api-key: YOUR_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vector_store_ids": ["vs_id1", "vs_id2", "vs_id3"]
  }' | jq '.'
```

## Notes

- L'option `| jq '.'` à la fin des commandes formate le JSON de manière lisible (nécessite `jq` installé)
- Toutes les requêtes retournent du JSON
- Les erreurs sont retournées avec des codes HTTP appropriés (400, 401, 404, 500, etc.)

