import RepoCard from "./RepoCard";
import "../assets/styles/repolist.css";

interface Repository {
  name: string;
  url: string;
  description: string;
  stargazers: number;
}

interface RepoListProps {
  repos: Repository[];
  visibleCount: number;
}

const RepoList: React.FC<RepoListProps> = ({ repos, visibleCount }) => {
  return (
    <div className="cards-container">
      {repos.slice(0, visibleCount).map((repo, index) => (
        <RepoCard key={index} repo={repo} />
      ))}
    </div>
  );
};

export default RepoList;
