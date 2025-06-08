import React, { useState, useEffect } from "react";
import axios from "axios";
import "./DashboardPage.css";

function DashboardPage() {
  const email = localStorage.getItem("email");
  const [resources, setResources] = useState([]);
  const [refresh, setRefresh] = useState(false);
  const [deleteName, setDeleteName] = useState("");

  useEffect(() => {
    if (email) {
      axios.get(`http://localhost:5050/api/resource/list/${email}`)
        .then(res => setResources(res.data.resources))
        .catch(err => console.error(err));
    }
  }, [email, refresh]);

  const createResource = (type) => {
    axios.post("http://localhost:5050/api/resource/create", {
      type: type,
      email: email
    }).then(res => {
      alert(res.data.message);
      setRefresh(!refresh);
    }).catch(err => alert("Error creating " + type));
  };

  const deleteResource = () => {
    if (!deleteName) return alert("Enter a resource name");
    axios.delete(`http://localhost:5050/api/resource/delete/${deleteName}`)
      .then(res => {
        alert(res.data.message);
        setDeleteName("");
        setRefresh(!refresh);
      }).catch(err => alert("Delete failed"));
  };

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

      <div className="resource-section">
        <h3>🖥️ Simulated Cloud Resources</h3>
        <button onClick={() => createResource("vm")}>Create VM</button>
        <button onClick={() => createResource("bucket")}>Create Bucket</button>

        <h4>My Resources:</h4>
        <ul>
          {resources.length === 0 ? (
            <li>No resources created yet</li>
          ) : (
            resources.map((res, i) => (
              <li key={i}>{res.name} ({res.type})</li>
            ))
          )}
        </ul>

        <div className="delete-section">
          <input
            type="text"
            value={deleteName}
            onChange={(e) => setDeleteName(e.target.value)}
            placeholder="Enter resource name to delete"
          />
          <button onClick={deleteResource}>Delete</button>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
