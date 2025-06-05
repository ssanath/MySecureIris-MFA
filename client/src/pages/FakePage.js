// FakePage.js - base file
// FakePage.js – redirect target after honeypot trap
import React from "react";
import "./FakePage.css";

function FakePage() {
  return (
    <div className="fake-container">
      <h2>🚫 Suspicious Access Detected</h2>
      <p>Your session has been terminated due to multiple invalid attempts.</p>
      <p>If you believe this is a mistake, contact admin at <a href="mailto:support@secureiris.com">support@secureiris.com</a></p>
    </div>
  );
}

export default FakePage;
