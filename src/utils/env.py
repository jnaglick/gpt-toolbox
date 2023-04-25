from dotenv import load_dotenv
import os

OPENAI_API_KEY = "OPENAI_API_KEY"
LOG_LEVEL = "LOG_LEVEL"

def load_env():
    load_dotenv()

    return {
        OPENAI_API_KEY: os.getenv(OPENAI_API_KEY),
        LOG_LEVEL: os.getenv(LOG_LEVEL),
    }

env = load_env()
