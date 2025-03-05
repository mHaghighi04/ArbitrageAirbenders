// src/components/About.js
import React from "react";

function About() {
  return (
    <div className="frameAbout">
      <h1 className="aboutTitle">About The Money Printer</h1>
      <p className="aboutText">
        The Money Printer is a revolutionary platform for sports betting arbitrage,
        offering comprehensive analysis and real-time updates to help you maximize your profits.
      </p>
      <p className="aboutText">
        Our mission is to deliver the highest quality data and insights, ensuring you
        always have the best opportunities at your fingertips.
      </p>
      <p className="aboutText">
        We look through live odds and find discrepenses and imbalances in the market. When we find an arbitrage opportunity,
        we calculate how much to bet on each site to maximize guarenteed profits.
      </p>
      <p className="aboutText">
        We only simulate margins given live odds. We are not a bookmaker, betting platform or reponsible for any assets.
      </p>
      <div className="lineAbout"></div>
    </div>
  );
}

export default About;
