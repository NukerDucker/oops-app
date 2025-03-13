import "../styles/Global.css";
import "../styles/List.css";
import { useState, useEffect } from "react";

const PatientList = () => {
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [emails, setEmails] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  const [patient_list, setPatientList] = useState([]);

  useEffect(() => {
  fetch("/samplePatientdata.json")
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
      const patient_list = json.flatMap((data) => data.patient_list);
      setPatientList(patient_list);

    })
    .catch((error) => console.error("Error fetching data: ", error));
}, []);

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
          <div className="ContainerRowContainer" style={{alignItems: "center",marginTop: "2rem"}}>
          <p className="MidPanelTopText">Patients list:</p>
          <div className="search-bar">
            <input name="search" type="text" placeholder="type to search" ></input>
            <button type="submit"><img src="search-icon.png" alt="Search"></img></button>
          </div>
          <div className="regist-button">
          <button ><img src="../../src/assets/plus.png" alt="Register"></img>Register Patient</button>
          </div>
          </div>
          <div className="HL1"></div>
            <div className="ContainerColumnContainer " style={{overflow: "hidden",height: "50rem" }}>
            <div className="ContainerRowContainer">
                  <p className="HeaderImage" >Image</p>
                  <p className="HeaderStats" >Name</p>
                  <p className="HeaderStats" >Age</p>
                  <p className="HeaderStats" >ID</p>
                </div>
              <div className="List" style={{overflowY: "scroll"}}>
                {patient_list.length > 0 ? patient_list.map((patient_list, index) => (
                <div className="Box" key={index}>
                  <img src={patient_list.image} alt="Patient" className="Image"></img>
                  <p className = "Stats">{patient_list.name}</p>
                  <p className = "Stats">{patient_list.age}</p>
                  <p className = "Stats">{patient_list.id}</p>

                  <div className = "container">
                    <button>
                          <span>Edit</span>
                    </button>
                        <div className="dropdown">
                            <ul>
                                <li>
                                    <a href="#">PatientRecord</a>
                                </li>
                                <li>
                                    <a href="#">Appointment</a>
                                </li>
                                <li>
                                    <a href="#">LabTest</a>
                                </li>
                                <li>
                                    <a href="#">PrescribeMedicine</a>
                                </li>
                                <li>
                                    <a href="#">Invoice</a>
                                </li>
                            </ul>
                        </div>
                  </div>
                </div>
                )) : <p>No patients found</p>}
            </div>  
          </div>
        </div>
      </div>
    </div>
    )
}
export default PatientList