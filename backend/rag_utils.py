# import dependencies
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import re 
import faiss #extract most releavent features
import numpy as np
from config import OPENAI_API_KEY, EMBEDDING_MODEL, LLM_MODEL
from sentence_transformers import SentenceTransformer

# Flow: transc -> split -> embed -> vector -> num array -> store in Faiss

# 1. Initilizing OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Extracting youtube video ID (input Video URL and return videoId)
def extract_video_id(url):
    patterns = [
        r"(?:v|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})"

    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        # if we find a match
        if match:
            return match.group(1)
        
    return None

# 2. Featching video Transcript (input videoId -> return Transcript)
def get_transcript(video_id):
    try:
        # extract transcript
        ytt_api = YouTubeTranscriptApi()
        try:
            # fetch english caption or transcript
            transcript_data = ytt_api.fetch(video_id, languages=["en"])

        except Exception:
            # if english language is not found then provide next available language
            transcript_list = ytt_api.list(video_id)
            transcript_data = next(iter(transcript_list)).fetch()

        full_text = " ".join(item.text for item in transcript_data) # join entire text of transcript including sub video
        return re.sub(r"\s+", " ", full_text ) # remove extra space and return full text
    
    except Exception as e:
        # If no transcript is found
        print("transcript error: ", e)
        return None
    
# 3 spliting transcript into chunks (input full transcript -> return splitted smaller chunks)
def split_text(text, chunk_size = 150):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size]) # ['hello', 'everyone'] -> 'hello everyone'
        for i in range(0, len(words), chunk_size)
    ]

# 4. Creating Embeddings (input chunks -> return Embeddings vector)
# def create_embeddings(text_list):
#     response = client.embeddings.create(
#         model= EMBEDDING_MODEL,
#         input= text_list
#     )
#     return np.array([item.embedding for item in response.data]).astype("float32")

model = SentenceTransformer(EMBEDDING_MODEL)
def create_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    return model.encode(texts, convert_to_numpy=True)

# 5. Building FAISS Index (store embeddings in vector -> search)
# Faiss - Fast similarity search on vectors
def build_faiss_index(embeddings):
    embeddings = embeddings.astype("float32")
    index = faiss.IndexFlatL2(embeddings.shape[1]) # created faiss index
    index.add(embeddings) # adding embeddings to index
    return index # return index

# 6. Retrieve relevent chunks (search faiss index -> return most relevent chunks for a user query)
# k = number of faiss similar, k= 3 -> provide top 3 similarities
# def retrieve_chunks(index, query_embedding, k=3):
#     ditances, indices = index.search(
#         np.array([query_embedding]).astype("float32"), k
#     )
#     return indices[0]

def retrieve_chunks(index, query_embedding, k=3):
    query_embedding = np.array([query_embedding]).astype("float32")
    distances, indices = index.search(query_embedding, k)
    return indices[0]

# 7. Asking LLM (send retrieve text transcript content & user que -> LLM model)
# def ask_llm(context, question):
#     # Handle empty context
#     if not context.strip():
#         return "sorry, I couldn't find relevant info in video transcript"

#     # Truncate context
#     context = context[:6000]

#     prompt = f""" You are an AI assistent answering question about a YouTube video.
#     The transcript may be in any language (Kannada, Hindi, English, etc).
#     Always answer in English using provided context.
    
#     Transcript Context:
#     {context}

#     Question:
#     {question}

#     Answer clearly in English: """

#     # callling llm api
#     response = client.chat.completions.create(
#         model= LLM_MODEL,
#         messages=[
#             {"role": "system", "content": "You answer question about YouTube videos."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content()

import requests

# def ask_llm(context, question):
#     prompt = f"Context: {context}\n\nQuestion: {question}"

#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={
#             "model": "mistral",
#             "prompt": prompt,
#             "stream": False
#         }
#     )

#     return response.json()["response"]

def ask_llm(context, question):
    prompt = f"Context: {context}\n\nQuestion: {question}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        return "LLM error"

    return response.json().get("response", "No response")