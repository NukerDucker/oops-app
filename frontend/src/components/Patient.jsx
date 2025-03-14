import "../styles/Global.css";
import "../styles/List.css";
import { useState, useEffect } from "react";
import { 
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  Typography,
  Menu,
  IconButton
} from "@mui/material";

const PatientList = () => {
  // User data states
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [emails, setEmails] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  
  // Patient specific states
  const [patient_list, setPatientList] = useState([]);
  const [filteredPatients, setFilteredPatients] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [inputValue, setInputValue] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Patient management states
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentPatient, setCurrentPatient] = useState({
    id: '',
    name: '',
    age: '',
    gender: '',
    contact: ''
  });
  
  // Menu state for dropdown actions
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedPatientId, setSelectedPatientId] = useState(null);

  // Handle opening/closing dropdown menu
  const handleMenuOpen = (event, patientId) => {
    setAnchorEl(event.currentTarget);
    setSelectedPatientId(patientId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedPatientId(null);
  };

  useEffect(() => {
    // Get authentication token from local storage
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return;
    }

    // Fetch user data using authentication
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
        
        // Set user data from API response
        setUsernames([userData.username]);
        setEmails([userData.email || ""]);
        setRoles([userData.user_type || "User"]);
        setAccess(userData.allow_access || []);
        setProfileImageDirectory([userData.profile_image_directory || "Profile-Icon.png"]);
        
        // Now fetch real patient data from the API
        return fetch("http://127.0.0.1:5000/api/patients", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch patients data");
        }
        return response.json();
      })
      .then(patientData => {
        // Process patient data from API
        const processedPatients = patientData.map(patient => ({
          id: patient.id,
          name: patient.name,
          age: patient.age,
          gender: patient.gender,
          contact: patient.contact,
          history: patient.history,
          // Add a default image path since API doesn't provide images
          image: "Profile-Icon.png" // Default image - make sure this file exists in your public folder
        }));
        
        setPatientList(processedPatients);
        setFilteredPatients(processedPatients);
        setError(null);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
        setError(error.message);
        setIsLoading(false);
      });
  }, []);

  // Search functionality
  useEffect(() => {
    // Filter patients based on search term
    if (searchTerm.trim() === "") {
      setFilteredPatients(patient_list);
    } else {
      const searchTermLower = searchTerm.toLowerCase();
      const filtered = patient_list.filter(patient => 
        patient.name.toLowerCase().includes(searchTermLower) || 
        patient.id.toString().includes(searchTermLower) || 
        patient.age.toString().includes(searchTermLower)
      );
      setFilteredPatients(filtered);
    }
  }, [searchTerm, patient_list]);

  // Handle form submission for adding or editing patients
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEditing) {
      // Update existing patient
      fetch(`http://127.0.0.1:5000/api/patients/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ 
          id: currentPatient.id,
          name: currentPatient.name,
          age: parseInt(currentPatient.age),
          gender: currentPatient.gender,
          contact: currentPatient.contact
        }),
      })
        .then(response => {
          if (!response.ok) throw new Error("Failed to update patient");
          return response.json();
        })
        .then(data => {
          // Update the patient list with the updated patient
          const updatedList = patient_list.map(patient => 
            patient.id === currentPatient.id ? {
              ...patient,
              name: currentPatient.name,
              age: parseInt(currentPatient.age),
              gender: currentPatient.gender,
              contact: currentPatient.contact
            } : patient
          );
          
          setPatientList(updatedList);
          setFilteredPatients(updatedList);
          setShowModal(false);
          alert("Patient updated successfully!");
        })
        .catch(error => {
          console.error("Error updating patient:", error);
          alert("Failed to update patient: " + error.message);
        });
    } else {
      // Add new patient
      fetch("http://127.0.0.1:5000/api/patients/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ 
          name: currentPatient.name,
          age: parseInt(currentPatient.age),
          gender: currentPatient.gender,
          contact: currentPatient.contact
        }),
      })
        .then(response => {
          if (!response.ok) throw new Error("Failed to add patient");
          return response.json();
        })
        .then(data => {
          // Add the new patient to the list
          const newPatient = {
            id: data.id, // Assuming the API returns the new ID
            name: currentPatient.name,
            age: parseInt(currentPatient.age),
            gender: currentPatient.gender,
            contact: currentPatient.contact,
            image: "Profile-Icon.png" // Default image
          };
          
          const newList = [...patient_list, newPatient];
          setPatientList(newList);
          setFilteredPatients(newList);
          setShowModal(false);
          alert("New patient added successfully!");
        })
        .catch(error => {
          console.error("Error adding patient:", error);
          alert("Failed to add patient: " + error.message);
        });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentPatient({
      ...currentPatient,
      [name]: value
    });
  };

  const handleDeletePatient = (patientId) => {
    const userInput = window.prompt("Are you sure? Type 'yes' to confirm:");
    if (userInput && userInput.toLowerCase() === 'yes') {
      fetch(`http://127.0.0.1:5000/api/patients/delete/${patientId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
      })
        .then(response => {
          if (!response.ok) throw new Error("Failed to delete patient");
          return response.json();
        })
        .then(data => {
          const updatedList = patient_list.filter(patient => patient.id !== patientId);
          setPatientList(updatedList);
          setFilteredPatients(updatedList);
          alert("Patient deleted successfully!");
        })
        .catch(error => {
          console.error("Error deleting patient:", error);
          alert("Failed to delete patient: " + error.message);
        });
    }
    handleMenuClose();
  };

  // Handle adding history entry
  const handleAddHistoryEntry = (patientId) => {
    const entry = window.prompt("Enter medical history entry:");
    if (entry && entry.trim() !== "") {
      fetch(`http://127.0.0.1:5000/api/patients/${patientId}/history`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ entry }),
      })
        .then(response => {
          if (!response.ok) throw new Error("Failed to add history entry");
          return response.json();
        })
        .then(data => {
          alert("History entry added successfully!");
        })
        .catch(error => {
          console.error("Error adding history entry:", error);
          alert("Failed to add history entry: " + error.message);
        });
    }
    handleMenuClose();
  };

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

  if (isLoading) return (
    <div className="ContainerPage">
      <div className="loading-container">
        <p>Loading patient data...</p>
      </div>
    </div>
  );

  if (!data) return <p>Loading...</p>;

  return (
    <>
    <head>
      <title>MedSoft - Patient Lists</title>
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
          <div className="ContainerRowContainer" style={{alignItems: "center",marginTop: "2rem"}}>
            <p className="MidPanelTopText">Patients List</p>
            <div className="search-bar">
              <input 
                name="search" 
                type="text" 
                placeholder="Search by name, ID or age" 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <button type="submit"><img src="search-icon.png" alt="Search"></img></button>
            </div>
            <div className="regist-button">
              <button onClick={() => {
                setIsEditing(false);
                setCurrentPatient({
                  id: '',
                  name: '',
                  age: '',
                  gender: '',
                  contact: ''
                });
                setShowModal(true);
              }}>
                <img src="plus.png" alt="Register"></img>Register Patient
              </button>
            </div>
          </div>
          <div className="HL1"></div>
          <div className="ContainerColumnContainer list" style={{overflow: "hidden",height: "50rem" }}>
            <div className="ContainerRowContainer list">
              <p className="HeaderStats id" >ID</p>
              <p className="HeaderImage" >Image</p>
              <p className="HeaderStats" >Name</p>
              <p className="HeaderStats" >Age</p>
            </div>
            <div className="List" style={{overflowY: "scroll"}}>
              {filteredPatients.length > 0 ? filteredPatients.map((patient, index) => (
                <div className="Box" key={index}>
                  <p className="Stats id">{patient.id}</p>
                  <img src={patient.image} alt="Patient" className="Image"></img>
                  <p className="Stats">{patient.name}</p>
                  <p className="Stats">{patient.age}</p>
                  
                  <div className="container">
                    <button onClick={() => {
                      setIsEditing(true);
                      setCurrentPatient({
                        id: patient.id,
                        name: patient.name,
                        age: patient.age.toString(),
                        gender: patient.gender,
                        contact: patient.contact
                      });
                      setShowModal(true);
                    }}>
                      <span>Edit</span>
                    </button>
                    <IconButton 
                      size="small"
                      onClick={(e) => handleMenuOpen(e, patient.id)}
                    >
                      ⋮
                    </IconButton>
                  </div>
                </div>
              )) : <p>No patients found</p>}
            </div>  
          </div>
        </div>
      </div>
      
      {/* Add/Edit Patient Dialog */}
      <Dialog open={showModal} onClose={() => setShowModal(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {isEditing ? 'Edit Patient Information' : 'Register New Patient'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              margin="dense"
              id="name"
              name="name"
              label="Name"
              type="text"
              fullWidth
              variant="outlined"
              value={currentPatient.name}
              onChange={handleInputChange}
              required
              sx={{ mb: 2 }}
            />
            
            <TextField
              margin="dense"
              id="age"
              name="age"
              label="Age"
              type="number"
              fullWidth
              variant="outlined"
              value={currentPatient.age}
              onChange={handleInputChange}
              required
              inputProps={{ min: 0 }}
              sx={{ mb: 2 }}
            />
            
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel id="gender-label">Gender</InputLabel>
              <Select
                labelId="gender-label"
                id="gender"
                name="gender"
                value={currentPatient.gender}
                label="Gender"
                onChange={handleInputChange}
                required
              >
                <MenuItem value="">Select gender</MenuItem>
                <MenuItem value="Male">Male</MenuItem>
                <MenuItem value="Female">Female</MenuItem>
                <MenuItem value="Other">Other</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              margin="dense"
              id="contact"
              name="contact"
              label="Contact"
              type="text"
              fullWidth
              variant="outlined"
              value={currentPatient.contact}
              onChange={handleInputChange}
              required
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowModal(false)} color="primary">
              Cancel
            </Button>
            <Button type="submit" color="primary" variant="contained">
              {isEditing ? 'Update' : 'Add Patient'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
      
      {/* Dropdown Menu for Actions */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleAddHistoryEntry(selectedPatientId)}>Add medical history</MenuItem>
        <MenuItem onClick={() => window.location.href = `/patient/${selectedPatientId}/prescriptions`}>Manage prescriptions</MenuItem>
        <MenuItem onClick={() => window.location.href = `/patient/${selectedPatientId}/medications`}>Manage medications</MenuItem>
        <MenuItem onClick={() => window.location.href = `/patient/${selectedPatientId}/lab-results`}>Manage lab results</MenuItem>
        <MenuItem onClick={() => window.location.href = `/patient/${selectedPatientId}/fees`}>Manage fees</MenuItem>
        <MenuItem onClick={() => window.location.href = `/patient/${selectedPatientId}/treatments`}>Manage treatments</MenuItem>
        <MenuItem onClick={() => handleDeletePatient(selectedPatientId)}>Delete patient</MenuItem>
      </Menu>
    </div>
    </>
  );
}

export default PatientList;