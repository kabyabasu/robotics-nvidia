import os

# Tokens / API keys
#HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# LLM provider selection. Supported: 'groq' (default), 'llamacpp' (OpenAI-compatible HTTP server)
# Set LLM_PROVIDER to 'llamacpp' and LLAMA_SERVER_URL to your server base (e.g. http://127.0.0.1:8080/v1)
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "groq")
LLAMA_SERVER_URL = os.environ.get("LLAMA_SERVER_URL")
# Default model name to use with llama.cpp (can be overridden via env)
# Example: Llama-3.1-8B-Instruct-Q4_0.gguf
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "Llama-3.1-8B-Instruct-Q4_0.gguf")

EMBEDDING_MODEL_NAME  = os.environ.get("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2-ggml-model-f16.gguf")
EMBEDDING_SERVER_URL = os.environ.get("EMBEDDING_SERVER_URL")


HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
DB_FAISS_PATH = "vectorstore/db_faiss"
DATA_PATH = "data/"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
