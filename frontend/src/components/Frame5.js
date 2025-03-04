// src/components/Frame5.js
import React from "react";
import { Link } from "react-router-dom";
import "../styles.css"; 

function Frame5() {
  return (
    <div className="frame5"style={{marginTop: "-95px"}}>
      <div className="textArbitrageNotFound">
        No Arbitration Opportunities Found :(
      </div>
      <Link className="textMoreSports" to="/frame2">
        More Sports
      </Link>
      <div className="rectangleMore"></div>
      <div className="linef5"></div>
    </div>

  );
}

export default Frame5;
