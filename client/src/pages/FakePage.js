import React from "react";
import "./FakePage.css"; // optional styling

const FakePage = () => {
  return (
    <div className="fake-container">
      <h1>🚫 Access Denied</h1>
      <p>
        Suspicious activity detected. You have been redirected to a secure
        endpoint.
      </p>
      <p>This attempt has been logged for security auditing.</p>
    </div>
  );
};

export default FakePage;
