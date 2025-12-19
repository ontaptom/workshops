# Image Describer - Gradio Frontend for Gemma Vision

A simple Gradio web app that sends images to your Ollama service running Gemma 3 for visual analysis.

## Prerequisites

- The Ollama service from `workshops/cloudrun/ollama` deployed and running
- Your Ollama service URL handy

## Deployment

If you're coming from the Ollama deployment (`workshops/cloudrun/ollama`), navigate to this directory:

```bash
cd ../image-describer
```

Deploy to Cloud Run:

```bash
gcloud run deploy image-describer \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

Once complete, open the service URL in your browser.

## Usage

1. Paste your Ollama service URL (e.g., `https://ollama-gemma-xxx-ew.a.run.app`)
2. Enter a prompt (default: "Describe this image")
3. Upload an image
4. Click Submit

The app sends your image to Gemma 3 and displays the model's response.

## ⚠️ Security Notice

Like the Ollama service, this uses `--allow-unauthenticated` for workshop simplicity. Not for production use.

## Cleanup

```bash
gcloud run services delete image-describer --region=europe-west1
```