# Financial-Report-QA

## Overview

Financial-Report-QA is a project designed to answer questions and extract insights from financial reports. It leverages a combination of advanced techniques to provide accurate and comprehensive information.

## Core Capabilities

*   **Hybrid RAG (Retrieval Augmented Generation):** Combines different retrieval methods to find the most relevant information.
*   **Fine-tuned LLM (Large Language Model):** Utilizes language models specifically trained for financial question answering and insight generation.
*   **Multi-modal:** Supports queries involving both text and tabular data.
*   **Evaluation:** Includes a framework for assessing the system's performance.

## Problem Solved

This project addresses the challenge of efficiently and accurately extracting information and insights from dense and complex financial documents, such as SEC filings. It aims to help users quickly find answers to their financial questions and understand key aspects of a company's performance.

## Key Features

*   **Data Ingestion:** Ingests financial documents (e.g., SEC filings) and data from standard financial QA datasets like FinQA and TatQA.
*   **Knowledge Representation:** Builds a knowledge graph and a vector store from the ingested data to enable efficient information retrieval.
*   **Hybrid RAG Pipeline:** Employs a sophisticated retrieval pipeline that combines vector search (for semantic similarity) and graph traversal (for structured relationships) to locate relevant context for answering questions.
*   **Fine-tuned LLMs:** Uses large language models that have been fine-tuned on financial domain-specific data for improved question answering and insight generation capabilities.
*   **Multi-modal Queries:** Capable of handling questions that require understanding information from both textual and tabular formats within financial reports.
*   **Evaluation Framework:** Provides tools and metrics to evaluate the accuracy and effectiveness of the question-answering system.

## Architecture

The system is composed of the following main components:

*   **Frontend:** A Next.js application provides the user interface for interacting with the system, submitting queries, and viewing results.
*   **Backend:** A Python/FastAPI backend handles the core logic, including:
    *   Data ingestion and preprocessing.
    *   Knowledge graph and vector store management.
    *   The hybrid RAG pipeline.
    *   Interaction with the fine-tuned LLMs.
    *   API endpoints for the frontend to consume.
*   **Containerization:** Docker is used to containerize the frontend and backend components, ensuring consistent deployment and scalability.

The frontend communicates with the backend via REST APIs. The backend processes user queries by first retrieving relevant information using the hybrid RAG pipeline and then feeding this information along with the query to the fine-tuned LLM to generate an answer or insight.

## Setup and Installation

### Prerequisites

*   **Docker and Docker Compose:** Essential for running the containerized application. Ensure you have them installed and configured on your system.
*   **Python:** Python 3.x is required for the backend. If you plan to contribute to backend development or run it outside Docker, ensure you have a compatible version installed.
*   **Node.js and npm/yarn:** Required for the frontend. If you plan to contribute to frontend development or run it separately from Docker.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd Financial-Report-QA
    ```

2.  **Set Up Environment Variables:**
    The backend service requires certain environment variables to function correctly. These can be set up by creating a `.env` file in the `backend` directory or by setting them directly in your environment.

    The following environment variables are used (as seen in `docker-compose.yml`):
    *   `OLLAMA_BASE_URL`: The base URL for the Ollama service. This is pre-configured in `docker-compose.yml` to use the Ollama service within the Docker network (e.g., `http://ollama:11434`).
    *   `NEO4J_URI`: The connection URI for the Neo4j graph database (e.g., `bolt://neo4j:7687`).
    *   `NEO4J_USER`: The username for Neo4j (e.g., `neo4j`).
    *   `NEO4J_PASSWORD`: The password for Neo4j (e.g., `password`).
    *   `PINECONE_API_KEY`: Your API key for the Pinecone vector database.
    *   `PINECONE_INDEX_NAME`: The name of your Pinecone index where document embeddings will be stored.

    Create a file named `.env` in the `backend/` directory with the following content, replacing the placeholder values with your actual credentials for services not managed by Docker Compose (like Pinecone):
    ```env
    OLLAMA_BASE_URL=http://ollama:11434
    NEO4J_URI=bolt://neo4j:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=password
    PINECONE_API_KEY=YOUR_PINECONE_API_KEY
    PINECONE_INDEX_NAME=your-pinecone-index-name
    ```
    **Note:** `OLLAMA_BASE_URL`, `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD` are typically configured to work with the services defined in `docker-compose.yml`. You'll primarily need to provide your `PINECONE_API_KEY` and `PINECONE_INDEX_NAME`.

3.  **Build and Run the Application:**
    Use Docker Compose to build and start all the services:
    ```bash
    docker-compose up --build -d
    ```
    The `-d` flag runs the containers in detached mode.

4.  **Accessing the Application:**
    Once the containers are up and running:
    *   The **Frontend** will be accessible at `http://localhost:3001`.
    *   The **Backend API** will be accessible at `http://localhost:8000/docs` for the Swagger UI.

