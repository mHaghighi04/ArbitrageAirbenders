// src/components/Frame4.js
import React from "react";
import { useLocation } from "react-router-dom";

function Frame4() {
  const location = useLocation();
  // Extract the opportunity data from location state (if available)
  const { opportunity } = location.state || {};

  return (
    <div className="frame4" style={{ marginTop: "-70px" }}>
      <div className="textArbitrageFound">Arbitrage Opportunity Found:</div>

      {opportunity ? (
        <div>
          <div id="website1-box" className="website-box">
        <div id="website1-title" className="website-title">
          {opportunity.home_book}:
        </div>
        <div id="bet1" className="bet-text">
          Place ${opportunity.stakes[0]} Bet on {opportunity.home_team}
        </div>
      </div>

      <div id="website2-box" className="website-box">
        <div id="website2-title" className="website-title">
        {opportunity.away_book}:
        </div>
        <div id="bet2" className="bet-text">
        Place ${opportunity.stakes[1]} Bet on {opportunity.away_team}
        </div>
      </div>

      <div id="guaranteed-box" className="container">
        <div id="guaranteed-title" className="text">Guaranteed Returns:</div>
        <div id="margins-text" className="text">{opportunity.profit_margin}% margins = ${opportunity.total_profit}</div>
      </div>
        </div>
      ) : (
        <p>No arbitrage opportunity data received.</p>
      )}

      {/* Existing structure */}
      

      <div className="line2"></div>
    </div>
  );
}

export default Frame4;
