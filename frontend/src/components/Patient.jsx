import React, { useState, useEffect } from "react";
import { 
  Grid2, Typography, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, Divider, Button, AppBar, Box, Toolbar, 
  InputBase, TextField, Dialog, DialogTitle, DialogContent, DialogActions, 
  FormControl, InputLabel, Select, MenuItem, List, ListItem, ListItemText, 
  styled, alpha 
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import useUserData from "../hooks/useUserData";
import usePatientData from "../hooks/usePatientData";
import useMedicalServices from "../hooks/useMedicalServices";
import UserProfile from "./UserProfile";
import "../styles/Inventory.css";

// Styled search components (same as Inventory)
const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));

const PatientList = () => {
  // Use custom hooks
  const { 
    usernames, roles, access, profile_image_directory, 
    error: userDataError, isLoading: userDataLoading 
  } = useUserData();
  
  const {
    filteredPatients, searchTerm, setSearchTerm,
    error: patientError, isLoading: patientLoading,
    addPatient, updatePatient, deletePatient
  } = usePatientData();
  
  const {
    medications, doctors, selectedMedication, selectedDoctor,
    prescriptionQuantity, calculatedFee, handleMedicationChange,
    handleQuantityChange, createPrescription
  } = useMedicalServices();

  // Local UI state
  const [selectedPatientDetails, setSelectedPatientDetails] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showPatientInfoModal, setShowPatientInfoModal] = useState(false);
  const [showPrescriptionModal, setShowPrescriptionModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState(null);
  const [currentPatient, setCurrentPatient] = useState({
    id: '',
    name: '',
    age: '',
    gender: '',
    contact: ''
  });

  // Handle form submission for adding or editing patients
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEditing) {
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
          // Use the hook function instead of direct state manipulation
          updatePatient(currentPatient);
          setShowModal(false);
          alert("Patient updated successfully!");
        })
        .catch(error => {
          console.error("Error updating patient:", error);
          alert("Failed to update patient: " + error.message);
        });
    } else {
      // Add new patient using hook
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
          
          addPatient(newPatient);
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
    if(window.confirm("Are you sure you want to delete this patient?")) {
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
          deletePatient(patientId);
          alert("Patient deleted successfully!");
        })
        .catch(error => {
          console.error("Error deleting patient:", error);
          alert("Failed to delete patient: " + error.message);
        });
    }
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
  };

  // Add this function to handle viewing patient details
  const handleViewPatientDetails = (patient) => {
    // Fetch detailed patient data including history, prescriptions, and lab results
    fetch(`http://127.0.0.1:5000/api/patients/${patient.id}/details`, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to load patient details");
        return response.json();
      })
      .then(data => {
        setSelectedPatientDetails(data);
        setShowPatientInfoModal(true);
      })
      .catch(error => {
        console.error("Error loading patient details:", error);
        alert("Failed to load patient details: " + error.message);
      });
  };

  // Modify the createPrescription function in useMedicalServices or add a wrapper function
  const handleCreatePrescription = () => {
    if (!selectedMedication || !selectedDoctor || !currentPatient.id) {
      alert("Please select medication, doctor, and ensure patient is selected");
      return;
    }
    
    fetch(`http://127.0.0.1:5000/api/prescriptions/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({
        patient_id: currentPatient.id,
        medication_id: selectedMedication,
        doctor_id: selectedDoctor,
        quantity: parseInt(prescriptionQuantity)
      }),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to create prescription");
        return response.json();
      })
      .then(data => {
        setShowPrescriptionModal(false);
        alert("Prescription created successfully!");
      })
      .catch(error => {
        console.error("Error creating prescription:", error);
        alert("Failed to create prescription: " + error.message);
      });
  };

  // Handle errors from user data hook
  if (userDataError) return (
    <div className="ContainerPage">
      <div className="error-container">
        <p className="error-message">{userDataError}</p>
        <Button 
          variant="contained" 
          onClick={() => window.location.href = "/login"}
        >
          Go to Login
        </Button>
      </div>
    </div>
  );

  // Handle errors from patient data
  if (patientError) return (
    <div className="ContainerPage">
      <div className="error-container">
        <p className="error-message">{patientError}</p>
        <Button 
          variant="contained" 
          onClick={() => window.location.href = "/login"}
        >
          Go to Login
        </Button>
      </div>
    </div>
  );

  // Handle loading states
  if (userDataLoading || patientLoading) return (
    <div className="ContainerPage">
      <div className="loading-container">
        <Typography variant="body1">Loading Data...</Typography>
      </div>
    </div>
  );

  return (
      <div className="parent-card">
        <Grid2 container spacing={2} sx={{ height: '100%',width: '100%' }}>
          {/* Left column - User profile using the UserProfile component */}
          <UserProfile 
            usernames={usernames}
            roles={roles}
            access={access}
            profile_image_directory={profile_image_directory}
          />
          
          {/* Right column - Patient table */}
          <Grid2 xs={8} sx={{ display: 'flex', flexDirection: 'column', padding: 2, width: '85%' }}>
            {/* Search bar header */}
            <Box sx={{ flexGrow: 0, marginBottom: 2, borderRadius: '30px', backgroundColor: 'none' }}>
              <AppBar position="static" sx={{ backgroundColor: 'none'}}>
                <Toolbar sx={{ backgroundColor: 'none'}}>
                  <Typography
                    variant="h6"
                    noWrap
                    component="div"
                    sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
                  >
                    Patients
                  </Typography>
                  <Search>
                    <SearchIconWrapper>
                      <SearchIcon />
                    </SearchIconWrapper>
                    <StyledInputBase
                      placeholder="Search…"
                      inputProps={{ 'aria-label': 'search' }}
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </Search>
                  <Button 
                    variant="contained" 
                    onClick={() => {
                      setIsEditing(false);
                      setCurrentPatient({
                        id: '',
                        name: '',
                        age: '',
                        gender: '',
                        contact: ''
                      });
                      setShowModal(true);
                    }}
                    sx={{ 
                      ml: 2, 
                      backgroundColor: 'var(--accent-color)', 
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    Register Patient
                  </Button>
                </Toolbar>
              </AppBar>
            </Box>

            {/* Table container */}
            <div className="table-container" style={{ 
              flexGrow: 1, 
              width: '100%', 
              height: 'calc(90vh - 150px)',
              overflow: 'hidden',
            }}>
              <TableContainer 
                component={Paper} 
                sx={{ 
                  height: '100%',
                  maxHeight: '100%',
                  overflow: 'auto',
                  mt: 2,
                  backgroundColor: 'transparent',
                  boxShadow: 'none'
                }}
              >
                <Table stickyHeader aria-label="patient table">
                  <TableHead>
                    <TableRow>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '60px' }}>ID</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '80px' }}>Image</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Patient Name</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold' }}>Age</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Gender</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Contact</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '120px' }}>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredPatients.length > 0 ? (
                      filteredPatients.map((patient) => (
                        <TableRow 
                          key={patient.id}
                          sx={{ 
                            '&:hover': { backgroundColor: 'rgba(236, 230, 240, 0.4)' }, 
                            borderRadius: '15px',
                            mb: 1,
                            border: '2px solid var(--border-color)'
                          }}
                        >
                          <TableCell align="center">{patient.id}</TableCell>
                          <TableCell align="center">
                            <img 
                              src={patient.image} 
                              alt="patient" 
                              style={{ width: '50px', height: '50px', borderRadius: '50%' }}
                            />
                          </TableCell>
                          <TableCell>
                            <Typography 
                              variant="body1" 
                              sx={{ 
                                cursor: 'pointer', 
                                textDecoration: 'underline',
                                color: 'primary.main',
                                '&:hover': { color: 'primary.dark' }
                              }}
                              onClick={() => handleViewPatientDetails(patient)}
                            >
                              {patient.name}
                            </Typography>
                          </TableCell>
                          <TableCell align="center">{patient.age}</TableCell>
                          <TableCell>{patient.gender}</TableCell>
                          <TableCell>{patient.contact}</TableCell>
                          <TableCell align="center">
                            <Button
                              variant="contained"
                              size="small"
                              sx={{ color: 'white' }}
                              onClick={() => {
                                setSelectedPatientId(patient.id);
                                setIsEditing(true);
                                setCurrentPatient({
                                  id: patient.id,
                                  name: patient.name,
                                  age: patient.age.toString(),
                                  gender: patient.gender,
                                  contact: patient.contact
                                });
                                setShowModal(true);
                              }}
                            >
                              Edit Patient
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={7} align="center">No patients found</TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </div>
          </Grid2>
        </Grid2>
        
        {/* Dialog for Add/Edit Form */}
        <Dialog 
          open={showModal} 
          onClose={() => setShowModal(false)} 
          maxWidth="md" 
          fullWidth
        >
          <DialogTitle>
            {isEditing ? 'Manage Patient Information' : 'Register New Patient'}
          </DialogTitle>
          <form onSubmit={handleSubmit}>
            <DialogContent>
              <Grid2 container spacing={2}>
                <Grid2 item xs={6}>
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
                  />
                </Grid2>
                <Grid2 item xs={3}>
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
                  />
                </Grid2>
                <Grid2 item xs={3}>
                  <FormControl fullWidth sx={{ mt: 1 }}>
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
                </Grid2>
                <Grid2 item xs={6}>
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
                </Grid2>
                <Grid2 item xs={6}>
                  <FormControl fullWidth sx={{ mt: 1 }}>
                    <InputLabel id="medication-label">Medication</InputLabel>
                    <Select
                      labelId="medication-label"
                      id="medication"
                      name="medication"
                      label="Medication"
                      value={selectedMedication}
                      onChange={handleMedicationChange}
                    >
                      <MenuItem value="">Select medication</MenuItem>
                      {medications.map(med => (
                        <MenuItem key={med.id} value={med.id}>
                          {med.name} - ${med.price}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid2>
                
                <Grid2 item xs={12}>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="h6">Patient Management</Typography>
                </Grid2>
                
                <Grid2 item xs={6}>
                  <Button 
                    fullWidth
                    variant="outlined" 
                    onClick={() => handleAddHistoryEntry(currentPatient.id)}
                  >
                    Add Medical History
                  </Button>
                </Grid2>
                <Grid2 item xs={6}>
                  <Button 
                    fullWidth
                    variant="outlined" 
                    onClick={() => {
                      setShowModal(false);
                      setShowPrescriptionModal(true);
                    }}
                  >
                    Order Prescription
                  </Button>
                </Grid2>
                <Grid2 item xs={6}>
                  <Button 
                    fullWidth
                    variant="outlined" 
                    onClick={() => window.location.href = `/patient/${currentPatient.id}/lab-results`}
                  >
                    Manage Lab Results
                  </Button>
                </Grid2>
                <Grid2 item xs={6}>
                  <Button 
                    fullWidth
                    variant="outlined" 
                    onClick={() => window.location.href = `/patient/${currentPatient.id}/fees`}
                  >
                    Manage Fees
                  </Button>
                </Grid2>
                <Grid2 item xs={6}>
                  <Button 
                    fullWidth
                    variant="outlined" 
                    onClick={() => window.location.href = `/patient/${currentPatient.id}/treatments`}
                  >
                    Manage Treatments
                  </Button>
                </Grid2>
              </Grid2>
            </DialogContent>
            <DialogActions sx={{ justifyContent: 'space-between', px: 3, pb: 2 }}>
              {isEditing && (
                <Button 
                  onClick={() => {
                    if(window.confirm("Are you sure you want to delete this patient?")) {
                      handleDeletePatient(currentPatient.id);
                      setShowModal(false);
                    }
                  }} 
                  color="error" 
                  variant="contained"
                >
                  Delete
                </Button>
              )}
              <Box>
                <Button onClick={() => setShowModal(false)} color="primary" sx={{ mr: 1 }}>
                  Cancel
                </Button>
                <Button type="submit" color="primary" variant="contained">
                  {isEditing ? 'Update' : 'Add Patient'}
                </Button>
              </Box>
            </DialogActions>
          </form>
        </Dialog>

        {/* Patient Info Modal */}
        <Dialog 
          open={showPatientInfoModal} 
          onClose={() => setShowPatientInfoModal(false)} 
          maxWidth="md" 
          fullWidth
        >
          {selectedPatientDetails && (
            <>
              <DialogTitle>
                Patient Information
              </DialogTitle>
              <DialogContent>
                <Grid2 container spacing={2}>
                  <Grid2 item xs={12} display="flex" justifyContent="center" mb={2}>
                    <img 
                      src={selectedPatientDetails.image} 
                      alt="patient" 
                      style={{ width: '100px', height: '100px', borderRadius: '50%' }}
                    />
                  </Grid2>
                  <Grid2 item xs={6}>
                    <Typography variant="subtitle2">Name</Typography>
                    <Typography variant="body1" gutterBottom>{selectedPatientDetails.name}</Typography>
                  </Grid2>
                  <Grid2 item xs={3}>
                    <Typography variant="subtitle2">Age</Typography>
                    <Typography variant="body1" gutterBottom>{selectedPatientDetails.age}</Typography>
                  </Grid2>
                  <Grid2 item xs={3}>
                    <Typography variant="subtitle2">Gender</Typography>
                    <Typography variant="body1" gutterBottom>{selectedPatientDetails.gender}</Typography>
                  </Grid2>
                  <Grid2 item xs={6}>
                    <Typography variant="subtitle2">Contact</Typography>
                    <Typography variant="body1" gutterBottom>{selectedPatientDetails.contact}</Typography>
                  </Grid2>
                  <Grid2 item xs={6}>
                    <Typography variant="subtitle2">Patient ID</Typography>
                    <Typography variant="body1" gutterBottom>{selectedPatientDetails.id}</Typography>
                  </Grid2>
                  
                  <Grid2 item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="h6">Medical History</Typography>
                    {selectedPatientDetails.history && selectedPatientDetails.history.length > 0 ? (
                      <List>
                        {selectedPatientDetails.history.map((entry, index) => (
                          <ListItem key={index}>
                            <ListItemText primary={entry.entry} secondary={new Date(entry.date).toLocaleDateString()} />
                          </ListItem>
                        ))}
                      </List>
                    ) : (
                      <Typography variant="body2" color="text.secondary">No medical history recorded</Typography>
                    )}
                  </Grid2>
                  
                  <Grid2 item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="h6">Prescriptions</Typography>
                    {selectedPatientDetails.prescriptions && selectedPatientDetails.prescriptions.length > 0 ? (
                      <TableContainer>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell>Medication</TableCell>
                              <TableCell>Quantity</TableCell>
                              <TableCell>Doctor</TableCell>
                              <TableCell>Date</TableCell>
                              <TableCell>Fee</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {selectedPatientDetails.prescriptions.map((prescription, index) => (
                              <TableRow key={index}>
                                <TableCell>{prescription.medication_name}</TableCell>
                                <TableCell>{prescription.quantity}</TableCell>
                                <TableCell>{prescription.doctor_name}</TableCell>
                                <TableCell>{new Date(prescription.date).toLocaleDateString()}</TableCell>
                                <TableCell>${prescription.fee}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    ) : (
                      <Typography variant="body2" color="text.secondary">No prescriptions recorded</Typography>
                    )}
                  </Grid2>
                  
                  <Grid2 item xs={12}>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="h6">Lab Results</Typography>
                    {selectedPatientDetails.lab_results && selectedPatientDetails.lab_results.length > 0 ? (
                      <TableContainer>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell>Test Name</TableCell>
                              <TableCell>Result</TableCell>
                              <TableCell>Date</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {selectedPatientDetails.lab_results.map((result, index) => (
                              <TableRow key={index}>
                                <TableCell>{result.test_name}</TableCell>
                                <TableCell>{result.result}</TableCell>
                                <TableCell>{new Date(result.date).toLocaleDateString()}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    ) : (
                      <Typography variant="body2" color="text.secondary">No lab results recorded</Typography>
                    )}
                  </Grid2>
                </Grid2>
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setShowPatientInfoModal(false)} color="primary">
                  Close
                </Button>
                <Button 
                  onClick={() => {
                    setShowPatientInfoModal(false);
                    setIsEditing(true);
                    setCurrentPatient({
                      id: selectedPatientDetails.id,
                      name: selectedPatientDetails.name,
                      age: selectedPatientDetails.age.toString(),
                      gender: selectedPatientDetails.gender,
                      contact: selectedPatientDetails.contact
                    });
                    setShowModal(true);
                  }} 
                  color="primary" 
                  variant="contained"
                >
                  Manage Patient
                </Button>
              </DialogActions>
            </>
          )}
        </Dialog>

        {/* Prescription Order Modal */}
        <Dialog
          open={showPrescriptionModal}
          onClose={() => setShowPrescriptionModal(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Order Prescription</DialogTitle>
          <DialogContent>
            <Grid2 container spacing={2}>
              <Grid2 item xs={12}>
                <FormControl fullWidth sx={{ mt: 1 }}>
                  <InputLabel id="prescription-med-label">Medication</InputLabel>
                  <Select
                    labelId="prescription-med-label"
                    id="prescription-medication"
                    value={selectedMedication}
                    label="Medication"
                    onChange={handleMedicationChange}
                    required
                  >
                    <MenuItem value="">Select medication</MenuItem>
                    {medications.map(med => (
                      <MenuItem key={med.id} value={med.id}>
                        {med.name} - ${med.price}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid2>
              
              <Grid2 item xs={6}>
                <TextField
                  margin="dense"
                  id="quantity"
                  label="Quantity"
                  type="number"
                  fullWidth
                  variant="outlined"
                  value={prescriptionQuantity}
                  onChange={handleQuantityChange}
                  required
                  inputProps={{ min: 1 }}
                />
              </Grid2>
              
              <Grid2 item xs={6}>
                <FormControl fullWidth sx={{ mt: 1 }}>
                  <InputLabel id="doctor-label">Doctor</InputLabel>
                  <Select
                    labelId="doctor-label"
                    id="doctor"
                    value={selectedDoctor}
                    label="Doctor"
                    onChange={(e) => setSelectedDoctor(e.target.value)}
                    required
                  >
                    <MenuItem value="">Select doctor</MenuItem>
                    {doctors.map(doctor => (
                      <MenuItem key={doctor.id} value={doctor.id}>
                        {doctor.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid2>
              
              <Grid2 item xs={12}>
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Total Fee: ${calculatedFee.toFixed(2)}
                </Typography>
              </Grid2>
            </Grid2>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowPrescriptionModal(false)} color="primary">
              Cancel
            </Button>
            <Button 
              onClick={handleCreatePrescription} 
              color="primary" 
              variant="contained"
              disabled={!selectedMedication || !selectedDoctor}
            >
              Create Prescription
            </Button>
          </DialogActions>
        </Dialog>
      </div>
  );
}

// ...existing code...

// Edit/Add Patient Modal
const PatientFormModal = ({ open, onClose, onSubmit, currentPatient, isEditing, handleInputChange }) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{isEditing ? "Edit Patient" : "Add New Patient"}</DialogTitle>
      <form onSubmit={onSubmit}>
        <DialogContent dividers>
          <Grid2 container spacing={2}>
            <Grid2 item xs={12}>
              <TextField
                name="name"
                label="Full Name"
                value={currentPatient.name}
                onChange={handleInputChange}
                fullWidth
                required
                margin="normal"
              />
            </Grid2>
            <Grid2 item xs={12} sm={6}>
              <TextField
                name="age"
                label="Age"
                type="number"
                value={currentPatient.age}
                onChange={handleInputChange}
                fullWidth
                required
                margin="normal"
                inputProps={{ min: 0 }}
              />
            </Grid2>
            <Grid2 item xs={12} sm={6}>
              <FormControl fullWidth margin="normal" required>
                <InputLabel id="gender-label">Gender</InputLabel>
                <Select
                  labelId="gender-label"
                  name="gender"
                  value={currentPatient.gender}
                  onChange={handleInputChange}
                  label="Gender"
                >
                  <MenuItem value="Male">Male</MenuItem>
                  <MenuItem value="Female">Female</MenuItem>
                  <MenuItem value="Other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid2>
            <Grid2 item xs={12}>
              <TextField
                name="contact"
                label="Contact Information"
                value={currentPatient.contact}
                onChange={handleInputChange}
                fullWidth
                required
                margin="normal"
                placeholder="Phone number or email"
              />
            </Grid2>
          </Grid2>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" color="primary">
            {isEditing ? "Save Changes" : "Add Patient"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

// ...existing code...

// Prescription Order Modal
const PrescriptionModal = ({ 
  open, 
  onClose, 
  currentPatient,
  medications,
  doctors,
  selectedMedication,
  selectedDoctor,
  prescriptionQuantity,
  calculatedFee,
  handleMedicationChange,
  handleQuantityChange,
  handleDoctorChange,
  onCreatePrescription
}) => {
  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Order Prescription</DialogTitle>
      <DialogContent dividers>
        <Grid2 container spacing={2}>
          <Grid2 item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Patient: {currentPatient.name}
            </Typography>
          </Grid2>
          
          <Grid2 item xs={12}>
            <FormControl fullWidth margin="normal" required>
              <InputLabel id="medication-label">Medication</InputLabel>
              <Select
                labelId="medication-label"
                value={selectedMedication}
                onChange={handleMedicationChange}
                label="Medication"
              >
                {medications.map((medication) => (
                  <MenuItem key={medication.id} value={medication.id}>
                    {medication.name} - ${medication.unit_price.toFixed(2)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid2>
          
          <Grid2 item xs={12}>
            <FormControl fullWidth margin="normal" required>
              <InputLabel id="doctor-label">Doctor</InputLabel>
              <Select
                labelId="doctor-label"
                value={selectedDoctor}
                onChange={(e) => handleDoctorChange(e.target.value)}
                label="Doctor"
              >
                {doctors.map((doctor) => (
                  <MenuItem key={doctor.id} value={doctor.id}>
                    {doctor.username}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid2>
          
          <Grid2 item xs={12}>
            <TextField
              label="Quantity"
              type="number"
              value={prescriptionQuantity}
              onChange={handleQuantityChange}
              fullWidth
              required
              margin="normal"
              inputProps={{ min: 1 }}
            />
          </Grid2>
          
          <Grid2 item xs={12}>
            <Paper variant="outlined" sx={{ p: 2, mt: 2, bgcolor: 'background.paper' }}>
              <Typography variant="h6" gutterBottom align="center">
                Total Fee: ${calculatedFee.toFixed(2)}
              </Typography>
            </Paper>
          </Grid2>
        </Grid2>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button 
          onClick={onCreatePrescription} 
          variant="contained" 
          color="primary"
          disabled={!selectedMedication || !selectedDoctor}
        >
          Create Prescription
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const PatientInfoModal = ({ open, onClose, patientDetails }) => {
  if (!patientDetails) return null;
  
  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        Patient Information: {patientDetails.name}
      </DialogTitle>
      <DialogContent dividers>
        <Grid2 container spacing={2}>
          {/* Basic patient info */}
          <Grid2 item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
              <Typography variant="h6" gutterBottom>Patient Details</Typography>
              <Typography><strong>ID:</strong> {patientDetails.id}</Typography>
              <Typography><strong>Name:</strong> {patientDetails.name}</Typography>
              <Typography><strong>Age:</strong> {patientDetails.age}</Typography>
              <Typography><strong>Gender:</strong> {patientDetails.gender}</Typography>
              <Typography><strong>Contact:</strong> {patientDetails.contact}</Typography>
            </Paper>
          </Grid2>
          
          {/* Medical history */}
          <Grid2 item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
              <Typography variant="h6" gutterBottom>Medical History</Typography>
              {patientDetails.history && patientDetails.history.length > 0 ? (
                <List dense>
                  {patientDetails.history.map((entry, index) => (
                    <ListItem key={index} divider={index < patientDetails.history.length - 1}>
                      <ListItemText primary={entry} />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography color="text.secondary">No medical history available</Typography>
              )}
            </Paper>
          </Grid2>
          
          {/* Prescribed medications */}
          <Grid2 item xs={12}>
            <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
              <Typography variant="h6" gutterBottom>Prescribed Medications</Typography>
              {patientDetails.prescriptions && patientDetails.prescriptions.length > 0 ? (
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Medication</TableCell>
                        <TableCell>Dosage</TableCell>
                        <TableCell>Doctor</TableCell>
                        <TableCell align="right">Cost</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {patientDetails.prescriptions.map((prescription) => (
                        <TableRow key={prescription.id}>
                          <TableCell>{prescription.medication}</TableCell>
                          <TableCell>{prescription.dosage}</TableCell>
                          <TableCell>{prescription.doctor_name}</TableCell>
                          <TableCell align="right">${prescription.amount.toFixed(2)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography color="text.secondary">No prescriptions available</Typography>
              )}
            </Paper>
          </Grid2>
          
          {/* Lab results */}
          <Grid2 item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
              <Typography variant="h6" gutterBottom>Lab Results</Typography>
              {patientDetails.lab_results && patientDetails.lab_results.length > 0 ? (
                <List dense>
                  {patientDetails.lab_results.map((result) => (
                    <ListItem key={result.id} divider>
                      <ListItemText 
                        primary={result.test_name}
                        secondary={
                          <>
                            <Typography component="span" variant="body2">
                              Date: {result.test_date}
                            </Typography>
                            <br />
                            <Typography component="span" variant="body2">
                              Result: {result.result}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography color="text.secondary">No lab results available</Typography>
              )}
            </Paper>
          </Grid2>
          
          {/* Fees and Treatments */}
          <Grid2 item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
              <Typography variant="h6" gutterBottom>Treatments</Typography>
              {patientDetails.treatments && patientDetails.treatments.length > 0 ? (
                <List dense>
                  {patientDetails.treatments.map((treatment) => (
                    <ListItem key={treatment.id} divider>
                      <ListItemText 
                        primary={treatment.diagnosis}
                        secondary={
                          <>
                            <Typography component="span" variant="body2">
                              Date: {treatment.treatment_date}
                            </Typography>
                            <br />
                            <Typography component="span" variant="body2">
                              Notes: {treatment.notes}
                            </Typography>
                          </>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography color="text.secondary">No treatments available</Typography>
              )}
            </Paper>
            
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>Fees</Typography>
              {patientDetails.fees && patientDetails.fees.length > 0 ? (
                <>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Description</TableCell>
                          <TableCell align="right">Amount</TableCell>
                          <TableCell align="right">Paid</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {patientDetails.fees.map((fee) => (
                          <TableRow key={fee.id}>
                            <TableCell>{fee.description}</TableCell>
                            <TableCell align="right">${fee.amount.toFixed(2)}</TableCell>
                            <TableCell align="right">{fee.is_paid ? "Yes" : "No"}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                  <Typography variant="subtitle1" sx={{ mt: 2, fontWeight: 'bold' }}>
                    Total: ${patientDetails.total_fees?.toFixed(2) || '0.00'}
                  </Typography>
                </>
              ) : (
                <Typography color="text.secondary">No fees available</Typography>
              )}
            </Paper>
          </Grid2>
        </Grid2>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PatientList;