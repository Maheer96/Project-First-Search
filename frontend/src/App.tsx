import { useState, useEffect } from "react";
import axios from "axios";
import Hero from "./components/Hero";
import SearchBar from "./components/SearchBar";
import RepoList from "./components/RepoList";
import LoadMoreButton from "./components/LoadMoreButton";
import "./assets/styles/global.css";

interface Repository {
  name: string;
  url: string;
  description: string;
  stargazers: number;
}

function App() {
  const [repos, setRepos] = useState<Repository[]>([]);
  const [visibleCount, setVisibleCount] = useState<number>(6);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [showChatbot, setShowChatbot] = useState(false);

  useEffect(() => {
    console.log("Chatbot visibility:", showChatbot);
  }, [showChatbot]);

  const handleSearch = async (query: string) => {
    setError(null);
    setLoading(true);

    try {
      const chatbotResponse = await axios.post("http://127.0.0.1:5000/chatbot", { input: query });
      const keywords = chatbotResponse.data.keywords;

      const searchResponse = await axios.get(`http://127.0.0.1:5000/smart_search?keywords=${encodeURIComponent(keywords)}`);
      setRepos(searchResponse.data);
      setVisibleCount(6);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch repositories. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleLoadMore = () => {
    setVisibleCount((prev) => prev + 6);
  };

  return (
    <div>
      {!showChatbot && <Hero onFadeComplete={() => setTimeout(() => setShowChatbot(true), 500)} />}
      <div className={`app-container ${showChatbot ? "visible" : ""}`}>
        <h1 className="title-text">Project-First Search</h1>
        <SearchBar onSearch={handleSearch} />
        {loading && <p className="loading-spinner">Loading...</p>}
        {error && <p className="text-red-500">{error}</p>}
        <RepoList repos={repos} visibleCount={visibleCount} />
        <LoadMoreButton onLoadMore={handleLoadMore} hasMore={repos.length > visibleCount} />
      </div>
    </div>
  );
}

export default App;
