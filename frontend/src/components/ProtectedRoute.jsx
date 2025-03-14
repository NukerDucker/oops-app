import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    let isMounted = true;
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/login");
      return;
    }

    const verifyToken = async () => {
      try {
        const res = await fetch("http://127.0.0.1:5000/protected", {
          headers: {
            "Authorization": `Bearer ${token}`
          },
        });

        if (!res.ok) throw new Error("Unauthorized");

        if (isMounted) setLoading(false);
      } catch (error) {
        localStorage.removeItem("token");
        navigate("/login");
      }
    };

    verifyToken();

    return () => {
      isMounted = false; // Cleanup to prevent state update on unmounted component
    };
  }, [navigate]);

  if (loading) return <div>Loading...</div>;

  return <>{children}</>;
};

export default ProtectedRoute;
