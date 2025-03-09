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
        <div key={index} className="repo-card"> {/* Wrap RepoCard in div */}
          <RepoCard repo={repo} />
        </div>
      ))}
    </div>
  );
};

export default RepoList;
