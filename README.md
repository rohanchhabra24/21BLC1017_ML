<<<<<<< HEAD

# Document Retrieval Project

## Overview

This project provides a document retrieval and question-answering system using a combination of Flask, Redis, FAISS, and OpenAI. The system allows users to upload PDF documents, which are indexed and cached for efficient retrieval. Users can perform semantic searches and ask questions about the content of the uploaded documents.

## Project Structure

- `app.py`: The main Flask application that handles file uploads, search, and question-answering requests.
- `cache.py`: Manages caching of document embeddings using Redis.
- `database.py`: Defines the SQLite database schema for storing document metadata.
- `dockerfile`: Provides the Docker configuration for containerizing the application.
- `search_engine.py`: Contains the logic for indexing documents and performing searches and question-answering using FAISS and OpenAI.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repository/document_retrieval_project.git
   cd document_retrieval_project
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with the following content:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

4. **Initialize the database:**
   ```bash
   python database.py
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The application will be available at `http://127.0.0.1:5001`.

2. **Upload a document:**
   Use `curl` to upload a PDF document:

   ```bash
   curl -F "file=@/path/to/your/document.pdf" http://127.0.0.1:5001/upload
   ```

3. **Perform a search:**
   To perform a semantic search:

   ```bash
   curl "http://127.0.0.1:5001/search?text=your_query&top_k=5&mode=search"
   ```

4. **Ask a question:**
   To ask a question about the document:
   ```bash
   curl "http://127.0.0.1:5001/search?text=your_question&mode=qa"
   ```

## Docker Setup

To build and run the application using Docker:

1. **Build the Docker image:**

   ```bash
   docker build -t document_retrieval_app .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -p 5000:5000 document_retrieval_app
   ```

## Debugging

Ensure that:

- Redis server is running and accessible.
- The `.env` file contains valid environment variables.
- # Document paths and queries are correctly formatted.

# 21BLC1017_ML

(content from the remote branch)

> > > > > > > 889f5fba24ee2ad45d0ff7c13def55d16fca3d45
