# Open LLM Workshops

Hands-on materials for running open-source language models locally and on Google Cloud.

## 📓 Notebooks

Colab notebooks that run on the free tier. Most of them require GPU support, which can be covered by free tier, check the details in the notebooks.

Most notebooks use Ollama with Gemma models. Some (like the Bielik agent notebook) use HuggingFace Transformers and require a free HuggingFace account with a read token — details inside the notebooks.

→ [`notebooks/`](./notebooks/)

## ☁️ Cloud Run

Deploy Ollama with GPU on Google Cloud Run and build simple apps on top of it.

| Folder | Description |
|--------|-------------|
| [`cloudrun/ollama`](./cloudrun/ollama/) | Ollama + Gemma 3 + EmbeddingGemma on Cloud Run with L4 GPU |
| [`cloudrun/image-describer`](./cloudrun/image-describer/) | Gradio app for image analysis with Gemma Vision |
| [`cloudrun/rag`](./cloudrun/rag/) | Simple RAG demo — upload PDF, ask questions |

Start with `ollama/`, then try the apps that connect to it.

## 📬 Contact

Tomek Porozynski

- GitHub: [@ontaptom](https://github.com/ontaptom)
- Linkedin: [in/tomaszporozynski](https://www.linkedin.com/in/tomaszporozynski/)


