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
DEFAULT_LEARNER_PROFILE = (
    "A 12th-grade graduate from India with limited English "
    "vocabulary and no prior knowledge of AI or machine learning."
)
DEMO_MODE = True