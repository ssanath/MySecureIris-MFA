import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState("");
  const [otpVerified, setOtpVerified] = useState(false);
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [shake, setShake] = useState(false);
  const navigate = useNavigate();

  const logIpAndRedirect = async () => {
    try {
      await axios.post("/api/auth/log-ip", { email });
    } catch (err) {
      console.error("IP logging failed");
    }
    setShake(true);
    setTimeout(() => {
      navigate("/fake");
    }, 1000);
  };

  const handleSendOTP = async () => {
    try {
      const response = await axios.post("/api/auth/send-otp", { email });
      if (response.data.success) {
        setMessage("✅ OTP sent to your email.");
        setOtpSent(true);
        localStorage.setItem("email", email);
      } else {
        setMessage("❌ " + response.data.message);
      }
    } catch {
      setMessage("🚫 Failed to send OTP.");
    }
  };

  const handleVerifyOTP = async () => {
    try {
      const response = await axios.post("/api/auth/verify-otp", { email, otp });

      if (response.data.success) {
        setMessage("✅ OTP verified. Please enter your password.");
        setOtpVerified(true);
      } else {
        setMessage("❌ " + response.data.message);
        if (response.data.message.includes("3 wrong attempts")) {
          await logIpAndRedirect();
        }
      }
    } catch (error) {
      const msg = error.response?.data?.message || "🚫 OTP verification failed.";
      setMessage("❌ " + msg);

      if (error.response?.status === 403) {
        await logIpAndRedirect();
      }
    }
  };

  const handlePasswordSubmit = () => {
    if (!password) {
      setMessage("❌ Please enter your password.");
      return;
    }

    localStorage.setItem("email", email);
    setMessage("✅ Login successful.");
    navigate("/iris-register");
  };

  return (
    <div className="login-container">
      <div className={`login-card ${shake ? "shake" : ""}`}>
        <h2>Login</h2>

        <input
          type="email"
          placeholder="Enter your registered email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
        />

        {!otpSent && <button onClick={handleSendOTP}>Send OTP</button>}

        {otpSent && !otpVerified && (
          <>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              maxLength="6"
              className="otp-input"
            />
            <button onClick={handleVerifyOTP}>Verify OTP</button>
          </>
        )}

        {otpVerified && (
          <>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handlePasswordSubmit}>Login</button>
          </>
        )}

        {message && <p className="message">{message}</p>}

        <p className="login-link">
          Don’t have an account? <a href="/register">Register here</a>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
