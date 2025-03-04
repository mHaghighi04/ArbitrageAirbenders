// Navbar.js
import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      {/* Left side (logo, title, etc.) */}
      <div className="left-section">
        <div className="printerSprite"></div>
        <div className="titleMoneyPrinter">The Money Printer</div>
        <div className="line1"></div>
      </div>

      {/* Right side (nav links, button) */}
      <div className="right-section">
        <Link className="navHome" to="/">Home</Link>
        <Link className="navAbout" to="/about">About</Link>
        <div className="rectangle1"></div>
        <Link className="buttonGetStarted" to="/frame2">Get Started</Link>
      </div>
    </nav>
  );
};

export default Navbar;
