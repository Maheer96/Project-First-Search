# 🚀 Project-First Search

![GitHub stars](https://img.shields.io/github/stars/Maheer96/Project-First-Search.svg) 
![GitHub forks](https://img.shields.io/github/forks/Maheer96/Project-First-Search.svg) 
![GitHub license](https://img.shields.io/github/license/Maheer96/Project-First-Search.svg)
![Live Demo](https://img.shields.io/badge/demo-live-green?style=flat&logo=github) 

🌐 **Live at:** https://maheer96.github.io/Project-First-Search/

## 🌟 About the Project

**Project-First Search** is a **smart repository discovery tool** that helps developers find relevant GitHub projects based on their **vague project ideas**. Powered by **Gemini AI & GitHub API**, the platform extracts **technical keywords**, generates **optimized search queries**, and returns the most relevant repositories.

🔹 **No more aimless searching!** Just describe your idea and let the AI do the work.  
🔹 **Get inspired!** Find real-world projects related to your concept.  
🔹 **Simple & sleek UI** with a **smooth hero transition** and a **responsive layout**.  

---

## 🎥 Demo Video

🚀 **Live Application:** https://maheer96.github.io/Project-First-Search/

https://github.com/user-attachments/assets/bf0ccb35-5f73-45c9-858f-b3cd8c7e4e30

---

## 📜 Features

✅ **AI-Powered Smart Search** – Extracts precise keywords for accurate results  
✅ **GitHub API Integration** – Retrieves trending repositories based on search criteria  
✅ **Smooth UI & Hero Transition** – Engaging landing page experience  
✅ **Dynamic Search & Results** – Fades in repositories for a seamless experience  

---

## ⚙️ Configuration & Installation

### **🔧 Prerequisites**
- **Node.js** (v18+)
- **Python** (v3.9+)
- **GitHub API Token** (Set up in `.env`)
- **Google Gemini AI API Key** (Set up in `.env`)

### **🛠️ Backend Setup (Flask)**

1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/project-first-search.git
cd project-first-search
```

2️⃣ **Navigate to Backend Folder**
```bash
cd backend
```

3️⃣ **Create a Virtual Environment**
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # (Mac/Linux) OR venv\Scripts\activate  # (Windows)
```

4️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

5️⃣ **Set Up Environment Variables** Create a .env file in the backend/ directory:
```bash
GEMINI_API_KEY=your-gemini-api-key
GITHUB_TOKEN=your-github-api-token
```

6️⃣ **Run the Backend**
```bash
python api.py
```

This starts the Flask API at `http://127.0.0.1:5000`.

---

### **💻 Frontend Setup (React + Vite)**

1️⃣ **Navigate to the Frontend Folder**
```bash
cd ../frontend
```

2️⃣ **Install Dependencies**
```bash
npm install
```

3️⃣ **Run the Development Server**
```bash
npm run dev
```
Now, visit `http://localhost:5173/` in your browser! 🎉

---

## 🔗 API & Configuration

### 🔑 Environment Variables (`.env`)

Make sure your `.env` file contains the following:

```plaintext
GEMINI_API_KEY=your-gemini-api-key
GITHUB_TOKEN=your-github-api-token
```

### 🛰️ Backend Endpoints

| Method | Endpoint        | Description                                |
|--------|---------------|--------------------------------------------|
| `POST` | `/chatbot`     | Extracts keywords from user input         |
| `GET`  | `/smart_search` | Queries GitHub using optimized search terms |

---

## 📊 Workflow Diagram

<div align="center">
  <img src="https://github.com/user-attachments/assets/76977121-bd7f-4e57-902d-3d881703e1eb" alt="PFS Workflow Diagram">
</div>

---

## 🔮 Future Updates

🛠️ Planned Features

* 🌍 User Profiles – Save search history across devices
* 🎯 Advanced Filtering – Filter by repo size, stars, forks, and language
* 🏆 Trending Projects Integration – Suggest AI-generated project ideas
* ✍🏼 Perfect User Experience –  Current implementation still contains a few bugs in need of fixing

---

🙌 Contributions are welcome! To contribute:

1. Fork the repo
2. Create a feature branch (git checkout -b feature-name)
3. Commit changes (git commit -m "Add feature XYZ")
4. Push to branch (git push origin feature-name)
5. Open a pull request

---

## 📄 License

📝 MIT License - Free to use & modify.

---

## 💌 Contact
📧 Email – [maheerhuq96@gmail.com](maheerhuq96@gmail.com)\
🌐 GitHub – [Maheer96](https://github.com/Maheer96)\
⏩ LinkedIn - [Maheer Huq](https://www.linkedin.com/in/maheer-huq-1aa3b426b/)

---

🚀 Happy coding! 🔥✨
