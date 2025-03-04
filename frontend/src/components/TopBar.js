// src/components/TopBar.js
import React from 'react';

const TopBar = () => {
  const topBarStyle = {
    backgroundColor: '#FFD700', // gold yellow color
    height: '80px',             // adjust the height as needed
    width: '100%',
    position: 'fixed',          // sticks the bar to the top
    top: 0,
    left: 0,
    zIndex: 9999,               // ensures it stays on top of other elements
  };

  return <div style={topBarStyle}></div>;
};

export default TopBar;
