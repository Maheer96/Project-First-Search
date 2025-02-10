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
GITHUB_BASE_URL = "https://api.github.com/search/repositories" # Base URL for GH Repo API
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
    
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Take this project idea: "{user_input}".
    Extract exactly 3 to 5 relevant keywords, separated by commas, without curly braces, avoiding generic terms.
    Cleverly utilize "OR" if needed. For example if someone asks for "AI finance trading bot", you can say: AI Finance, OR Trading.
    Example Output: AI, finance, automation, chatbot, investment
    """
    response = model.generate_content(prompt)
    keywords = response.text.strip().replace("{", "").replace("}", "") # Filter a bunch of stuff since Gemini output can give unwanted characters
    return jsonify({"keywords": keywords})
    
# Smart searching algorithm
@app.route('/smart_search', methods=['GET'])
def smart_search_github():
    keywords = request.args.get("keywords")
    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400
    
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Given the keywords: {keywords}, classify them into two categories:
    1. High-importance keywords (use AND)
    2. Lower-importance keywords (use OR)
    
    Format your response as:
    AND: (list of 1-2 most important terms)
    OR: (list of 2-4 general terms)
    """
    
    response = model.generate_content(prompt).text.strip()
    
    # Extracting the AND and OR keywords
    and_keywords = []
    or_keywords = []
    
    for line in response.split("\n"):
        if line.startswith("AND:"):
            and_keywords = line.replace("AND:", "").strip().split(", ")
        elif line.startswith("OR:"):
            or_keywords = line.replace("OR:", "").strip().split(", ")   
            
        
    if not and_keywords and not or_keywords:
        return jsonify({"error" : "AI failed to generate valid keywords"}), 500
    
    and_part = " ".join(and_keywords) if and_keywords else ""
    or_part = " OR ".join(or_keywords) if or_keywords else ""
    
    query = f"{and_part} {or_part}".strip()
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    try:
        response = requests.get(f"{GITHUB_BASE_URL}?q={query}&sort=stars&order=desc", headers=headers, timeout=10) # Send API token
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "GitHub API request failed", "details": str(e)}), 500
    
    repos = response.json().get("items", [])
    filtered_repos = []
    for repo in repos:
        description = repo.get("description", "")
        
        # Check for English descriptions
        if description:
            try:
                lang = detect(description)
                if lang != 'en':
                    continue # If not English, skip the description
            except:
                continue # If erroneous, skip the description
            
        filtered_repos.append(
            {
            "name": repo.get("name"),
             "url": repo.get("html_url"),
             "description": description if description else "No description available",
             "stargazers": repo.get("stargazers_count")
             }
        )
    
    return jsonify(filtered_repos) 


@app.route('/bookmark', methods=['POST'])
def bookmark_repo():
    data = request.json
    if not all (k in data for k in ["repo_name", "repo_url", "description"]):
        return jsonify({"error": "Missing data fields"}), 400
    
    new_bookmark = Bookmark(
        repo_name=data['repo_name'],
        repo_url=data['repo_url'],
        description=data['description']
    )
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({"message": "Repository bookmarked successfully"})

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    return jsonify([{ "repo_name": b.repo_name, "repo_url": b.repo_url, "description": b.description } for b in bookmarks])

if __name__ == '__main__':
    app.run(debug=True)