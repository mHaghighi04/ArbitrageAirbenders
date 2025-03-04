// src/components/Frame3.js
import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

const sports = [
  { id: "box1", name: "Football" },
  { id: "box2", name: "Basketball" },
  { id: "box3", name: "Baseball" },
  { id: "box4", name: "Soccer" },
  { id: "box5", name: "Tennis" },
];

function Frame3() {
  const navigate = useNavigate();

  const handleFailClick = () => {
    navigate("/frame5");
  };

  const handleNBAClick = () => {
    navigate("/frame4");
  };


  return (
    <div className="frame3" style={{marginTop: "-60px"}}>
      <div className="pickSportText">Pick a sport:</div>

      {/* <div className="rectangle6"></div> */}

      {/* Row 1 of boxes and labels */}
      {/* <div id="boxf" className="box"></div>
      <div id="textf" className="text">Fail</div>

      <div id="boxnba" className="box"></div>
      <div id="textnba" className="text">NBA</div> */}

      <div
        id="boxf"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={handleFailClick}
      ></div>
      <div
        id="textf"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={handleFailClick}
      >
        Fail
      </div>

      {/* NBA option: when clicked, navigates to Frame4 */}
      <div
        id="boxnba"
        className="box"
        style={{ cursor: "pointer" }}
        onClick={handleNBAClick}
      ></div>
      <div
        id="textnba"
        className="text"
        style={{ cursor: "pointer" }}
        onClick={handleNBAClick}
      >
        NBA
      </div>

      <div id="box1" className="box"></div>
      <div id="text1" className="text">UFC</div>

      <div id="box2" className="box"></div>
      <div id="text2" className="text">NFL</div>

      <div id="box3" className="box"></div>
      <div id="text3" className="text">Sport 3</div>

      <div id="box4" className="box"></div>
      <div id="text4" className="text">Sport 4</div>

      <div id="box5" className="box"></div>
      <div id="text5" className="text">Sport 5</div>

      {/* Row 2 */}
      <div id="box6" className="box"></div>
      <div id="text6" className="text">Sport 6</div>

      <div id="box7" className="box"></div>
      <div id="text7" className="text">Sport 7</div>

      <div id="box8" className="box"></div>
      <div id="text8" className="text">Sport 8</div>

      <div id="box9" className="box"></div>
      <div id="text9" className="text">Sport 9</div>

      <div id="box10" className="box"></div>
      <div id="text10" className="text">Sport 10</div>

      <div id="box11" className="box"></div>
      <div id="text11" className="text">Sport 11</div>

      <div id="box12" className="box"></div>
      <div id="text12" className="text">Sport 12</div>

      {/* Row 3 */}
      <div id="box13" className="box"></div>
      <div id="text13" className="text">Sport 13</div>

      <div id="box14" className="box"></div>
      <div id="text14" className="text">Sport 14</div>

      <div id="box15" className="box"></div>
      <div id="text15" className="text">Sport 15</div>

      <div id="box16" className="box"></div>
      <div id="text16" className="text">Sport 16</div>

      <div id="box17" className="box"></div>
      <div id="text17" className="text">Sport 17</div>

      <div id="box18" className="box"></div>
      <div id="text18" className="text">Sport 18</div>

      <div id="box19" className="box"></div>
      <div id="text19" className="text">Sport 19</div>

      {/* Horizontal line */}
      <div className="line2"></div>

    </div>
  );
}

export default Frame3;
