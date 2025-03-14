import React, { useState, useEffect } from "react";
import "../styles/Global.css";
import "../styles/Main.css";

const Main = () => {
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [weekly_tasks, setWeeklyTasks] = useState([]);
  const [error, setError] = useState(null);

  const [currentSlide, setCurrentSlide] = useState(0);
  const totalSlides = 4;
  
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
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
        setTasks(userData.tasks || []);
        setWeeklyTasks(userData.weekly_tasks || []);
        
        setError(null);
      })
      .catch((error) => {
        console.error("Error fetching user data: ", error);
        setError(error.message);
      });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide % totalSlides) + 1);
    }, 7000); // Change slide every 7 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  // Show error message if there was an error fetching data
  if (error) return (
    <div className="ContainerPage">
      <div className="error-container">
        <p className="error-message">{error}</p>
        <button onClick={() => window.location.href = "/login"} className="login-button">
          Go to Login
        </button>
      </div>
    </div>
  );

  if (!data) return <p className="Loading">Loading...</p>;

  return (
    <>
<head>
      <title>MedSoft - Main</title>
    
    </head>
    <div className="ContainerPage">
      <div className="ContainerPageUIBoundary">
        <div className="ContainerPageLeftPanel">
          <img src="logo.png" className="logo" alt="Logo" />
          <p>{roles.join(", ")}</p>
          <img
            src={profile_image_directory[0]}
            className="profile-icon"
            alt="Profile"
          />
          <p>{usernames.join(", ")}</p>
          <div className="HL1"></div>

          <div className="ContainerColumnContainer" style={{alignItems: "center"}}>
          {access.map((access, index) => (
                  <div className="Link" key={index}>
                    <a href={access.access_link}>{access.access}</a>
                  </div>
          ))}

          </div>
        </div>

        <div className="VL1"></div>

        <div className="ContainerPageMiddlePanel">
          <div className="ContainerRowContainer" style={{justifyContent: "flex-start"}}>
          <p className="welcome-text">Welcome Back!, <strong>{usernames[0]}</strong></p>
          </div>

          <div className="ContainerColumnContainer" style={{height: "40%"}}>
            <div className="SlidesViewPort">
              <div className="SlidesContainer" style={{ transform: `translateX(-${(currentSlide%totalSlides) * 25}%)` }}>
                  <div className="SlideContent">
                    <h2>Slide 1</h2>
                    <p>Content for Slide 1</p>
                  </div>
                  <div className="SlideContent">
                    <h2>Slide 2</h2>
                    <p>Content for Slide 2</p>
                  </div>
                  <div className="SlideContent">
                    <h2>Slide 3</h2>
                    <p>Content for Slide 3</p>
                  </div>
                  <div className="SlideContent">
                    <h2>Slide 4</h2>
                    <p>Content for Slide 4</p>
                  </div>
              </div>
              {/* Navigation Bullets */}
            </div>
            <div className = "ContainerRowContainer" style={{justifyContent: "center"}}>
              <div id="bullets">
                {[1, 2, 3, 4].map((index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentSlide(index - 1)}
                    className={index - 1 === currentSlide ? "active" : ""}
                  ></button>
                ))}
              </div>
            </div>
          </div>

          <div className="ContainerColumnContainer taskContainer task">
            <div className="ContainerRowContainer">
              <div className="ContainerColumnContainer task " style={{width: "50%"}}>
                {tasks.map((task, index) => (
                  <div className="TaskBox" key={index}>
                    <h1>Upcoming Appointment #{index + 1}</h1>
                    <h2>Title: {task.title}</h2>
                    <p>Description: {task.description}</p>
                  </div>
                ))}
              </div>
              <div className="ContainerColumnContainer task" style={{width: "50%"}}>
              {weekly_tasks.map((weekly_task, index) => (
                  <div className="TaskBox" key={index}>
                    <h1>Weekly Tasks #{index + 1}</h1>
                    <h2>Title: {weekly_task.title}</h2>
                    <p>Description: {weekly_task.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default Main;