import React, { useState } from "react";
import { 
  Grid2, Typography, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, Button, AppBar, Box, Toolbar, 
  InputBase, TextField, Dialog, DialogTitle, DialogContent, DialogActions, 
  FormControl, InputLabel, Select, MenuItem, styled, alpha, IconButton 
} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import SearchIcon from "@mui/icons-material/Search";
import useUserData from "../hooks/useUserData";
import useAppointmentData from "../hooks/useAppointmentData";
import UserProfile from "./UserProfile";
import "../styles/Inventory.css";
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider, DatePicker, TimePicker, } from '@mui/x-date-pickers';
import dayjs from 'dayjs';

// Styled components for search
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

const StatusChip = styled('span')(({ color }) => ({
  backgroundColor: color,
  color: 'white',
  padding: '4px 8px',
  borderRadius: '16px',
  fontSize: '0.75rem',
  fontWeight: 'bold',
  display: 'inline-block',
}));

function Appointments() {
  const { 
    usernames, roles, access, profile_image_directory, 
    error: userError, isLoading: userLoading 
  } = useUserData();
  
  const {
    filteredAppointments,
    searchTerm,
    setSearchTerm,
    error: appointmentError,
    isLoading: appointmentLoading,
    doctors,
    patients,
    getStatusColor,
    addAppointment,
    updateAppointment,
    updateAppointmentStatus,
    removeAppointment
  } = useAppointmentData();

  // Local UI state
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentAppointment, setCurrentAppointment] = useState({
    id: null,
    patient_id: "",
    doctor_id: "",
    date: null,
    time: null,
    status: "scheduled"
  });

  // Handle form submission for adding or editing appointments
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const formattedAppointment = {
        ...currentAppointment,
        date: currentAppointment.date ? dayjs(currentAppointment.date).format('YYYY-MM-DD') : '',
        time: currentAppointment.time ? dayjs(currentAppointment.time).format('HH:mm') : ''
      };

      if (isEditing) {
        await updateAppointment(formattedAppointment);
      } else {
        await addAppointment(formattedAppointment);
      }
      
      setShowModal(false);
      
    } catch (error) {
      console.error("Error saving appointment:", error);
      alert(error.message || "Failed to save appointment");
    }
  };

  // Handle input changes in the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentAppointment({
      ...currentAppointment,
      [name]: value
    });
  };

  // Handle date change
  const handleDateChange = (newDate) => {
    setCurrentAppointment({
      ...currentAppointment,
      date: newDate
    });
  };

  // Handle time change
  const handleTimeChange = (newTime) => {
    setCurrentAppointment({
      ...currentAppointment,
      time: newTime
    });
  };

  // Handle status change
  const handleStatusChange = async (id, newStatus) => {
    try {
      await updateAppointmentStatus(id, newStatus);
    } catch (error) {
      console.error("Error updating status:", error);
      alert(error.message || "Failed to update status");
    }
  };

  // Handle delete confirmation
  const handleRemoveAppointment = async (id) => {
    try {
      await removeAppointment(id);
    } catch (error) {
      console.error("Error removing appointment:", error);
      alert(error.message || "Failed to delete appointment");
    }
  };

  const error = userError || appointmentError;
  const isLoading = userLoading || appointmentLoading;

  if (error) return (
    <div className="ContainerPage">
      <div className="error-container">
        <p className="error-message">{error}</p>
        <Button 
          variant="contained" 
          onClick={() => window.location.href = "/login"}
        >
          Go to Login
        </Button>
      </div>
    </div>
  );

  if (isLoading) return (
    <div className="ContainerPage">
      <div className="loading-container">
        <Typography variant="body1">Loading Appointment Data...</Typography>
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
                    Appointments
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
                      setCurrentAppointment({
                        id: null,
                        patient_id: "",
                        doctor_id: "",
                        date: null,
                        time: null,
                        status: "scheduled"
                      });
                      setShowModal(true);
                    }}
                    sx={{ 
                      ml: 2, 
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    New Appointment
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
                  mt: 2,
                  backgroundColor: 'transparent',
                  boxShadow: 'none'
                }}
              >
                <Table stickyHeader aria-label="appointments table">
                  <TableHead>
                    <TableRow>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '60px' }}>ID</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Patient</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold' }}>Date</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Time</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold' }}>Doctor</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold' }}>Status</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '180px' }}>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredAppointments.length > 0 ? (
                      filteredAppointments.map((appointment) => (
                        <TableRow 
                          key={appointment.id}
                          sx={{ 
                            '&:hover': { backgroundColor: 'rgba(236, 230, 240, 0.4)' }, 
                            borderRadius: '15px',
                            mb: 1,
                            border: '2px solid var(--border-color)'
                          }}
                        >
                          <TableCell align="center">{appointment.id}</TableCell>
                          <TableCell>{appointment.patient_name}</TableCell>
                          <TableCell align="center">{appointment.dateFormatted}</TableCell>
                          <TableCell>{appointment.timeFormatted}</TableCell>
                          <TableCell align="center">{appointment.doctor_name}</TableCell>
                          <TableCell align="center">
                            <StatusChip color={appointment.statusColor}>
                              {appointment.status}
                            </StatusChip>
                          </TableCell>
                          <TableCell align="center">
                          <Button
  variant="contained"
  size="small"
  sx={{ mr: 1, color: 'white' }}
  onClick={() => {
    setIsEditing(true);
    
    setCurrentAppointment({
      id: appointment.id,
      patient_id: appointment.patient_id,
      doctor_id: appointment.doctor_id,
      date: appointment.date ? dayjs(appointment.date) : null,  // Ensure it's valid
      time: appointment.time ? dayjs(`2000-01-01T${appointment.time}`) : null,  // Ensure proper formatting
      status: appointment.status
    });

    setShowModal(true);
  }}
>
  Edit
</Button>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={7} align="center">No appointments found</TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </div>
          </Grid2>
        </Grid2>
        
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <Dialog 
            open={showModal} 
            onClose={() => setShowModal(false)} 
            maxWidth="sm" 
            fullWidth
          >
            <DialogTitle>
              {isEditing ? 'Edit Appointment' : 'New Appointment'}
            </DialogTitle>
            <IconButton
              aria-label="close"
              onClick={() => setShowModal(false)}
              sx={{
                position: 'absolute',
                right: 8,
                top: 8,
                color: (theme) => theme.palette.grey[500],
              }}
            >
              <CloseIcon />
            </IconButton>
            <form onSubmit={handleSubmit}>
              <DialogContent>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel id="patient-label">Patient</InputLabel>
                  <Select
                    labelId="patient-label"
                    id="patient_id"
                    name="patient_id"
                    value={currentAppointment.patient_id}
                    label="Patient"
                    onChange={handleInputChange}
                    required
                  >
                    {patients.map(patient => (
                      <MenuItem key={patient.id} value={patient.id}>
                        {patient.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel id="doctor-label">Doctor</InputLabel>
                  <Select
                    labelId="doctor-label"
                    id="doctor_id"
                    name="doctor_id"
                    value={currentAppointment.doctor_id}
                    label="Doctor"
                    onChange={handleInputChange}
                    required
                  >
                    {doctors.map(doctor => (
                      <MenuItem key={doctor.id} value={doctor.id}>
                        {/* Make sure to use consistent property between table display and dropdown */}
                        {doctor.name || doctor.username || doctor.doctor_name || `Doctor ID: ${doctor.id}`}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                
                <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between' }}>
                  <DatePicker
                    label="Date"
                    value={currentAppointment.date}
                    onChange={handleDateChange}
                    renderInput={(params) => <TextField {...params} fullWidth required />}
                  />
                                    <TimePicker
                    label="Time"
                    value={currentAppointment.time}
                    onChange={handleTimeChange}
                    renderInput={(params) => <TextField {...params} fullWidth required />}
                  />
                </Box>
                
                
                {isEditing && (
                  <FormControl fullWidth>
                    <InputLabel id="status-label">Status</InputLabel>
                    <Select
                      labelId="status-label"
                      id="status"
                      name="status"
                      value={currentAppointment.status}
                      label="Status"
                      onChange={handleInputChange}
                    >
                      <MenuItem value="scheduled">Scheduled</MenuItem>
                      <MenuItem value="completed">Completed</MenuItem>
                      <MenuItem value="cancelled">Cancelled</MenuItem>
                      <MenuItem value="no-show">No Show</MenuItem>
                    </Select>
                  </FormControl>
                )}
              </DialogContent>
              <DialogActions sx={{ justifyContent: 'space-between', px: 3, pb: 2 }}>
                {isEditing && (
                  <Button 
                    onClick={() => {
                      if(window.confirm("Are you sure you want to delete this appointment?")) {
                        handleRemoveAppointment(currentAppointment.id);
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
                  <Button type="submit" color="primary" variant="contained">
                    {isEditing ? 'Update' : 'Add Appointment'}
                  </Button>
                </Box>
              </DialogActions>
            </form>
          </Dialog>
        </LocalizationProvider>
      </div>
  );
}

export default Appointments;