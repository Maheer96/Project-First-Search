from flask import Flask, request, jsonify
import requests
import os
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from langdetect import detect
from flask_cors import CORS

# Loading .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# APIs and DB setup
GITHUB_BASE_URL = "https://api.github.com/search/repositories"
GEMINI_API = os.getenv("GEMINI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmarks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
genai.configure(api_key=GEMINI_API)

# Db class for SQLAlchemy
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(255), nullable=False)
    repo_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    
with app.app_context():
    db.create_all()

# Setting up routes
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = f"""
    Take this project idea: "{user_input}".
    Extract exactly 3 to 5 **core technical keywords** related to programming languages, frameworks, or technologies.
    Do **NOT** classify them as AND/OR yet.
    Example:
    - Input: "I want to build an AI-powered chatbot for customer support"
    - Output: AI, chatbot, NLP, Python, automation

    Return the keywords in **a comma-separated format**.
    """

    response = model.generate_content(prompt)
    keywords = response.text.strip().replace("{", "").replace("}", "")  # Cleanup
    return jsonify({"keywords": keywords})


# Smart searching algorithm
@app.route('/smart_search', methods=['GET'])
def smart_search_github():
    keywords = request.args.get("keywords")
    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    prompt = f"""
    Given the keywords: "{keywords}", classify them into **AND** (high priority) and **OR** (optional).
    
    - **Programming languages** (Python, C++, Java) → OR
    - **Libraries & frameworks** (TensorFlow, PyTorch, OpenCV) → AND
    - **General topics** (AI, Machine Learning, Robotics) → OR if combined with frameworks.

    Format response as:
    AND: (list of 1-2 most important terms)
    OR: (list of 2-4 general terms)
    """

    response = model.generate_content(prompt).text.strip()

    and_keywords, or_keywords = [], []
    for line in response.split("\n"):
        if line.startswith("AND:"):
            and_keywords = line.replace("AND:", "").strip().split(", ")
        elif line.startswith("OR:"):
            or_keywords = line.replace("OR:", "").strip().split(", ")   

    if not and_keywords and not or_keywords:
        return jsonify({"error": "AI failed to generate valid keywords"}), 500

    query = f"({' AND '.join(and_keywords)}) ({' OR '.join(or_keywords)})"
    print(f"GitHub Search Query: {query}")  # Debugging

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    try:
        response = requests.get(f"{GITHUB_BASE_URL}?q={query}&sort=stars&order=desc", headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "GitHub API request failed", "details": str(e)}), 500

    repos = response.json().get("items", [])
    filtered_repos = []
    for repo in repos:
        description = repo.get("description", "")

        if description:
            try:
                if detect(description) != 'en':
                    continue  # Skip non-English descriptions
            except:
                continue  # Skip descriptions with errors
            
        filtered_repos.append({
            "name": repo["name"],
            "url": repo["html_url"],
            "description": description if description else "No description available",
            "stargazers": repo["stargazers_count"]
        })
    
    return jsonify(filtered_repos)

if __name__ == '__main__':
    app.run(debug=True)
