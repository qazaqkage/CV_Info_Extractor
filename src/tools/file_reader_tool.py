from langchain.tools import BaseTool
from pathlib import Path
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from pydantic import PrivateAttr
from typing import Any
import json

class FileReadTool(BaseTool):
    name: str = "FileReadTool"  # Annotated with type
    description: str = "Reads a CV file and uses an LLM to extract structured information."  # Annotated with type
    _llm: ChatOpenAI = PrivateAttr()  # Declared as a private attribute

    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """
        Initialize with the API key and model name.
        """
        super().__init__()
        self._llm = ChatOpenAI(openai_api_key=api_key, model=model_name, temperature=0)

    def _run(self, file_path: str) -> dict:
        """
        Extracts key information from a CV file using an LLM.
        """
        file = Path(file_path)
        if not file.exists():
            raise FileNotFoundError(f"{file_path} not found!")

        # Extract raw text from the file (PDF)
        if file.suffix.lower() == ".pdf":
            reader = PdfReader(file_path)
            raw_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        else:
            raise ValueError(f"Unsupported file format: {file.suffix}")

        # Prompt the LLM to extract structured information
        prompt = (
            f"The following text is extracted from a CV:\n\n{raw_text}\n\n"
            "Please extract the following details in JSON format:\n"
            "- Name\n"
            "- Email\n"
            "- Desired Position\n"
            "- Skills\n"
            "- Years of Experience\n"
            "- Education Background"
        )
        response = self._llm.invoke(prompt)  # Use invoke to get AIMessage response

        try:
            # Extract the raw content from the `invoke` response
            raw_response = response.content.strip()  # Access the content and remove leading/trailing whitespace

            # Clean up triple backticks if present
            if raw_response.startswith("```") and raw_response.endswith("```"):
                raw_response = raw_response[3:-3].strip()

            # Remove the "json" prefix if present
            if raw_response.lower().startswith("json"):
                raw_response = raw_response[4:].strip()

            # Safely parse the JSON output
            parsed_response = json.loads(raw_response)  # Convert the JSON string into a Python dictionary
            return parsed_response
        except json.JSONDecodeError as e:
            # If parsing fails, include the raw response in the error for debugging
            raise ValueError(f"Failed to parse LLM response: {raw_response}") from e

    async def _arun(self, file_path: str) -> Any:
        raise NotImplementedError("FileReadTool does not support async.")
