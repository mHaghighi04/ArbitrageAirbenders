// src/components/Frame3.js
import React from "react";
// import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useLocation } from 'react-router-dom';

function Frame3() {
  const location = useLocation();
  const { bankroll } = location.state || {};
  const navigate = useNavigate();
  const handleSportClick = async (sportName) => {
    console.log("Sending sport to backend:", sportName);
    try {
      const response = await fetch("http://127.0.0.1:5000/api/check_arbitrage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sport: sportName , amount : bankroll}),
      });
      const data = await response.json();
      console.log(`Backend response for ${sportName}:`, data);

      if (data && Object.keys(data).length > 0) {
        navigate("/frame4", { state: { opportunity: data } });
      } else {
        navigate("/frame5");
      }
    } catch (error) {
      console.error("Error calling backend:", error);
      navigate("/frame5");
    }
  };

  return (
    <div className="frame3" style={{marginTop: "-60px"}}>
      <div className="pickSportText">Pick a sport:</div>

       <div
        id="boxf"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("Fail")}
      ></div>
      <div
        id="textf"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("Fail")}
      >
        Fail
      </div>

      <div
        id="boxnba"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("basketball_nba")}
      ></div>
      <div
        id="textnba"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("basketball_nba")}
      >
        NBA
      </div>

      <div
        id="box1"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("mma_mixed_martial_arts")}
      ></div>
      <div
        id="text1"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("mma_mixed_martial_arts")}
      >
        MMA
      </div>

      <div
        id="box2"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("americanfootball_nfl")}
      ></div>
      <div
        id="text2"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("americanfootball_nfl")}
      >
        NFL
      </div>

      <div
        id="box3"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("baseball_mlb")}
      ></div>
      <div
        id="text3"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("baseball_mlb")}
      >
        MLB
      </div>

      <div
        id="box4"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("icehockey_nhl")}
      ></div>
      <div
        id="text4"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("icehockey_nhl")}
      >
        NHL
      </div>

      <div
        id="box5"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("basketball_ncaab")}
      ></div>
      <div
        id="text5"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={() => handleSportClick("basketball_ncaab")}
      >
        NCAAB
      </div>

      {/* Row 2 */}
      <div id="box6" className="box"></div>
      <div id="text6" className="text">Sport</div>

      <div id="box7" className="box"></div>
      <div id="text7" className="text">Sport</div>

      <div id="box8" className="box"></div>
      <div id="text8" className="text">Sport</div>

      <div id="box9" className="box"></div>
      <div id="text9" className="text">Sport</div>

      <div id="box10" className="box"></div>
      <div id="text10" className="text">Sport</div>

      <div id="box11" className="box"></div>
      <div id="text11" className="text">Sport</div>

      <div id="box12" className="box"></div>
      <div id="text12" className="text">Sport</div>

      {/* Row 3 */}
      <div id="box13" className="box"></div>
      <div id="text13" className="text">Sport</div>

      <div id="box14" className="box"></div>
      <div id="text14" className="text">Sport</div>

      <div id="box15" className="box"></div>
      <div id="text15" className="text">Sport</div>

      <div id="box16" className="box"></div>
      <div id="text16" className="text">Sport</div>

      <div id="box17" className="box"></div>
      <div id="text17" className="text">Sport</div>

      <div id="box18" className="box"></div>
      <div id="text18" className="text">Sport</div>

      <div id="box19" className="box"></div>
      <div id="text19" className="text">Sport</div>

      <div className="line2"></div>

    </div>
  );
}

export default Frame3;
