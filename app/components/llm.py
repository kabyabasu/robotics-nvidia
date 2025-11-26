from app.config.config import LLM_PROVIDER, LLAMA_SERVER_URL, LLM_MODEL_NAME, OPENAI_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from langchain_openai import ChatOpenAI

logger = get_logger(__name__)


def load_llm(model_name: str | None = None):
    """Load an LLM client based on configured provider.

    Supported providers:
    - 'llamacpp' (default): uses an OpenAI-compatible HTTP client pointed at LLAMA_SERVER_URL
    - 'openai': uses OpenAI's API via ChatOpenAI

    For llama.cpp's HTTP server, ensure the server exposes an OpenAI-compatible
    /v1/chat/completions endpoint (many llama.cpp frontends do).
    """
    try:
        # Use provided model_name or the configured default
        model_name = model_name or LLM_MODEL_NAME

        provider = (LLM_PROVIDER or "llamacpp").lower()

        if provider == "llamacpp":
            # Use OpenAI-compatible client but point to the llama.cpp server URL.
            import os

            if not LLAMA_SERVER_URL:
                raise ValueError("LLAMA_SERVER_URL is not set for provider 'llamacpp'")

            # Ensure the base URL ends without a trailing slash
            base = LLAMA_SERVER_URL.rstrip("/")

            # Create a ChatOpenAI model wrapper that points to the llama.cpp HTTP server.
            llm = ChatOpenAI(
                model=model_name,
                temperature=0.3,
                stream_usage=True,
                base_url=base,
                max_tokens=256,
            )
            logger.info("LLM loaded successfully from llama.cpp HTTP server.")
            return llm

        elif provider == "openai":
            # Use ChatOpenAI against OpenAI's servers. Ensure OPENAI_API_KEY is set in env.
            llm = ChatOpenAI(model=model_name, temperature=0.3, max_tokens=256)
            logger.info("LLM loaded successfully from OpenAI.")
            return llm

        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    except Exception as e:
        error_message = CustomException("Failed to load an LLM", e)
        logger.error(str(error_message))
        return None
