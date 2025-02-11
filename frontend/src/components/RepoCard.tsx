import "../assets/styles/repocard.css";

interface Repository {
    name: string;
    url: string;
    description: string;
    stargazers: number;
}

const RepoCard: React.FC<{ repo: Repository }> = ({ repo }) => {
    const truncateText = (text: string, maxLength: number) => {
        return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
    };

    return (
        <div className="card" onClick={() => window.open(repo.url, "_blank")}>
            <h2 className="card-title">{repo.name}</h2>
            <p className="card-description">{truncateText(repo.description, 150)}</p>
            <a href={repo.url} target="_blank" rel="noopener noreferrer" className="card-link" onClick={(e) => e.stopPropagation()}>
                View Repository
            </a>
            <p className="card-stars">⭐ {repo.stargazers} stars</p>
        </div>
    );
};

export default RepoCard;
