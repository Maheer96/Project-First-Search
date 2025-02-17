import { FaHome, FaGithub } from "react-icons/fa"; // Import logos for home and GitHub icons
import "../assets/styles/navbar.css";
import logo from "../assets/images/logo.png";

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <button className="nav-btn" onClick={() => window.location.reload()}>
        <FaHome className="icon" />
      </button>

      <img src={logo} alt="Logo" className="navbar-logo" />

      <a href="https://github.com/Maheer96/Project-First-Search" target="_blank" rel="noopener noreferrer" className="nav-btn">
        <FaGithub className="icon" />
      </a>
    </nav>
  );
};

export default Navbar;
