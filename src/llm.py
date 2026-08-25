from langchain_ollama import ChatOllama

from src.config import MODEL_NAME, OLLAMA_BASE_URL


def get_llm() -> ChatOllama:
    """Create and return the configured local Ollama model."""

    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )