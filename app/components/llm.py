from app.config.config import LLM_PROVIDER, LLAMA_SERVER_URL, LLM_MODEL_NAME,OPENAI_API_KEY,GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from langchain_openai import ChatOpenAI

logger = get_logger(__name__)


def load_llm(model_name: str | None = None, groq_api_key: str = GROQ_API_KEY):
    """Load an LLM client based on configured provider.

    Supported providers:
    - 'groq' (default): uses langchain_groq.ChatGroq
    - 'llamacpp': uses an OpenAI-compatible HTTP client pointed at LLAMA_SERVER_URL

    For llama.cpp's HTTP server, ensure the server exposes an OpenAI-compatible
    /v1/chat/completions endpoint (many llama.cpp frontends do).
    """
    try:
        # Use provided model_name or the configured default
        model_name = model_name or LLM_MODEL_NAME

        provider = (LLM_PROVIDER or "groq").lower()

        if provider == "groq":
            # Lazy import to avoid requiring langchain_groq when not used
            from langchain_groq import ChatGroq

            logger.info("Loading LLM from Groq using LLaMA3 model...")

            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name=model_name,
                temperature=0.3,
                max_tokens=256,
            )

            logger.info("LLM loaded successfully from Groq.")
            return llm

        elif provider == "llamacpp":
            # Use OpenAI-compatible client but point to the llama.cpp server URL.
            # langchain provides ChatOpenAI which delegates to openai SDK. We configure
            # the OPENAI_API_BASE environment variable so that openai calls target the
            # llama.cpp HTTP server (which must implement the OpenAI-compatible endpoints).
            import os

            if not LLAMA_SERVER_URL:
                raise ValueError("LLAMA_SERVER_URL is not set for provider 'llamacpp'")

            # Ensure the base URL ends with /v1 or the appropriate prefix expected by the server
            base = LLAMA_SERVER_URL.rstrip("/")

            # Set environment variable used by openai client to override base url
            # os.environ.setdefault("OPENAI_API_BASE", base)

            # logger.info("Loading LLM using OpenAI-compatible client pointed at %s", base)

            # Create a ChatOpenAI model wrapper. Model name should match what the server expects.
           # llm = ChatOpenAI(model=model_name, temperature=0.3, max_tokens=256)



            # Use the cleaned base URL (string). If your llama.cpp HTTP server does
            # not require an API key, omit the api_key parameter. Passing a tuple
            # (like ("OPENAI_API_BASE", base)) causes pydantic validation errors.
            llm = ChatOpenAI(
                model=model_name,
                temperature=0.3,
                stream_usage=True,
                base_url=base,
                max_tokens=256,
            )
            logger.info("LLM loaded successfully from llama.cpp HTTP server.")
            return llm

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    except Exception as e:
        error_message = CustomException("Failed to load an LLM", e)
        logger.error(str(error_message))
        return None
