import "../styles/Global.css";
import "../styles/List.css";
import { useState, useEffect } from "react";

const InventoryList = () => {
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [emails, setEmails] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  const [inventory_list, setInventoryList] = useState([]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  useEffect(() => {
  fetch("/sampleInventorydata.json")
    .then((response) => response.json())
    .then((json) => {
      setData(json);
      const usernames = json.map((data) => data.username);
      setUsernames(usernames);
      const emails = json.map((data) => data.email);
      setEmails(emails);
      const roles = json.map((data) => data.role);
      setRoles(roles);
      const allow_access = json.flatMap((data) => data.allow_access);
      setAccess(allow_access);
      const profile_image_directory = json.map((data) => data.profile_image_directory);
      setProfileImageDirectory(profile_image_directory);
      const inventory_list = json.flatMap((data) => data.inventory_list);
      setInventoryList(inventory_list);

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
        <p>{emails.join(", ")}</p>
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
          <p className="MidPanelTopText">Inventory list:</p>
          <div className="search-bar">
            <input name="search" type="text" placeholder="type to search" ></input>
            <button type="submit"><img src="search-icon.png" alt="Search"></img></button>
          </div>
          <div className="regist-button">
          <button ><img src="../../src/assets/plus.png" alt="Register"></img>Register Inventory</button>
          </div>
          </div>
          <div className="HL1"></div>
            <div className="ContainerColumnContainer " style={{overflow: "hidden",height: "50rem" }}>
              <div className="List" style={{overflowY: "scroll"}}>
                <div className="ContainerRowContainer">
                  <p className="HeaderImage" >Image</p>
                  <p className="HeaderStats" >Name</p>
                  <p className="HeaderStats" >Count</p>
                  <p className="HeaderStats" >ID</p>
                </div>

                {inventory_list.length > 0 ? inventory_list.map((inventory_list, index) => (
                <div className="Box" key={index}>
                  <img src={inventory_list.image} alt="inventory" className="Image"></img>
                  <p className = "Stats">{inventory_list.name}</p>
                  <p className = "Stats">{inventory_list.count}</p>
                  <p className = "Stats">{inventory_list.id}</p>

                  <div className = "container">
                    <button>
                          <span>Edit</span>
                    </button>
                        <div className="dropdown">
                            <ul>
                                <li>
                                  <form action="/edit" method="post">
                                    <button className="edit" type="submit">Add count</button>
                                    <input type="hidden" name="id" value={inventory_list.id} />
                                  </form>
                                </li>
                                <li>
                                <form action="/edit" method="post">
                                    <button className="edit" type="submit">Delete count</button>
                                    <input type="hidden" name="id" value={inventory_list.id} />
                                  </form>
                                </li>
                                <li>
                                <form action="/edit" method="post">
                                    <button className="edit" type="submit">Remove from Inventory</button>
                                    <input type="hidden" name="id" value={inventory_list.id} />
                                  </form>
                                </li>
                            </ul>
                        </div>
                  </div>
                </div>
                )) : <p>No Inventory found</p>}
            </div>  
          </div>
        </div>
      </div>
    </div>
    )
}
export default InventoryList