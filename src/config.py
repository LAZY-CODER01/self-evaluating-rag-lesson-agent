import os

from dotenv import load_dotenv


load_dotenv()


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3:14b")

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))