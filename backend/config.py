# store configuration variables
import os
from dotenv import load_dotenv

#  loading env var
load_dotenv()

# Getting OPENAI API KEY
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")

# Embiding model for generating vector embeddings
# EMBEDDING_MODEL = 'text-embedding-3-small'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# LLM Model for generating ans
LLM_MODEL = 'gpt-3.5-turbo'

