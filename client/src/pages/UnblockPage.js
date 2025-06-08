import React, { useState } from "react";
import axios from "axios";
import "./UnblockPage.css";

function UnblockPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleUnblock = async () => {
    try {
      const response = await axios.post("/api/auth/unblock", { email });
      if (response.data.success) {
        setMessage("✅ User unblocked successfully.");
      } else {
        setMessage("❌ " + response.data.message);
      }
    } catch (error) {
      setMessage("❌ Failed to unblock user.");
    }
  };

  return (
    <div className="unblock-container">
      <div className="unblock-card">
        <h2>Unblock User</h2>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={handleUnblock}>Unblock</button>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}

export default UnblockPage;
