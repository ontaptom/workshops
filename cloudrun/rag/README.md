# RAG Demo - Question Answering over PDFs

A simple Flask app that lets you upload a PDF and ask questions about its content using Retrieval-Augmented Generation with Gemma models.

## Prerequisites

- The Ollama service from `workshops/cloudrun/ollama` deployed and running
- Your Ollama service URL handy

## Deployment

If you're coming from the previous exercise, navigate to this directory:
```bash
cd ../rag
```

Deploy to Cloud Run:
```bash
gcloud run deploy rag-demo \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

Once complete, open the service URL in your browser.

## Usage

1. Paste your Ollama service URL
2. Upload a PDF file (must be text-based PDF, not scanned images)
3. Click "Process PDF" — the app will chunk the document and generate embeddings using EmbeddingGemma. Depending on PDF size, this may take a few minutes. Progress updates will be shown.
4. Once processing is complete, ask questions about the document

## ⚠️ Important Disclaimers

**This is a workshop demo app, not production-ready code.**

- **No state persistence** — refreshing the page loses everything; you'll need to re-upload and reprocess
- **No scale optimization** — single instance, in-memory storage, will struggle with large PDFs or concurrent users
- **Simplest possible RAG implementation** — uses basic `cosine_similarity` for retrieval, naive chunking strategy, no reranking, no hybrid search
- **Text PDFs only** — scanned documents or image-based PDFs won't work

There's plenty of room for improvement: vector databases, better chunking, semantic caching, etc. This is just to demonstrate the core RAG concept.

## ⚠️ Security Notice

Uses `--allow-unauthenticated` for workshop simplicity. Not for production use.

## Cleanup
```bash
gcloud run services delete rag-demo --region=europe-west1
```