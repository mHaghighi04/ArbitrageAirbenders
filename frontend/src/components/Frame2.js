// src/components/Frame2.js
import React from 'react';
import { Link } from 'react-router-dom';

const Frame2 = () => {
  // const navigate = useNavigate();

  // const handleNextClick = () => {
  //   console.log("Next button clicked!");
  //   navigate("/frame3");
  // };

  return (
    <div className="frame2" style={{marginTop: "-60px"}}>
      <div className="rectangle4"></div>
      <Link className="buttonNext" to="/frame3">Next</Link>
      <div className="rectangle3"></div>
      <div className="rectangle5"></div>
      <div className="bankrollQuestion">
        What is your bankroll?
      </div>
      <input className="inputBankroll" type="number" defaultValue="1000" />
      <div className="dollarsign">
        $
      </div>
    </div>
  );
};

export default Frame2;
