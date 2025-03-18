import { useState, useEffect } from 'react';

const useUserData = () => {
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return;
    }

    fetch("http://127.0.0.1:5000/api/user-data", {
      headers: {
        "Authorization": `Bearer ${token}`
      },
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            throw new Error("Your session has expired. Please login again.");
          }
          throw new Error("Failed to fetch data from server");
        }
        return response.json();
      })
      .then((userData) => {
        setData(userData);
        
        setUsernames([userData.username]);
        setRoles([userData.user_type || "User"]);
        setAccess(userData.allow_access || []);
        setProfileImageDirectory([userData.profile_image_directory || "Profile-Icon.png"]);
        
        setError(null);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching user data: ", error);
        setError(error.message);
        setIsLoading(false);
      });
  }, []);

  return {
    data,
    usernames,
    roles,
    access,
    profile_image_directory,
    error,
    isLoading
  };
};

export default useUserData;