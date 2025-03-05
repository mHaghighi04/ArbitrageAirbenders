import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Frame2 = () => {
  // Initialize bankroll as a string to allow empty input
  const [bankroll, setBankroll] = useState("1000");

  // Validate that the input is empty or contains only digits
  const handleChange = (e) => {
    const value = e.target.value;
    if (value === "" || /^[0-9]*$/.test(value)) {
      setBankroll(value);
    }
  };

  return (
    <div className="frame2" style={{ marginTop: "-60px" }}>
      <div className="rectangle4"></div>
      {/* Convert bankroll to a number when passing to Frame3 */}
      <Link className="buttonNext" to="/frame3" state={{ bankroll: Number(bankroll) }}>
        Next
      </Link>
      <div className="rectangle3"></div>
      <div className="rectangle5"></div>
      <div className="bankrollQuestion">What is your bankroll?</div>
      <input
        className="inputBankroll"
        type="number"
        value={bankroll}
        onChange={handleChange}
      />
      <div className="dollarsign">$</div>
    </div>
  );
};

export default Frame2;
