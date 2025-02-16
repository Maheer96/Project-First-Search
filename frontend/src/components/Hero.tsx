import { useEffect, useState } from "react";
import "../assets/styles/hero.css";

const Hero: React.FC<{ onFadeComplete: () => void }> = ({ onFadeComplete }) => {
  const [fadeOut, setFadeOut] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      console.log("Hero is fading out...");
      setFadeOut(true);
      setTimeout(() => {
        console.log("Hero fade complete, showing chatbot.");
        onFadeComplete();
      }, 1000);
    }, 2500);
  }, [onFadeComplete]);

  return (
    <div className={`hero-container ${fadeOut ? "fade-out" : ""}`}>
      <h1 className="hero-text">an idea a day keeps the layoff away</h1>
    </div>
  );
};

export default Hero;
