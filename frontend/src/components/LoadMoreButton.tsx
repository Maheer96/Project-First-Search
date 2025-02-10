import "../assets/styles/button.css";

interface LoadMoreProps {
    onLoadMore: () => void;
    hasMore: boolean;
  }
  
  const LoadMoreButton: React.FC<LoadMoreProps> = ({ onLoadMore, hasMore }) => {
    return hasMore ? (
      <button onClick={onLoadMore} className="load-more-btn">
        Load More
      </button>
    ) : null;
  };
  
  export default LoadMoreButton;
  