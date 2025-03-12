import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login"); // Redirect to login if no token is found
      return;
    }

    fetch("http://127.0.0.1:5000/protected", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        setMessage(data.message);
        setLoading(false); 
      })
      .catch(() => {
        navigate("/login"); // Redirect to login if token is invalid or fetch fails
      });
  }, [navigate]);

  // While checking token status, show a loading message
  if (loading) {
    return <div>Loading...</div>;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
