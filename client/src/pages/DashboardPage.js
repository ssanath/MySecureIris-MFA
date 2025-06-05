// DashboardPage.js - base file
// DashboardPage.js – after successful login
import React from "react";
import "./DashboardPage.css";

function DashboardPage() {
  const email = localStorage.getItem("email");

  return (
    <div className="dashboard-container">
      <h2>Welcome to Secure Iris MFA Dashboard</h2>
      <p>🎉 Successfully authenticated!</p>
      <p>🔒 Logged in as: <strong>{email}</strong></p>

      <div className="dashboard-info">
        <h3>🔍 Confidential Info</h3>
        <p>This dashboard displays sensitive tender information and company documents. Handle with care.</p>
        <ul>
          <li>📁 Tender_001_Confidential.pdf</li>
          <li>📁 Budget2025_Draft.xlsx</li>
          <li>📁 R&D_Tech_Roadmap.docx</li>
        </ul>
      </div>
    </div>
  );
}

export default DashboardPage;
