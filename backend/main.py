# File -> runs backend logic to frontend through FastApi

from fastapi import FastAPI
from rag_utils import *
from rag_utils import extract_video_id

from fastapi.middleware.cors import CORSMiddleware

# Create FastApi app
app = FastAPI()

# enable app using corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True, 
    allow_methods = ["*"],
    allow_headers = ['*']
)

# create to store processed video
chunks = []
index = None
# 1. Create processed video endpoint
@app.post("/process_video")
def process_video(url: str):
    global chunks, index

    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid Youtube URL"}
    
    # Get Transcript
    text = get_transcript(video_id)
    if not text:
        return {"error": "Transcript not found"}
    
    # Split transcript into chinks
    chunks = split_text(text)

    # create embeddings 
    embedings = create_embeddings(chunks)

    # Build FAISS Index
    index = build_faiss_index(embedings)

    return {"message": "Video processed sucessfully"}

# 2. Ask questions on processed video
@app.post("/ask")
def ask(question: str):
    if index is None:
        return {"error": "Please process a video first"}
    try:
        # Convert question to embedding
        query_embedding = create_embeddings([question])[0]

        # Retrieve Relevent chunks
        top_chunks = retrieve_chunks(index, query_embedding)
        if len(top_chunks) == 0:
            return {"answer": "No relevant context found in video"}
        
        # combine Context
        context_chunks = []
        for i in top_chunks:
            if i < len(chunks):
                context_chunks.append(chunks[i])
        
        context = " ". join(context_chunks)

        # debugging
        print("retrieved chunks: ", top_chunks)
        print("context preview: ", context[:300])

        #  Ask LLM
        answer = ask_llm(context, question)

        # return answer
        return {"answer": answer}
    
    except Exception as e:
        print("Ask error: ", e)
        return {"error": str(e)}

