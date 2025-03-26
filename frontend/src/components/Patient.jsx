import React, { useState, useEffect } from "react";
import { 
  Grid2, Typography, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, Divider, Button, AppBar, Box, Toolbar, 
  InputBase, TextField, Dialog, DialogTitle, DialogContent, DialogActions, 
  FormControl, InputLabel, Select, MenuItem, List, ListItem, ListItemText, 
  styled, alpha, IconButton, FormControlLabel, Checkbox 
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import CloseIcon from "@mui/icons-material/Close";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
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
    updatePatient, deletePatient,
    createPatient,
    fetchPatientHistory, addHistoryEntry,
    updateHistoryEntry, deleteHistoryEntry,
    fetchPatientDetails, addTreatment,
    historyEntries, setHistoryEntries,deleteTreatment,
    updateTreatment,
    selectedPatientDetails, setSelectedPatientDetails
  } = usePatientData();

  // Local UI state
  const [showModal, setShowModal] = useState(false);
  const [showPatientInfoModal, setShowPatientInfoModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState(null);
  const [currentPatient, setCurrentPatient] = useState({
    id: '',
    name: '',
    age: '',
    gender: '',
    contact: ''
  });
  const [showTreatmentModal, setShowTreatmentModal] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [diagnosis, setDiagnosis] = useState('');
  const [treatmentNotes, setTreatmentNotes] = useState('');
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [newHistoryEntry, setNewHistoryEntry] = useState("");
  const [editingHistoryId, setEditingHistoryId] = useState(null);
  const [editHistoryText, setEditHistoryText] = useState("");
  const [symptoms, setSymptoms] = useState('');
  const [treatment, setTreatment] = useState('');
  const [treatmentFinished, setTreatmentFinished] = useState(false);
  const [editingTreatment, setEditingTreatment] = useState(null);
  const [patientTreatments, setPatientTreatments] = useState([]); 
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEditing) {
      updatePatient({ 
        id: currentPatient.id,
        name: currentPatient.name,
        age: parseInt(currentPatient.age),
        gender: currentPatient.gender,
        contact: currentPatient.contact
      })
      .then(() => {
        setShowModal(false);
        alert("Patient updated successfully!");
      })
      .catch(error => {
        console.error("Error updating patient:", error);
        alert("Failed to update patient: " + error.message);
      });
    } else {
      // Add new patient using hook
      createPatient({ 
        name: currentPatient.name,
        age: parseInt(currentPatient.age),
        gender: currentPatient.gender,
        contact: currentPatient.contact
      })
      .then(() => {
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
      deletePatient(patientId)
        .then(() => {
          alert("Patient deleted successfully!");
        })
        .catch(error => {
          console.error("Error deleting patient:", error);
          alert("Failed to delete patient: " + error.message);
        });
    }
  };

  // Handle adding history entry
  const handleAddHistoryEntry = () => {
    if (!newHistoryEntry.trim()) {
      alert("Please enter a history entry");
      return;
    }
    
    addHistoryEntry(currentPatient.id, newHistoryEntry)
      .then(() => {
        setNewHistoryEntry("");
        alert("History entry added successfully!");
      })
      .catch(error => {
        console.error("Error adding history entry:", error);
        alert("Failed to add history entry: " + error.message);
      });
  };

  // Function to fetch patient history
  const loadPatientHistory = (patientId) => {
    fetchPatientHistory(patientId)
      .catch(error => {
        console.error("Error loading patient history:", error);
        alert("Failed to load patient history: " + error.message);
      });
  };

  // Update history entry
  const handleUpdateHistoryEntry = (index) => {
    if (!editHistoryText.trim()) {
      alert("Please enter a valid history entry");
      return;
    }
    
    updateHistoryEntry(currentPatient.id, index, editHistoryText)
      .then(() => {
        setEditingHistoryId(null);
        setEditHistoryText("");
        alert("History entry updated successfully!");
      })
      .catch(error => {
        console.error("Error updating history entry:", error);
        alert("Failed to update history entry: " + error.message);
      });
  };

  // Handle delete history entry
  const handleDeleteHistoryEntry = (index) => {
    if (window.confirm("Are you sure you want to delete this history entry?")) {
      deleteHistoryEntry(currentPatient.id, index)
        .then(() => {
          // The hook should already update historyEntries state by filtering out the deleted entry
          alert("History entry deleted successfully!");
        })
        .catch(error => {
          console.error("Error deleting history entry:", error);
          alert("Failed to delete history entry: " + error.message);
        });
    }
  };

  const handleViewPatientDetails = (patient) => {
    fetchPatientDetails(patient.id)
      .then(() => {
        setShowPatientInfoModal(true);
      })
      .catch(error => {
        console.error("Error loading patient details:", error);
        alert("Failed to load patient details: " + error.message);
      });
  };

  // Refresh patient details
  const refreshPatientDetails = (patientId) => {
    if (patientId) {
      fetchPatientDetails(patientId)
        .then(() => {
          // Increment refresh trigger to cause re-render
          setRefreshTrigger(prev => prev + 1);
        })
        .catch(error => {
          console.error("Error loading patient details:", error);
        });
    }
  };

  // Add treatment
  const handleAddTreatment = (patientId, diagnosis, notes) => {
    addTreatment(patientId, diagnosis, notes)
      .then(() => {
        alert("Treatment added successfully!");
        // Refresh patient details to include the new treatment
        refreshPatientDetails(patientId);
      })
      .catch(error => {
        console.error("Error adding treatment:", error);
        alert("Failed to add treatment: " + error.message);
      });
  };

  // Add these handler functions

// Open treatment modal for new treatment
const handleOpenAddTreatment = () => {
  setSymptoms('');
  setDiagnosis('');
  setTreatment('');
  setTreatmentFinished(false);
  setEditingTreatment(null);
  setShowTreatmentModal(true);
};

// Open treatment modal for editing
const handleOpenEditTreatment = (treatment) => {
  setSymptoms(treatment.symptoms);
  setDiagnosis(treatment.diagnosis);
  setTreatment(treatment.treatment);
  setTreatmentFinished(treatment.finished);
  setEditingTreatment(treatment);
  setShowTreatmentModal(true);
};

// Save or update treatment
const handleSaveTreatment = () => {
  if (!symptoms || !diagnosis || !treatment) {
    alert('Please fill all required fields');
    return;
  }

  const treatmentData = {
    symptoms,
    diagnosis,
    treatment,
    finished: treatmentFinished
  };

  if (editingTreatment) {
    // Update existing treatment
    updateTreatment(currentPatient.id, editingTreatment.id, treatmentData)
      .then(() => {
        // Refresh both data sources
        refreshPatientDetails(currentPatient.id);
        loadPatientTreatments(currentPatient.id);
        // Close modal and reset form
        setShowTreatmentModal(false);
        setSymptoms('');
        setDiagnosis('');
        setTreatment('');
        setTreatmentFinished(false);
        setEditingTreatment(null);
      })
      .catch(error => console.error('Error updating treatment:', error));
  } else {
    // Add new treatment
    addTreatment(currentPatient.id, treatmentData)
      .then(() => {
        // Refresh both data sources
        refreshPatientDetails(currentPatient.id);
        loadPatientTreatments(currentPatient.id);
        // Close modal and reset form
        setShowTreatmentModal(false);
        setSymptoms('');
        setDiagnosis('');
        setTreatment('');
        setTreatmentFinished(false);
      })
      .catch(error => console.error('Error adding treatment:', error));
  }
};

// Delete treatment
const handleDeleteTreatment = (treatmentId) => {
  if (window.confirm('Are you sure you want to delete this treatment?')) {
    deleteTreatment(currentPatient.id, treatmentId)
      .then(() => {
        // Refresh both data sources
        refreshPatientDetails(currentPatient.id);
        loadPatientTreatments(currentPatient.id);
      })
      .catch(error => console.error('Error deleting treatment:', error));
  }
};

// Add this function to load patient treatments
const loadPatientTreatments = (patientId) => {
  fetch(`http://127.0.0.1:5000/api/patients/${patientId}/treatments`, {
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch treatments");
      return response.json();
    })
    .then(data => {
      setPatientTreatments(data);
    })
    .catch(error => {
      console.error("Error loading patient treatments:", error);
      setPatientTreatments([]); // Clear treatments on error
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
          <Grid2 size="auto">
          <UserProfile 
            usernames={usernames}
            roles={roles}
            access={access}
            profile_image_directory={profile_image_directory}
          />
          </Grid2>
          {/* Right column - Patient table */}
            <Grid2 xs={8} size="grow" sx={{ display: 'flex', flexDirection: 'column', padding: 2 }}>
            <Box sx={{ flexGrow: 0 }}>
              <AppBar position="static">
                <Toolbar>
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
                          <TableCell 
                            onClick={() => handleViewPatientDetails(patient)}
                            sx={{ cursor: 'pointer', color: 'var(--accent-color)', fontWeight: 'bold' }}
                          >
                            {patient.name}
                          </TableCell>
                          <TableCell align="center">{patient.age}</TableCell>
                          <TableCell>{patient.gender}</TableCell>
                          <TableCell>{patient.contact}</TableCell>
                          <TableCell align="center">
  <Box
    sx={{
      display: "flex",
      flexDirection: "row",
      gap: 0.5,
      justifyContent: "center",
    }}
  >
    <Button
      variant="contained"
      size="small"
      sx={{
        color: "white",
        mr: 1,
      }}
      onClick={() => {
        setIsEditing(true);
        setCurrentPatient({
          id: patient.id,
          name: patient.name,
          age: patient.age,
          gender: patient.gender,
          contact: patient.contact,
        });
        setShowModal(true);
      }}
    >
      Edit Info
    </Button>
    <Button
      variant="contained"
      size="small"
      sx={{
        color: "white",
        mr: 1,
      }}
      onClick={() => {
        setCurrentPatient({
          id: patient.id,
          name: patient.name,
          age: patient.age,
          gender: patient.gender,
          contact: patient.contact,
        });
        // Reset treatments before loading new ones
        setPatientTreatments([]);
        setSelectedPatientDetails(null);
        loadPatientHistory(patient.id);
        loadPatientTreatments(patient.id);
        setShowHistoryModal(true);
      }}
    >
      Edit History
    </Button>
    <Button
      variant="contained"
      size="small"
      color="error"
      onClick={() => handleDeletePatient(patient.id)}
    >
      Delete
    </Button>
  </Box>
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
          
          {/* Add/Edit Patient Modal */}
          <Dialog 
            open={showModal} 
            onClose={() => setShowModal(false)}
            fullWidth
            maxWidth="sm"
          >
            <DialogTitle>
              {isEditing ? "Edit Patient Information" : "Register New Patient"}
              <IconButton
                aria-label="close"
                onClick={() => setShowModal(false)}
                sx={{ position: 'absolute', right: 8, top: 8 }}
              >
                <CloseIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent dividers>
              <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }} noValidate>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="name"
                  label="Patient Name"
                  name="name"
                  autoFocus
                  value={currentPatient.name || ''}
                  onChange={handleInputChange}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="age"
                  label="Age"
                  name="age"
                  type="number"
                  value={currentPatient.age || ''}
                  onChange={handleInputChange}
                />
                <FormControl fullWidth margin="normal">
                  <InputLabel id="gender-label">Gender</InputLabel>
                  <Select
                    labelId="gender-label"
                    id="gender"
                    name="gender"
                    value={currentPatient.gender || ''}
                    label="Gender"
                    onChange={handleInputChange}
                  >
                    <MenuItem value="Male">Male</MenuItem>
                    <MenuItem value="Female">Female</MenuItem>
                    <MenuItem value="Other">Other</MenuItem>
                  </Select>
                </FormControl>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="contact"
                  label="Contact Number"
                  name="contact"
                  value={currentPatient.contact || ''}
                  onChange={handleInputChange}
                />
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleSubmit} color="primary" variant="contained">
                {isEditing ? "Update Patient" : "Add Patient"}
              </Button>
            </DialogActions>
          </Dialog>
          
          {/* Patient Information Modal */}
          <Dialog 
            open={showPatientInfoModal} 
            onClose={() => setShowPatientInfoModal(false)}
            fullWidth
            maxWidth="md"
          >
            <DialogTitle>
              Patient Information
              <IconButton
                aria-label="close"
                onClick={() => setShowPatientInfoModal(false)}
                sx={{ position: 'absolute', right: 8, top: 8 }}
              >
                <CloseIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent dividers>
              {selectedPatientDetails && (
                <>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Basic Information</Typography>
                    <Grid2 container spacing={2}>
                      <Grid2 xs={6}>
                        <Typography><strong>Name:</strong> {selectedPatientDetails.name}</Typography>
                        <Typography><strong>Age:</strong> {selectedPatientDetails.age}</Typography>
                        <Typography><strong>Gender:</strong> {selectedPatientDetails.gender}</Typography>
                      </Grid2>
                      <Grid2 xs={6}>
                        <Typography><strong>Contact:</strong> {selectedPatientDetails.contact}</Typography>
                        <Typography><strong>Patient ID:</strong> {selectedPatientDetails.id}</Typography>
                        <Typography><strong>Total Fees:</strong> ${selectedPatientDetails.fees_total?.toFixed(2) || "0.00"}</Typography>
                      </Grid2>
                    </Grid2>
                  </Box>
                  
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Medical History</Typography>
                    <List dense>
                      {selectedPatientDetails.history?.length > 0 ? (
                        selectedPatientDetails.history.map((entry, idx) => (
                          <ListItem key={idx}>
                            <ListItemText primary={entry} />
                          </ListItem>
                        ))
                      ) : (
                        <ListItem>
                          <ListItemText primary="No medical history available" />
                        </ListItem>
                      )}
                    </List>
                  </Box>
                  
            
                  
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>Treatment Notes</Typography>
                    <TableContainer component={Paper} sx={{ maxHeight: 200 }}>
                      <Table size="small" stickyHeader>
                        <TableHead>
                          <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Symptoms</TableCell>
                            <TableCell>Diagnosis</TableCell>
                            <TableCell>Treatment</TableCell>
                            <TableCell>Status</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {selectedPatientDetails.treatments?.length > 0 ? (
                            selectedPatientDetails.treatments.map((treatment, idx) => (
                              <TableRow key={idx}>
                                <TableCell>{treatment.date}</TableCell>
                                <TableCell>{treatment.symptoms}</TableCell>
                                <TableCell>{treatment.diagnosis}</TableCell>
                                <TableCell>{treatment.treatment}</TableCell>
                                <TableCell>{treatment.finished ? "Completed" : "Ongoing"}</TableCell>
                              </TableRow>
                            ))
                          ) : (
                            <TableRow>
                              <TableCell colSpan={5} align="center">No treatment notes available</TableCell>
                            </TableRow>
                          )}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </Box>
                </>
              )}
            </DialogContent>
          </Dialog>
          {/* Treatment Modal */}
          <Dialog 
            open={showTreatmentModal} 
            onClose={() => setShowTreatmentModal(false)}
            fullWidth
            maxWidth="sm"
          >
            <DialogTitle>
              {editingTreatment ? "Edit Treatment" : "Add Treatment"} for {currentPatient.name}
              <IconButton
                aria-label="close"
                onClick={() => setShowTreatmentModal(false)}
                sx={{ position: 'absolute', right: 8, top: 8 }}
              >
                <CloseIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent dividers>
              <Box component="form" sx={{ mt: 2 }} noValidate>
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="symptoms"
                  label="Symptoms"
                  name="symptoms"
                  autoFocus
                  value={symptoms || ''}
                  onChange={(e) => setSymptoms(e.target.value)}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  id="diagnosis"
                  label="Diagnosis"
                  name="diagnosis"
                  value={diagnosis || ''}
                  onChange={(e) => setDiagnosis(e.target.value)}
                />
                <TextField
                  margin="normal"
                  required
                  fullWidth
                  multiline
                  rows={4}
                  id="treatment"
                  label="Treatment"
                  name="treatment"
                  value={treatment || ''}
                  onChange={(e) => setTreatment(e.target.value)}
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={treatmentFinished}
                      onChange={(e) => setTreatmentFinished(e.target.checked)}
                      name="finished"
                    />
                  }
                  label="Treatment Completed"
                />
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => {
                setShowTreatmentModal(false);
                setSymptoms('');
                setDiagnosis('');
                setTreatment('');
                setTreatmentFinished(false);
                setEditingTreatment(null);
              }}>Cancel</Button>
              <Button 
                onClick={handleSaveTreatment}
                color="primary" 
                variant="contained"
                disabled={!symptoms || !diagnosis || !treatment}
              >
                {editingTreatment ? "Update Treatment" : "Add Treatment"}
              </Button>
            </DialogActions>
          </Dialog>
          {/* History Modal */}
          <Dialog 
            open={showHistoryModal} 
            onClose={() => setShowHistoryModal(false)}
            fullWidth
            maxWidth="md"
          >
            <DialogTitle>
              Medical History for {currentPatient.name}
              <IconButton
                aria-label="close"
                onClick={() => setShowHistoryModal(false)}
                sx={{ position: 'absolute', right: 8, top: 8 }}
              >
                <CloseIcon />
              </IconButton>
            </DialogTitle>
            <DialogContent dividers>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>Add New Entry</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={2}
                    label="New Medical History Entry"
                    value={newHistoryEntry}
                    onChange={(e) => setNewHistoryEntry(e.target.value)}
                  />
                  <Button 
                    variant="contained" 
                    color="primary"
                    onClick={handleAddHistoryEntry}
                  >
                    Add Entry
                  </Button>
                </Box>
              </Box>
              
              <Divider sx={{ my: 2 }} />
              
              <Typography variant="h6" gutterBottom>Patient History</Typography>
              
              {historyEntries.length > 0 ? (
                <List>
                  {historyEntries.map((entry, index) => (
                    <ListItem 
                      key={index} 
                      divider 
                      sx={{ 
                        display: 'flex', 
                        alignItems: 'flex-start', 
                        flexDirection: 'column',
                        py: 2
                      }}
                    >
                      {editingHistoryId === index ? (
                        <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', gap: 1 }}>
                          <TextField
                            fullWidth
                            multiline
                            rows={2}
                            value={editHistoryText}
                            onChange={(e) => setEditHistoryText(e.target.value)}
                          />
                          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
                            <Button 
                              variant="outlined" 
                              onClick={() => {
                                setEditingHistoryId(null);
                                setEditHistoryText("");
                              }}
                            >
                              Cancel
                            </Button>
                            <Button 
                              variant="contained" 
                              onClick={() => handleUpdateHistoryEntry(index)}
                            >
                              Save
                            </Button>
                          </Box>
                        </Box>
                      ) : (
                          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
  <ListItemText 
    primary={entry.history} 
    sx={{ flexGrow: 1 }}
  />
  <Box sx={{ display: 'flex', gap: 1, ml: 2, flexShrink: 0 }}>
    <Button 
      size="small" 
      startIcon={<EditIcon />}
      onClick={() => {
        setEditingHistoryId(index);
        setEditHistoryText(entry.history);
      }}
    >
      Edit
    </Button>
    <Button 
      size="small" 
      color="error"
      startIcon={<DeleteIcon />}
      onClick={() => handleDeleteHistoryEntry(index)}
    >
      Delete
    </Button>
  </Box>
</Box>
                  
                      )}
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body1">No history entries available</Typography>
              )}
              
              <Divider sx={{ my: 2 }} />
              
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>Treatment Notes</Typography>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleOpenAddTreatment}
                  sx={{ mb: 2 }}
                >
                  Add New Treatment
                </Button>
                
                <TableContainer component={Paper}>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Symptoms</TableCell>
                        <TableCell>Diagnosis</TableCell>
                        <TableCell>Treatment</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell align="center">Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {selectedPatientDetails?.treatments?.length > 0 ? (
                        selectedPatientDetails.treatments.map((treatment, idx) => (
                          <TableRow key={idx}>
                            <TableCell>{treatment.date}</TableCell>
                            <TableCell>{treatment.symptoms}</TableCell>
                            <TableCell>{treatment.diagnosis}</TableCell>
                            <TableCell>{treatment.treatment}</TableCell>
                            <TableCell>{treatment.finished ? "Completed" : "Ongoing"}</TableCell>
                            <TableCell align="center">
                              <Button 
                                size="small" 
                                variant="outlined"
                                onClick={() => handleOpenEditTreatment(treatment)}
                                sx={{ mr: 1 }}
                              >
                                Edit
                              </Button>
                              <Button 
                                size="small" 
                                variant="outlined" 
                                color="error"
                                onClick={() => handleDeleteTreatment(treatment.id)}
                              >
                                Delete
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan={6} align="center">No treatment notes available</TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setShowHistoryModal(false)}>Close</Button>
            </DialogActions>
          </Dialog>
  </div>
         );       
        };



export default PatientList;