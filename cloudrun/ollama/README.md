# Ollama on Cloud Run with Gemma Models

This folder contains a Dockerfile for deploying Ollama with Gemma 3 (4B) and EmbeddingGemma models on Google Cloud Run with GPU support.

## Prerequisites

- Google Cloud account with billing enabled
- Access to Google Cloud Shell (or gcloud CLI installed locally)
- An active GCP project selected

## Clone the repo and navigate to proper folder

Run there commands in Google Cloud Shell.

### 1. Clone the repository

```bash
git clone https://github.com/ontaptom/workshops.git
```

### 2. Navigate to proper structure

```bash
$ cd workshops/cloudrun/ollama/
```

## Deployment

Run these commands in Google Cloud Shell.

### 1. Enable necessary APIs and Verify Cloud Build is ready


Enable necessary APIs, it might take few minutes
```bash
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com
```

This retrieves the default Cloud Build service account. If you get an error, give it another minute, perhaps the previous operation is still not finished.

```bash
gcloud builds get-default-service-account
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

You may see a request to create a repository in Artifact Registry. Press `Y` to continue. What happens in the background is, our Dockerbuild will be used to build a container image, which will be stored in Artifact Registry in Your project, so later on it can be used for new deployments. However, this command will automatically also deploy the container.

This will take a few minutes. If running for the first time, you'll be prompted to enable Cloud Build, Artifact Registry, and Cloud Run APIs—confirm with `y`.

Once complete, you'll see the service URL in the output.

The output at the end should look like that:

```bash
⚠️ this is an example output, do not copy/paste me to the terminal! :)

Deploying from source requires an Artifact Registry Docker repository to store built containers. A repository named [cloud-run-source-deploy] in region [europe-west1] will be created.

Do you want to continue (Y/n)?  Y

Building using Dockerfile and deploying container to Cloud Run service [ollama-gemma] in project [project-id] region [europe-west1]
Building and deploying new service...                                                                                                                                                                                  
  Validating Service...done                                                                                                                                                                                            
  Creating Container Repository...done                                                                                                                                                                                 
  Uploading sources...done                                                                                                                                                                                             
  Building Container... Logs are available at [https://console.cloud.google.com/cloud-build/builds;region=[...]]....done                              
  Setting IAM Policy...done                                                                                                                                                                                            
  Creating Revision...done                                                                                                                                                                                             
  Routing traffic...done                                                                                                                                                                                               
Done.                                                                                                                                                                                                                  
Service [ollama-gemma] revision [ollama-gemma-00001-vlc] has been deployed and is serving 100 percent of traffic.
Service URL: https://ollama-<rest-of-url>.europe-west1.run.app
```

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