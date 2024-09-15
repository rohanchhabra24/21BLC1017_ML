from flask import Flask, request, jsonify
from search_engine import perform_semantic_search, question_answering, load_and_index_document
from cache import cache_set, cache_get
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variable for FAISS index
faiss_index = None  # Initialize this properly in your actual implementation

@app.route('/')
def home():
    return jsonify(message="Welcome to the Document Retrieval API")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"}), 200

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        # Create the 'uploads' directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        
        # Save the file to the 'uploads' directory
        filepath = f"./uploads/{file.filename}"
        try:
            file.save(filepath)
            # Load and index the document here
            global faiss_index
            faiss_index = load_and_index_document(filepath)
            return jsonify({"message": f"File uploaded and indexed successfully at {filepath}"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to process file: {str(e)}"}), 500

# Search/Question Answering endpoint
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('text')
    top_k = int(request.args.get('top_k', 5))
    mode = request.args.get('mode', 'search')  # 'search' or 'qa'
    
    if not query:
        return jsonify({"error": "Query text is missing"}), 400
    
    try:
        if mode == 'search':
            results = perform_semantic_search(faiss_index, query, top_k)
        elif mode == 'qa':
            results = question_answering(faiss_index, query)
        else:
            return jsonify({"error": "Invalid mode"}), 400
        
        return jsonify({"results": results}), 200
    
    except Exception as e:
        return jsonify({"error": f"Failed to perform {mode}: {str(e)}"}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
