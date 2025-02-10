import { useState } from "react";
import "../assets/styles/searchbar.css";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [input, setInput] = useState("");

  const handleSearch = () => {
    if (!input.trim()) return;
    onSearch(input);
  };

  return (
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
  );
};

export default SearchBar;
