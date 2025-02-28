from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyB-Hibm0kUQMo4AU-0lFSjtwBmyO0WBbU8")

# Load documentation from a text file
def read_documentation(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""

# Merge documentation from multiple files
files = ["segment_data.txt", "mparticle.txt", "lytics.txt"]
# Read each file's content and join them with separation for clarity
documentation = "\n\n".join([read_documentation(f) for f in files if read_documentation(f)])

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Root route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Chatbot API. Use /ask to interact with the chatbot."})

@app.route("/ask", methods=["POST"])
def ask_chatbot():
    if not documentation:
        return jsonify({"error": "Documentation not found"}), 500

    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required"}), 400

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are a support chatbot that strictly answers based on the provided documentation.

    Documentation:
    {documentation}

    Question: {question}
    """

    response = model.generate_content(prompt)
    return jsonify({"answer": response.text.strip()})

if __name__ == "__main__":
    app.run(debug=True)