### Optional: Running Services Separately for Development

If you prefer to run the frontend and backend services separately for development (e.g., for faster iteration or more detailed debugging):

*   **Backend (Python/FastAPI):**
    Navigate to the `backend` directory. It's recommended to use a Python virtual environment.
    ```bash
    cd backend
    # python -m venv venv
    # source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    # Ensure your .env file is configured or environment variables are set
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

*   **Frontend (Next.js):**
    Navigate to the `frontend` directory.
    ```bash
    cd frontend
    npm install # or yarn install
    npm run dev # or yarn dev
    ```
    The frontend development server will typically start on `http://localhost:3000` (or another port if 3000 is busy).

    **Note:** When running services separately, ensure that the backend's `OLLAMA_BASE_URL` and `NEO4J_URI` are correctly pointing to your local Ollama and Neo4j instances, which might be running directly on your host machine or in separate Docker containers. You might need to adjust the `.env` file in the `backend` directory accordingly (e.g., `OLLAMA_BASE_URL=http://localhost:11434`, `NEO4J_URI=bolt://localhost:7687`).

## Project Components

This section provides a brief overview of the key components within the Financial-Report-QA project.

### Backend

*   **Technology:** Python, FastAPI
*   **Core Functionalities:**
    *   Provides API endpoints for the frontend.
    *   Manages data ingestion pipelines for various financial data sources (FinQA, SEC Filings, TatQA).
    *   Includes services for insight generation, table question answering, and the hybrid RAG pipeline.
*   **Key Directories:**
    *   `backend/app/main.py`: The main FastAPI application entry point.
    *   `backend/app/api/`: Contains API route definitions.
    *   `backend/app/pipelines/`: Houses scripts and modules for data ingestion and preprocessing.
    *   `backend/app/services/`: Implements the core business logic, including RAG, QA, and insight generation.

### Frontend

*   **Technology:** Next.js, TypeScript
*   **Core Functionalities:**
    *   Provides the user interface for document uploading.
    *   Allows users to ask questions about the financial reports.
    *   Displays generated insights and answers.
*   **Key Directories:**
    *   `frontend/src/app/page.tsx`: The main application page for user interaction.
    *   `frontend/src/components/`: Contains reusable UI components.

### Datasets

*   **Location:** `datasets/`
*   **Description:** This directory stores various datasets used for training, evaluating, and testing the system.
    *   **FinQA:** A dataset for financial question answering, involving numerical reasoning over financial reports.
    *   **TatQA (Table Text Question Answering):** A dataset focused on answering questions that require understanding both tabular and textual data.
    *   **SEC Filings Data:** May include scripts to download or preprocessed data from SEC filings (e.g., 10-K, 10-Q reports) which are primary sources for financial analysis.
    These datasets are crucial for developing and fine-tuning the models to understand and respond to financial queries accurately.

### Vector Store

