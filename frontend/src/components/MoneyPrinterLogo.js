// ExampleComponent.js
import React from 'react';
import logo from '../assets/MoneyPrinterLogo.png'; // Renamed the import

function MoneyPrinterLogo() {
  return (
    <div>
      <img src={logo} alt="Money Printer Logo" style={{ width: '300px', display: 'block', margin: '0 auto' }} />
    </div>
  );
}

export default MoneyPrinterLogo;
