import { useState } from "react";
import axios from "axios";
import "./App.css";

interface Repository {
  name: string;
  url: string;
  description: string;
  stargazers: number;
}

function App() {
  const [input, setInput] = useState<string>("");
  const [repos, setRepos] = useState<Repository[]>([]);
  const [visibleCount, setVisibleCount] = useState<number>(5);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!input) {
      setError("Please enter a project idea.");
      return;
    }
    setError(null);
    setLoading(true);

    try {
      const chatbotResponse = await axios.post("http://127.0.0.1:5000/chatbot", {
        input: input,
      });

      const keywords = chatbotResponse.data.keywords;

      const searchResponse = await axios.get(
        `http://127.0.0.1:5000/smart_search?keywords=${encodeURIComponent(
          keywords
        )}`
      );

      setRepos(searchResponse.data);
      setVisibleCount(5);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch repositories. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setVisibleCount((prev) => prev + 5);
  };

  const truncateText = (text: string, maxLength: number) => {
    if (text.length > maxLength) {
      return text.slice(0, maxLength) + "...";
    }
    return text;
  };

  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-6">Project-First Search</h1>

      <div className="input-section">
        <input
          type="text"
          placeholder="Enter a project idea..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="input-box"
        />
        <button onClick={handleSearch} className="search-btn">
          Search Repositories
        </button>
      </div>

      {loading && <p className="loading-spinner">Loading...</p>}

      {error && <p className="text-red-500">{error}</p>}

      <div className="cards-container">
        {repos.slice(0, visibleCount).map((repo, index) => (
          <div key={index} className="card">
            <h2 className="card-title">{repo.name}</h2>
            <p className="card-description">
              {truncateText(repo.description, 150)} {/* Limit description to 150 characters */}
            </p>
            <a
              href={repo.url}
              target="_blank"
              rel="noopener noreferrer"
              className="card-link"
            >
              View Repository
            </a>
            <p className="card-stars">⭐ {repo.stargazers} stars</p>
          </div>
        ))}
      </div>

      {!loading && repos.length > visibleCount && (
        <button onClick={handleLoadMore} className="load-more-btn">
          Load More
        </button>
      )}
    </div>
  );
}

export default App;