*   **Default Local Path (if using ChromaDB with default settings):** `backend/vector_store/` (This path might be created by ChromaDB if it's configured to persist locally and no specific path is set elsewhere for Docker volumes).
*   **Purpose:** The vector store (e.g., ChromaDB, Pinecone) is responsible for storing vector embeddings of the financial documents and other ingested data. These embeddings enable efficient semantic search, allowing the RAG pipeline to quickly retrieve document chunks relevant to a user's query. For a production or scalable setup, a managed service like Pinecone is often used (as indicated by environment variables).

### Docker Configuration

*   **`Dockerfile`:**
    *   Located in `backend/Dockerfile` and `frontend/Dockerfile`.
    *   Each Dockerfile defines the instructions to build the respective service (backend or frontend) into a Docker image. This includes installing dependencies, copying source code, and specifying runtime commands.
*   **`docker-compose.yml`:**
    *   Located in the root directory of the project.
    *   Defines and orchestrates the multi-container application, including the backend, frontend, Ollama, and Neo4j services. It specifies how these services are networked, their environment variables (some of which can be overridden by a `.env` file in the backend), and port mappings.

## Using the Application

This section outlines how to use the key functionalities of the Financial-Report-QA application.

### Data Ingestion

The system supports ingesting data from various financial sources. This process typically involves running Python scripts located in the `backend` directory. These scripts process the data and store it in the knowledge graph (Neo4j) and vector store (e.g., Pinecone or ChromaDB) for retrieval.

*   **Supported Data Sources:**
    *   **FinQA:** A dataset featuring question-answer pairs over financial reports, often including tables and numerical reasoning.
    *   **SEC Filings:** Publicly available financial reports from the U.S. Securities and Exchange Commission (e.g., 10-K annual reports, 10-Q quarterly reports).
    *   **TatQA:** A dataset for table-and-text question answering, requiring comprehension of both structured tables and unstructured text.

*   **Ingestion Scripts (examples, actual script names might vary):**
    *   To ingest the **FinQA** dataset, you would typically run a script like `python run_finqa_ingestion.py` from within the `backend` directory (or its equivalent path if running inside the Docker container). This script processes the FinQA data, extracts relevant information, and populates the knowledge graph and vector store.
    *   To ingest **TatQA** data, a similar script such as `python run_tatqa_ingestion.py` would be used. This script parses the TatQA dataset and integrates it into the system's knowledge base.
    *   For **SEC Filings:**
        1.  **Downloading:** You might first need to download the filings. A script like `datasets/sec_filings/raw/sec_filings_downloader.py` (or a similar utility) would be used to fetch the raw filing documents.
        2.  **Ingestion:** After downloading, a script like `python run_sec_ingestion.py` (from the `backend` directory) would process these filings (e.g., parsing HTML/XBRL, extracting text, tables, and metadata) and load them into the knowledge graph and vector store.

    *Running these scripts requires the backend environment to be set up with necessary dependencies and environment variables (see "Setup and Installation").*

### Interacting with the Application (Frontend/API)

Once the application is running (e.g., via `docker-compose up`), users can interact with it through the frontend interface or by directly calling the backend API.

*   **Typical Frontend Workflow:**
    1.  **Access the Frontend:** Open your web browser and navigate to `http://localhost:3001` (or the configured frontend port).
    2.  **Document Upload (Optional):** The interface may allow users to upload their own financial documents (e.g., PDFs of annual reports). These documents would then be processed and ingested by the backend.
    3.  **Asking Questions:** Users can type questions into a query interface. These questions can pertain to pre-ingested datasets (like FinQA, TatQA, or SEC filings) or recently uploaded documents.
    4.  **Viewing Answers and Insights:** The system will process the question, retrieve relevant information using its hybrid RAG pipeline, and generate an answer or insight using the fine-tuned LLM. The results are then displayed on the frontend.

### Table Question Answering

A key capability of the system is answering questions that require understanding data within tables.
*   Financial datasets like **FinQA** and **TatQA** are rich in tabular data. The ingestion pipelines for these datasets are designed to extract and represent this tabular information effectively.
*   When a question involves specific figures, calculations, or comparisons found in tables within financial reports, the system's multi-modal RAG pipeline and fine-tuned LLM work together to locate the correct table and extract or infer the answer.

### Insight Generation

Beyond direct question answering, the application aims to provide deeper insights from financial data.
*   This could involve summarizing key financial metrics, identifying trends, or extracting important statements from reports based on a general query or a specific document.
*   Insight generation is likely facilitated by specialized services in the backend (`backend/app/services/`) and exposed through API endpoints that the frontend can utilize. Users might interact with this by asking broader questions or selecting an "insight generation" feature on the interface.

*The exact features and user experience will depend on the specific implementation of the frontend and the available API endpoints.*

## Contributing

We welcome contributions to the Financial-Report-QA project! Whether you're fixing a bug, adding a new feature, or improving documentation, your help is appreciated.

### General Guidelines

To contribute, please follow these general steps:

1.  **Fork the Repository:** Create your own fork of the project on GitHub.
2.  **Create a Branch:** Make a new branch in your fork for your specific feature or bug fix (e.g., `feature/new-data-source` or `fix/ingestion-error`).
3.  **Make Your Changes:** Implement your changes, additions, or fixes in your branch.
4.  **Follow Code Style:** Ensure your code adheres to the project's coding style. While specific linters or formatters may not be explicitly stated here, try to maintain consistency with the existing codebase. (If linters like Black or Flake8 for Python, or Prettier for TypeScript are used, they should be mentioned here).
5.  **Write or Update Tests:** Add new tests for any new functionality or update existing tests if your changes affect them. Ensure all tests pass before submitting.
6.  **Submit a Pull Request:** Push your changes to your fork and then submit a pull request to the main repository. Provide a clear description of your changes in the pull request.

### Reporting Issues

If you encounter a bug or have any problems with the application, please report them using the GitHub Issues tracker for the repository.

When reporting an issue, please include:

*   A clear and descriptive title.
*   A detailed description of the issue.
*   Steps to reproduce the bug, if applicable.
*   Information about your environment (e.g., operating system, Docker version, browser version) if relevant.
*   Any error messages or screenshots.

### Suggesting Features

We are open to new ideas and feature suggestions! To suggest a new feature:

1.  **Use GitHub Issues:** Create a new issue in the GitHub Issues tracker.
2.  **Label as Feature Request:** Clearly label the issue as a "feature request" or "enhancement."
3.  **Provide Details:**
    *   A clear and descriptive title for the feature.
    *   A detailed explanation of the proposed feature and why it would be beneficial.
    *   Any potential use cases or examples.
    *   If possible, suggestions on how it might be implemented.

Thank you for considering contributing to Financial-Report-QA!

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file. Please see the LICENSE file for more details.
