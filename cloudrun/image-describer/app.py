# app.py
import gradio as gr
from ollama import Client
import tempfile
import os

def ask_ollama(ollama_url, prompt, image):
    if not ollama_url:
        return "Please provide Ollama URL"
    if image is None:
        return "Please upload an image"
    
    # Save uploaded image to temp file
    temp_path = os.path.join(tempfile.gettempdir(), "uploaded_image.png")
    image.save(temp_path)
    
    try:
        client = Client(host=ollama_url)
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
            images=[temp_path]
        )
        return response['response']
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=ask_ollama,
    inputs=[
        gr.Textbox(label="Ollama URL", placeholder="https://ollama-xxx.run.app"),
        gr.Textbox(label="Prompt", value="Describe this image"),
        gr.Image(label="Upload image", type="pil"),
    ],
    outputs=gr.Textbox(label="Response", lines=10),
    title="🖼️ Gemma Vision on Cloud Run",
    clear_btn="Reset",
)

demo.launch(server_name="0.0.0.0", server_port=8080)
