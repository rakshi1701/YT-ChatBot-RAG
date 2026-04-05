# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask questions about any YouTube video using its transcript.

---

## 🚀 Features

* 🔗 Extracts transcript from YouTube videos
* ✂️ Splits transcript into semantic chunks
* 🧠 Generates embeddings using Sentence Transformers
* ⚡ Stores embeddings in FAISS for fast similarity search
* 🔍 Retrieves most relevant context based on user query
* 🤖 Generates answers using local LLM (Mistral via Ollama)
* 🌐 Simple HTML frontend for interaction

---

## 🏗️ Architecture

```
YouTube URL
    ↓
Transcript Extraction
    ↓
Text Chunking
    ↓
Embeddings (SentenceTransformers)
    ↓
FAISS Vector Store
    ↓
Query Embedding
    ↓
Similarity Search (Top-K)
    ↓
Context + Question
    ↓
LLM (Ollama - Mistral)
    ↓
Final Answer
```

---

## 📂 Project Structure

```
YT-ChatBot-RAG/
│
├── backend/
│   ├── main.py          # FastAPI app
│   ├── rag_utils.py     # Core RAG logic
│   ├── config.py        # API keys & model config
│   └── requirements.txt
│
├── index.html           # Simple frontend
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone git@github.com:rakshi1701/YT-ChatBot-RAG.git
cd YT-ChatBot-RAG/backend
```

---

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn faiss-cpu numpy sentence-transformers youtube-transcript-api requests
```

---

### 4️⃣ Install Ollama (Local LLM)

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start server:

```bash
ollama serve
```

Pull model:

```bash
ollama pull mistral
```

---

### 5️⃣ Run Backend

```bash
uvicorn main:app --reload
```

API will run at:

```
http://127.0.0.1:8000
```

---

### 6️⃣ Open Frontend

Open `Frontend/test.html` in browser.

---

## 📡 API Endpoints

### ▶️ Process Video

```http
POST /process_video?url=<youtube_url>
```

**Response:**

```json
{
  "message": "Video processed successfully"
}
```

---

### ▶️ Ask Question

```http
POST /ask?question=<your_question>
```

**Response:**

```json
{
  "answer": "Generated answer from video context"
}
```

---

## 🧠 Tech Stack

* **Backend:** FastAPI
* **Embeddings:** Sentence Transformers
* **Vector DB:** FAISS
* **LLM:** Mistral (via Ollama)
* **Frontend:** HTML + JavaScript

---

## ⚠️ Notes

* Ensure Ollama server is running before asking questions
* Works with videos that have transcripts available
* Supports multilingual transcripts (answers in English)

---

## 🔥 Future Improvements

* ✅ Chat UI (React / Next.js)
* ✅ Streaming responses
* ✅ Persistent FAISS storage
* ✅ Hybrid search (BM25 + Vector)
* ✅ Docker deployment
* ✅ GPU acceleration

---

## 💡 Use Cases

* 📚 Learn from YouTube videos quickly
* 🎓 Educational Q&A assistant
* 🔍 Video content summarization
* 🤖 AI-powered knowledge retrieval

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
