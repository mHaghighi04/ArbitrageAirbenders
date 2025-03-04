// src/components/Frame1.js
import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

function Frame1() {
  return (
    <div className="frame1" style={{marginTop: "-70px"}}>
      <div className="moneyPrinterLogo"></div>
      <div className="headline">
        The Money Printer: The premier platform for sports betting arbitrage
      </div>
      <div className="paragraph">
        Welcome to The Money Printer, your ultimate destination to guaranteed returns from your favorite activity. Our cutting-edge platform empowers you to capitalize on the dynamic odds and maximize your profits with our comprehensive analysis and real-time updates.
      </div>
      <div className="rectangle2"></div>
      <Link className="buttonExploreSports" to="/frame2">Explore Sports</Link>
    </div>
  );
}

export default Frame1;
