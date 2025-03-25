import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return f"API Key Loaded: {API_KEY[:5]}... (hidden for security)"

if __name__ == "__main__":
    app.run(debug=True)
