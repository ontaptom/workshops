# app.py
from flask import Flask, render_template, request, jsonify
import pdfplumber
import numpy as np
import tempfile
import os
import time
import threading
import requests as http_requests

app = Flask(__name__)

storage = {
    "chunks": [],
    "embeddings": []
}

job = {
    "status": "idle",
    "logs": []
}

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
            text += "\n"
    return text

def chunk_text(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embed_texts(ollama_url, texts):
    response = http_requests.post(
        f"{ollama_url}/api/embed",
        json={"model": "embeddinggemma", "input": texts},
        timeout=300
    )
    response.raise_for_status()
    return response.json()["embeddings"]

def generate_text(ollama_url, prompt):
    response = http_requests.post(
        f"{ollama_url}/api/generate",
        json={"model": "gemma3:4b", "prompt": prompt, "stream": False},
        timeout=300
    )
    response.raise_for_status()
    return response.json()["response"]

def process_in_background(tmp_path, ollama_url):
    global job, storage
    
    try:
        job["logs"].append("📄 Extracting text from PDF...")
        text = extract_text_from_pdf(tmp_path)
        job["logs"].append(f"✓ Extracted {len(text)} characters")
        
        job["logs"].append("✂️ Chunking text...")
        new_chunks = chunk_text(text)
        job["logs"].append(f"✓ Created {len(new_chunks)} chunks")
        
        if not new_chunks:
            job["logs"].append("❌ No text found in PDF")
            job["status"] = "error"
            return
        
        job["logs"].append("🔢 Starting embedding...")
        
        BATCH_SIZE = 50
        new_embeddings = []
        total = len(new_chunks)
        
        start_total = time.time()
        
        for batch_start in range(0, total, BATCH_SIZE):
            batch = new_chunks[batch_start:batch_start + BATCH_SIZE]
            
            batch_start_time = time.time()
            batch_embeddings = embed_texts(ollama_url, batch)
            batch_elapsed = time.time() - batch_start_time
            
            new_embeddings.extend(batch_embeddings)
            
            done = batch_start + len(batch)
            pct = int(100 * done / total)
            job["logs"].append(f"🔢 Embedded {done}/{total} ({pct}%) - {batch_elapsed:.1f}s")
        
        elapsed_total = time.time() - start_total
        
        storage["chunks"].extend(new_chunks)
        storage["embeddings"].extend(new_embeddings)
        
        job["logs"].append(f"✅ Done! {total} chunks embedded in {elapsed_total:.1f}s. Knowledge base: {len(storage['chunks'])} chunks")
        job["status"] = "done"
    
    except Exception as e:
        job["logs"].append(f"❌ Error: {str(e)}")
        job["status"] = "error"
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify({
        "chunks": len(storage["chunks"]),
        "job_status": job["status"],
        "logs": job["logs"]
    })

@app.route('/clear', methods=['POST'])
def clear():
    storage["chunks"] = []
    storage["embeddings"] = []
    job["status"] = "idle"
    job["logs"] = []
    return jsonify({"status": "cleared"})

@app.route('/process', methods=['POST'])
def process():
    global job
    
    ollama_url = request.form.get('ollama_url', '').rstrip('/')
    file = request.files.get('pdf')
    
    if not file:
        return jsonify({"error": "No file uploaded"})
    
    if not ollama_url:
        return jsonify({"error": "No Ollama URL provided"})
    
    tmp_path = tempfile.mktemp(suffix=".pdf")
    file.save(tmp_path)
    
    job["status"] = "running"
    job["logs"] = ["📤 Upload complete, starting processing..."]
    
    thread = threading.Thread(target=process_in_background, args=(tmp_path, ollama_url))
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    ollama_url = data.get('ollama_url', '').rstrip('/')
    question = data.get('question')
    
    if not ollama_url:
        return jsonify({"error": "No Ollama URL provided"})
    if not storage["chunks"]:
        return jsonify({"error": "Knowledge base is empty"})
    if not question:
        return jsonify({"error": "No question provided"})
    
    query_embedding = embed_texts(ollama_url, question)[0]
    scores = [cosine_similarity(query_embedding, emb) for emb in storage["embeddings"]]
    top_indices = np.argsort(scores)[-3:][::-1]
    
    context = "\n\n".join([storage["chunks"][i] for i in top_indices])
    sources = [{"score": float(scores[i]), "text": storage["chunks"][i][:150]} for i in top_indices]
    
    prompt = f"""Answer the question based only on the following context and answer in the same language as the question:

{context}

Question: {question}
Answer in full sentence:"""
    
    answer = generate_text(ollama_url, prompt)
    
    return jsonify({
        "answer": answer,
        "sources": sources
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)