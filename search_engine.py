import os
import logging
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from cache import cache_set, cache_get

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv(dotenv_path='./.env')

# Load the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

if not openai_api_key:
    raise EnvironmentError("OpenAI API key not found in environment variables.")

# Initialize OpenAI
openai = OpenAI(api_key=openai_api_key)

# Load and index the document with FAISS
def load_and_index_document(file_path):
    try:
        logging.info(f"Loading document from {file_path}")

        # Check if the index is cached
        cached_index = cache_get(file_path)
        if cached_index:
            logging.info("Loaded index from cache.")
            return cached_index

        # Load document and create FAISS index
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        embeddings = OpenAIEmbeddings()
        index = FAISS.from_documents(docs, embeddings)

        # Cache the index
        cache_set(file_path, index)
        logging.info("Document indexed and cached successfully.")

        return index
    except Exception as e:
        logging.error(f"Error loading document: {str(e)}")
        return None

# Perform semantic search
def perform_semantic_search(index, query, top_k=5):
    try:
        logging.info(f"Performing semantic search for query: {query}")
        retriever = index.as_retriever(search_kwargs={"k": top_k})
        results = retriever.get_relevant_documents(query)
        logging.debug(f"Search results: {results}")  # Debug output
        logging.info(f"Search completed. Found {len(results)} relevant documents.")
        return results
    except Exception as e:
        logging.error(f"Error during semantic search: {str(e)}")
        return None

# Question Answering feature
def question_answering(index, query):
    try:
        logging.info(f"Running question-answering for query: {query}")
        retriever = index.as_retriever()
        chain = RetrievalQA.from_chain_type(llm=openai, retriever=retriever)
        answer = chain.run(query)
        logging.debug(f"Answer generated: {answer}")  # Debug output
        logging.info("Answer generated successfully.")
        return answer
    except Exception as e:
        logging.error(f"Error during question answering: {str(e)}")
        return None
