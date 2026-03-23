import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Neo4j Settings
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    MODEL_NAME = "gemini-flash-latest"


if not Config.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")