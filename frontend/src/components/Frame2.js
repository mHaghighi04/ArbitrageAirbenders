// src/components/Frame2.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Frame2 = () => {
  const [bankroll, setBankroll] = useState(1000);

  return (
    <div className="frame2" style={{ marginTop: "-60px" }}>
      <div className="rectangle4"></div>
      {/* Pass the bankroll value to Frame3 using the state prop */}
      <Link className="buttonNext" to="/frame3" state={{ bankroll }}>
        Next
      </Link>
      <div className="rectangle3"></div>
      <div className="rectangle5"></div>
      <div className="bankrollQuestion">What is your bankroll?</div>
      <input
        className="inputBankroll"
        type="number"
        value={bankroll}
        onChange={(e) => setBankroll(Number(e.target.value))}
      />
      <div className="dollarsign">$</div>
    </div>
  );
};

export default Frame2;
