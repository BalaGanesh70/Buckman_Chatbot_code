import openai
import os
import logging
from scripts.retrieval.vector_store import retrieve_relevant_docs  # ✅ Corrected import path
from scripts.chatbot.prompt_engineering import create_prompt  # ✅ Corrected import path

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    logging.error("❌ ERROR: OpenAI API key not found. Please check your .env file.")
    exit(1)

def generate_response(user_query):
    """
    Generates a response using Retrieval-Augmented Generation (RAG).
    """
    try:
        # Retrieve relevant documents
        relevant_docs = retrieve_relevant_docs(user_query)
        context = "\n".join(relevant_docs) if relevant_docs else "No relevant documents found."

        # Create a structured prompt
        prompt = create_prompt(user_query, context)

        # Call OpenAI API for response generation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        logging.error(f"❌ OpenAI API Error: {e}")
        return "Sorry, there was an issue connecting to OpenAI. Please try again later."
    
    except Exception as e:
        logging.error(f"❌ Unexpected Error: {e}")
        return "An unexpected error occurred. Please try again."

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye! Have a great day! 👋")
            break
        print("Chatbot:", generate_response(user_input))
