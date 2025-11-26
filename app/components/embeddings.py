from langchain_huggingface import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from langchain_openai import ChatOpenAI
from app.config.config import EMBEDDING_MODEL_NAME, EMBEDDING_SERVER_URL
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import LlamaCppEmbeddings
from openai import OpenAI

logger = get_logger(__name__)

def get_embedding_model():
    try:
        # logger.info("Intializing our Huggingface embedding model")

        
        #model = OpenAI(base_url="http://localhost:808/v1", api_key="llama-cpp")
        

        # # Validate EMBEDDING_SERVER_URL before using it
        # if not EMBEDDING_SERVER_URL:
        #     raise CustomException("EMBEDDING_SERVER_URL is not set. Please configure it in app.config.config or environment variables.")

        # base = EMBEDDING_SERVER_URL.rstrip("/")

        # model = OpenAIEmbeddings(model=EMBEDDING_MODEL_NAME,base_url=EMBEDDING_SERVER_URL)

        model = LlamaCppEmbeddings(model_path="./app/embdding_model/all-MiniLM-L6-v2-ggml-model-f16.gguf")
        

        # logger.info("Huggingface embedding model loaded sucesfully....")

        return model
    
    except Exception as e:
        error_message=CustomException("Error occured while loading embedding model" , e)
        logger.error(str(error_message))
        raise error_message