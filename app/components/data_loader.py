import os
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so `import app...` works when
# running this module directly (e.g. `python app/components/data_loader.py`).
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.components.pdf_loader import load_pdf_files,create_text_chunks
from app.components.vector_store import save_vector_store
from app.config.config import DB_FAISS_PATH

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_pdfs():
    try:
        logger.info("MAking the vectorstore....")
        
        documents = load_pdf_files()

        text_chunks = create_text_chunks(documents)

        save_vector_store(text_chunks)

        logger.info("Vectorstore created sucesfully....")

    except Exception as e:
        error_message = CustomException("Faialedd to create vectorstore",e)
        logger.error(str(error_message))


if __name__=="__main__":
    process_and_store_pdfs()
