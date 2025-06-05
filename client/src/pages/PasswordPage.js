import React, { useState } from "react";
import "./PasswordPage.css";

function PasswordPage() {
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handlePasswordSubmit = () => {
    // You can add logic to validate password here
    setMessage("✅ Password accepted. Proceeding to Iris Scan...");
    // Redirect to iris registration if needed
    setTimeout(() => {
      window.location.href = "/iris-register";
    }, 1500);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Enter Password</h2>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handlePasswordSubmit}>Submit Password</button>
        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default PasswordPage;
