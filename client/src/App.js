// App.js - base file
// App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RegisterPage from "./pages/RegisterPage";
import LoginPage from "./pages/LoginPage";
import PasswordPage from "./pages/PasswordPage";
import IrisRegisterPage from "./pages/IrisRegisterPage";
import IrisVerifyPage from "./pages/IrisVerifyPage";
import DashboardPage from "./pages/DashboardPage";
import FakePage from "./pages/FakePage";



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/password" element={<PasswordPage />} />
        <Route path="/iris-register" element={<IrisRegisterPage />} />
        <Route path="/iris-verify" element={<IrisVerifyPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/fake" element={<FakePage />} />


        {/* You can add more routes here later */}
      </Routes>
    </Router>
  );
}

export default App;
