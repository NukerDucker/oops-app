import React, { useState, useEffect } from "react";
import "../styles/Global.css";
import "../styles/Main.css";

const Main = () => {
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [emails, setEmails] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [weekly_tasks, setWeeklyTasks] = useState([]);
  const [emergency_tasks, setEmergencyTasks] = useState([]);

  const [currentSlide, setCurrentSlide] = useState(0);
  const totalSlides = 4;

  //fetch data dynamically
  useEffect(() => {
    fetch("/sampleMaindata.json")
      .then((response) => response.json())
      .then((json) => {
        setData(json);
        const usernames = json.map((data) => data.username);
        setUsernames(usernames);
        const roles = json.map((data) => data.role);
        setRoles(roles);
        const allow_access = json.flatMap((data) => data.allow_access);
        setAccess(allow_access);
        const profile_image_directory = json.map((data) => data.profile_image_directory);
        setProfileImageDirectory(profile_image_directory);
        const tasks = json.flatMap((data) => data.tasks);
        setTasks(tasks);
        const weekly_tasks = json.flatMap((data) => data.weekly_tasks);
        setWeeklyTasks(weekly_tasks);
        const emergency_tasks = json.flatMap((data) => data.emergency_tasks);
        setEmergencyTasks(emergency_tasks);

      })
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide % totalSlides) + 1);
    }, 7000); // Change slide every 7 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
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
            <div className="Link mainButton">
          <a href="/main">Main</a>
          </div>
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
          <p className="welcome-text">Welcome Back!, {usernames[0]}</p>
          </div>
          <div className="ContainerRowContainer" style={{justifyContent: "flex-start"}}>
            <div className="search-bar">
              <input name="search" type="text" placeholder="Search" />
              <button type="submit">
                <img src="search-icon.png" alt="Search" />
              </button>
            </div>
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

          {/* Add right banner here if needed */}
        </div>
      </div>
  );
};

export default Main;