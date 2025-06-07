import React, { useEffect, useState } from "react";
import axios from "axios";
import "./FakePage.css";

const FakePage = () => {
  const [ip, setIp] = useState("");

  useEffect(() => {
    const fetchIp = async () => {
      try {
        const res = await axios.get("/api/auth/get-ip");
        setIp(res.data.ip);
      } catch (err) {
        console.error("Failed to fetch IP");
      }
    };

    fetchIp();
  }, []);

  return (
    <div className="fake-container">
      <div className="fake-card">
        <h1>🚫 Access Denied</h1>
        <p>Suspicious activity detected. You have been redirected to a secure endpoint.</p>
        <p>This attempt has been logged for security auditing.</p>
        {ip && <p><strong>Blocked IP:</strong> {ip}</p>}
      </div>
    </div>
  );
};

export default FakePage;
