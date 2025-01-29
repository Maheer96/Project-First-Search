from flask import Flask, request, jsonify
import requests
import os
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Loading .env variables
load_dotenv()

app = Flask(__name__)

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
    Example Output: AI, finance, automation, chatbot, investment
    """
    response = model.generate_content(prompt)
    keywords = response.text.strip().replace("{", "").replace("}", "") # Filter a bunch of stuff since Gemini can be strange
    return jsonify({"keywords": keywords})
    
@app.route('/search', methods=['GET'])
def search_github():
    keywords = request.args.get("keywords")
    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400
    
    query = "+".join(keywords.split())
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"{GITHUB_BASE_URL}?q={query}&sort=stars&order=desc", headers=headers) # Send API token
    
    if response.status_code != 200:
        return jsonify({"error": "GitHub API request failed", "details": response.json()}), 500
    
    return jsonify(response.json())

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
    db.session.commit
    return jsonify({"message": "Repository bookmarked successfully"})

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    bookmarks = Bookmark.query.all()
    return jsonify([{ "repo_name": b.repo_name, "repo_url": b.repo_url, "description": b.description } for b in bookmarks])

if __name__ == '__main__':
    app.run(debug=True)
    
    