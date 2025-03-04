// src/components/Frame4.js
import React from "react";
import { Link } from "react-router-dom";

function Frame4() {
  return (
    <div className="frame4"style={{marginTop: "-70px"}}>
      <div className="textArbitrageFound">
        Arbitrage Opportunity Found:
      </div>

      <div id="website1-box" className="website-box">
        <div id="website1-title" className="website-title">
          Website 1:
        </div>
        <div id="bet1" className="bet-text">
          Place $500 Bet
        </div>
      </div>

      <div id="website2-box" className="website-box">
        <div id="website2-title" className="website-title">
          Website 2:
        </div>
        <div id="bet2" className="bet-text">
          Place $500 Bet
        </div>
      </div>

      <div id="guaranteed-box" className="container">
        <div id="guaranteed-title" className="text">
          Guaranteed Returns:
        </div>
        <div id="margins-text" className="text">
          10% margins = $100
        </div>
      </div>

      <div className="line2"></div>

    </div>
  );
}

export default Frame4;
