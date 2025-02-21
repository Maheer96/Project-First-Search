import { FaHome, FaGithub, FaRedo } from "react-icons/fa";
import "../assets/styles/navbar.css";
import logo from "../assets/images/logo.png";

interface NavbarProps {
  onReplayHero: () => void;
  onGoHome: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onReplayHero, onGoHome }) => {
  return (
    <nav className="navbar">
      <button className="nav-btn" onClick={onGoHome} title="New Idea?">
        <FaHome className="icon" />
      </button>

      <img src={logo} alt="Logo" className="navbar-logo" />

      <button className="nav-btn" onClick={onReplayHero} title="Rewind!">
        <FaRedo className="icon" />
      </button>

      <a href="https://github.com/maheer96/project-first-search" target="_blank" rel="noopener noreferrer" className="nav-btn" title="Repo!">
        <FaGithub className="icon" />
      </a>
    </nav>
  );
};

export default Navbar;
