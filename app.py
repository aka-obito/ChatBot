from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure the Google Gemini API
API_KEY = "AIzaSyBpVMSkWj2iBHtpyQHzsC9gsRYYRA8RuhE"
genai.configure(api_key=API_KEY)

# Function to generate schema using Google Gemini API
def generate_schema(prompt):
    try:
        # Use the Gemini model to generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text  # Extract the generated text from the response
    except Exception as e:
        return f"Error: {str(e)}"

# Route to serve the frontend
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to generate schema
@app.route('/generate-schema', methods=['POST'])
def generate_schema_api():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    schema = generate_schema(prompt)
    return jsonify({"schema": schema})

if __name__ == '__main__':
    app.run(debug=True)
