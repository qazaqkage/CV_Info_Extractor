CV Uploader and Key Information Extractor

This project is a simple yet powerful application for uploading CVs (PDF files), extracting key information such as name, email, skills, years of experience, and education background, and displaying it in a user-friendly interface. The frontend is built with Streamlit, and the backend leverages the LangChain framework for LLM-based text extraction.
Features

    Frontend:
        Upload CVs through a clean and simple Streamlit interface.
        Display extracted CV information in a JSON format.

    Backend:
        Uses LangChain with OpenAI's LLMs for text extraction from CVs.
        Handles PDF parsing via PyPDF2.

    Switch of Framework:
        Initially designed with the CrewAI framework, but switched to LangChain due to issues with tools in CrewAI, ensuring smoother development.

Installation

Follow these steps to set up and run the project locally.
1. Clone the Repository

git clone <repository-url>
cd <repository-folder>

2. Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

3. Install Requirements

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file in the project root and add the following:

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_NAME=gpt-4

How to Run the Project

    Run the Streamlit App:

    streamlit run src/streamlit_app.py

    Access the App: Open the app in your browser at http://localhost:8501.

    Upload a CV: Upload a PDF file, and the app will extract and display key information in JSON format.

Future Improvements and Undeveloped Parts
1. Backend: User Authorization

    Planned Features:
        Users can register and log in.
        Each user will have a unique account with their uploaded files stored securely.
    Planned Tech:
        Backend: Flask.
        Authentication: JWT-based authentication.

2. Database Integration

    Planned Features:
        Use PostgreSQL to store:
            Extracted CV data (key information).
            Uploaded CV files (for each user account).
    Planned Tech:
        Database: PostgreSQL.
        ORM: SQLAlchemy.

3. Dockerization

    Planned Features:
        Containerize the application for ease of deployment.
        Include both frontend (Streamlit) and backend (Flask) in separate services.
    Planned Tech:
        Docker.
        Docker Compose for managing services.

4. Expanded Functionality

    Use the backend to:
        Store uploaded CVs and extracted data in the database.
        Enable CRUD operations for users to manage their uploaded files.
    Frontend improvements:
        Add user-friendly login and dashboard for managing files.

Acknowledgments

    LangChain: Used for text extraction and handling LLM-based operations.
    OpenAI: For powering the language model used in text extraction.
    Streamlit: For building the simple and intuitive frontend interface.
    PyPDF2: For handling PDF parsing and text extraction.

History

    Initially, the project was built using the CrewAI framework, but due to tool-related issues, it was migrated to LangChain for smoother functionality and a better developer experience.