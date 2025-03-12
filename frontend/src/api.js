const API_URL = "http://127.0.0.1:5000";

export const getProtectedData = async () => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("No token found. Please log in.");
  }

  const response = await fetch(`${API_URL}/protected`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  return response.json();
};
