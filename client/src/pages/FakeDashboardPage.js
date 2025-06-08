import React from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./FakeDashboardPage.css";

function FakeDashboardPage() {
  const navigate = useNavigate();

  const handleFakeClick = async (action) => {
    const email = localStorage.getItem("email");
    const screenSize = `${window.innerWidth}x${window.innerHeight}`;

    // Optional: Fake data per action for realism
    const fakePayload = {
      "Create VM": { cpu: "2 vCPU", ram: "4GB", region: "us-west-1" },
      "Add Storage": { name: "bucket42", size: "20GB" },
      "Add User": { username: "admin_clone", role: "viewer" },
      "View Billing": { total: "$123.45", cycle: "June 2025" },
      "View Analytics": { cpuUsage: "65%", traffic: "512MB" }
    };

    const logData = {
      route: "/fake-dashboard",
      action: `Tried to ${action}`,
      email: email || "unknown",
      screenSize: screenSize,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      payload: fakePayload[action] || {}
    };

    try {
      await axios.post("http://localhost:5050/api/honeypot/log", logData);
    } catch (error) {
      console.error("📛 Failed to log honeypot activity:", error);
    }

    alert(`${action} simulated.`);
    navigate("/fake"); // Redirect to trap page
  };

  return (
    <div className="fake-dashboard-container">
      <h2>🛡️ Simulated Cloud Dashboard</h2>
      <p className="warning-text">
        ⚠️ You are viewing restricted infrastructure. All actions are being logged.
      </p>

      <div className="fake-buttons">
        <button onClick={() => handleFakeClick("Create VM")}>🔧 Create VM</button>
        <button onClick={() => handleFakeClick("Add Storage")}>📦 Add Storage</button>
        <button onClick={() => handleFakeClick("Add User")}>👤 Add User</button>
        <button onClick={() => handleFakeClick("View Billing")}>💳 View Billing</button>
        <button onClick={() => handleFakeClick("View Analytics")}>📊 View Analytics</button>
      </div>
    </div>
  );
}

export default FakeDashboardPage;
