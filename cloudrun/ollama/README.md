# Ollama on Cloud Run with Gemma Models

This folder contains a Dockerfile for deploying Ollama with Gemma 3 (4B) and EmbeddingGemma models on Google Cloud Run with GPU support.

## Prerequisites

- Google Cloud account with billing enabled
- Access to Google Cloud Shell (or gcloud CLI installed locally)
- An active GCP project selected

## Deployment

Run these commands in Google Cloud Shell.

### 1. Verify Cloud Build is ready

```bash
gcloud builds get-default-service-account
```

This retrieves the default Cloud Build service account. If you see an error, Cloud Build API may need to be enabled. You can enable the APIs with:

```bash
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com
```

### 2. Deploy to Cloud Run

## ⚠️ Important: Security Notice

This deployment uses `--allow-unauthenticated`, meaning **anyone with the URL can access the service**. This is fine for a quick workshop demo, but for any production or development workload, configure proper authentication.

```bash
gcloud run deploy ollama-gemma \
  --source . \
  --concurrency 4 \
  --region europe-west1 \
  --cpu 8 \
  --set-env-vars OLLAMA_NUM_PARALLEL=4 \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --max-instances 1 \
  --memory 32Gi \
  --allow-unauthenticated \
  --no-cpu-throttling \
  --no-gpu-zonal-redundancy \
  --timeout=600
```

This will take a few minutes. If running for the first time, you'll be prompted to enable Cloud Build, Artifact Registry, and Cloud Run APIs—confirm with `y`.

Once complete, you'll see the service URL in the output.

## Testing the deployment

Replace `YOUR_SERVICE_URL` with the URL from the deployment output.

**Linux / macOS:**

```bash
SERVICE_URL="https://your-service-url-here"

curl -X POST "$SERVICE_URL/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"model": "gemma3:4b", "prompt": "What day comes after Friday?", "stream": false}'
```

**Windows (PowerShell):**

```powershell
$SERVICE_URL = "https://your-service-url-here"

Invoke-RestMethod -Uri "$SERVICE_URL/api/generate" -Method POST -ContentType "application/json" -Body '{"model": "gemma3:4b", "prompt": "What day comes after Friday?", "stream": false}'
```

**Windows (Command Prompt):**

```cmd
set SERVICE_URL=https://your-service-url-here

curl -X POST "%SERVICE_URL%/api/generate" -H "Content-Type: application/json" -d "{\"model\": \"gemma3:4b\", \"prompt\": \"What day comes after Friday?\", \"stream\": false}"
```


## Cleanup

When you're done, delete the service to avoid charges:

```bash
gcloud run services delete ollama-gemma --region=europe-west1
```

Adjust the service name and region if you changed them during deployment.