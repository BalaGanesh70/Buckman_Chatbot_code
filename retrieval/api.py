import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS  
from dotenv import load_dotenv  
from scripts.ingestion.data_ingestion import DataIngestion  
from scripts.retrieval.vector_store import retrieve_relevant_docs  

# ✅ Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ ERROR: OpenAI API key is missing! Check your .env file.")
    exit(1)

openai.api_key = openai_api_key

app = Flask(__name__)
CORS(app)

# ✅ Fix: Ensure correct file path
DATASET_PATH = os.path.abspath(os.path.join("data", "Students_Grading_Dataset.csv"))

# ✅ Initialize Data Ingestion
data_ingestion = DataIngestion(file_path=DATASET_PATH)  
text_data = data_ingestion.load_data()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the RAG Chatbot API!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Invalid request, 'query' is required"}), 400
    
    user_query = data["query"].strip().lower()

    # ✅ Retrieve relevant text from stored data
    relevant_text = retrieve_relevant_docs(user_query)
    
    print(f"🔍 Retrieved Text: {relevant_text}")

    if not relevant_text:
        return jsonify({"answer": "I couldn't find relevant data in the dataset. Please ask something else."})

    # ✅ Construct prompt
    prompt = f"Use the following extracted data to answer the question:\n\n{relevant_text}\n\nUser: {user_query}\nAI:"

    try:
        # ✅ Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a knowledgeable assistant."},
                      {"role": "user", "content": prompt}]
        )

        answer = response["choices"][0]["message"]["content"]

        print(f"✅ Chatbot Response: {answer}")  # ✅ Debugging log
        return jsonify({"answer": answer})

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # ✅ Debugging log
        return jsonify({"error": f"Failed to generate response: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
