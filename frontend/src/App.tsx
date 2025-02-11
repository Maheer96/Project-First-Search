import { useState } from "react";
import axios from "axios";
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
  const [visibleCount, setVisibleCount] = useState<number>(5);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

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
    <div className="container">
      <h1 className="text-3xl font-bold mb-6">Project-First Search</h1>

      <SearchBar onSearch={handleSearch} />

      {loading && <p className="loading-spinner">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <RepoList repos={repos} visibleCount={visibleCount} />

      <LoadMoreButton onLoadMore={handleLoadMore} hasMore={repos.length > visibleCount} />
    </div>
  );
}

export default App;
