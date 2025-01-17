import os
from pathlib import Path
from tools.file_reader_tool import FileReadTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API key and model name from .env
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

# Directory to store CVs
CVS_DIR = Path("data/cvs")
CVS_DIR.mkdir(parents=True, exist_ok=True)

def process_last_cv():
    """
    Reads the last uploaded CV and extracts key information using an LLM.
    """
    # Get the most recently uploaded CV
    cv_files = sorted(CVS_DIR.iterdir(), key=lambda f: f.stat().st_mtime, reverse=True)
    if not cv_files:
        raise FileNotFoundError("No CVs found in the uploads directory!")

    last_cv = cv_files[0]
    tool = FileReadTool(api_key=API_KEY, model_name=MODEL_NAME)
    key_info = tool.run(str(last_cv))
    return key_info
