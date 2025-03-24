import { useState, useEffect } from 'react';

const useAppointmentData = () => {
  const [appointmentList, setAppointmentList] = useState([]);
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);

  // Function to get appointment status color
  const getStatusColor = (status) => {
    switch(status) {
      case 'scheduled':
        return '#3498db'; // Blue
      case 'completed':
        return '#2ecc71'; // Green
      case 'cancelled':
        return '#e74c3c'; // Red
      case 'no-show':
        return '#f39c12'; // Orange
      default:
        return '#95a5a6'; // Gray
    }
  };

  // Fetch appointments data
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          setError("You must be logged in");
          setIsLoading(false);
          return;
        }

        // Fetch appointments
        const response = await fetch("http://localhost:5000/api/appointments", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        
        // Format the data
        const formattedData = data.map(appointment => ({
          ...appointment,
          dateFormatted: new Date(appointment.date).toLocaleDateString(),
          timeFormatted: appointment.time.substring(0, 5),
          statusColor: getStatusColor(appointment.status)
        }));
        
        setAppointmentList(formattedData);
        setFilteredAppointments(formattedData);

        // Fetch doctors list for the dropdown
        const doctorsResponse = await fetch("http://localhost:5000/api/users/doctors", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (doctorsResponse.ok) {
          const doctorsData = await doctorsResponse.json();
          setDoctors(doctorsData);
        }

        // Fetch patients list for the dropdown
        const patientsResponse = await fetch("http://localhost:5000/api/patients", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (patientsResponse.ok) {
          const patientsData = await patientsResponse.json();
          setPatients(patientsData);
        }

      } catch (error) {
        console.error("Error fetching appointment data:", error);
        setError(error.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // Search functionality
  useEffect(() => {
    if (searchTerm.trim() === "") {
      setFilteredAppointments(appointmentList);
      return;
    }

    const searchTermLower = searchTerm.toLowerCase();
    const filtered = appointmentList.filter(
      appointment =>
        appointment.patient_name.toLowerCase().includes(searchTermLower) ||
        appointment.doctor_name.toLowerCase().includes(searchTermLower) ||
        appointment.status.toLowerCase().includes(searchTermLower) ||
        appointment.dateFormatted.toLowerCase().includes(searchTermLower)
    );
    
    setFilteredAppointments(filtered);
  }, [searchTerm, appointmentList]);

  // CRUD operations
  const addAppointment = async (appointmentData) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("You must be logged in");

      const response = await fetch("http://localhost:5000/api/appointments/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          patient_id: parseInt(appointmentData.patient_id),
          doctor_id: parseInt(appointmentData.doctor_id),
          date: appointmentData.date,
          time: appointmentData.time
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to add appointment");
      }

      // Refetch to update the list
      const updatedResponse = await fetch("http://localhost:5000/api/appointments", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (updatedResponse.ok) {
        const data = await updatedResponse.json();
        const formattedData = data.map(appointment => ({
          ...appointment,
          dateFormatted: new Date(appointment.date).toLocaleDateString(),
          timeFormatted: appointment.time.substring(0, 5),
          statusColor: getStatusColor(appointment.status)
        }));
        setAppointmentList(formattedData);
        setFilteredAppointments(formattedData);
      }

      return true;
    } catch (error) {
      console.error("Error adding appointment:", error);
      throw error;
    }
  };

  const updateAppointment = async (appointmentData) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("You must be logged in");

      const response = await fetch("http://localhost:5000/api/appointments/update", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          id: parseInt(appointmentData.id),
          patient_id: parseInt(appointmentData.patient_id),
          doctor_id: parseInt(appointmentData.doctor_id),
          date: appointmentData.date,
          time: appointmentData.time,
          status: appointmentData.status
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update appointment");
      }

      // Refetch to update the list
      const updatedResponse = await fetch("http://localhost:5000/api/appointments", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (updatedResponse.ok) {
        const data = await updatedResponse.json();
        const formattedData = data.map(appointment => ({
          ...appointment,
          dateFormatted: new Date(appointment.date).toLocaleDateString(),
          timeFormatted: appointment.time.substring(0, 5),
          statusColor: getStatusColor(appointment.status)
        }));
        setAppointmentList(formattedData);
        setFilteredAppointments(formattedData);
      }

      return true;
    } catch (error) {
      console.error("Error updating appointment:", error);
      throw error;
    }
  };

  const updateAppointmentStatus = async (id, status) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("You must be logged in");

      const response = await fetch(`http://localhost:5000/api/appointments/status/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update appointment status");
      }

      // Update local state
      const updatedAppointments = appointmentList.map(appointment => {
        if (appointment.id === id) {
          return {
            ...appointment,
            status,
            statusColor: getStatusColor(status)
          };
        }
        return appointment;
      });
      
      setAppointmentList(updatedAppointments);
      setFilteredAppointments(updatedAppointments.filter(appointment => 
        searchTerm === "" || 
        appointment.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.doctor_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.status.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.dateFormatted.toLowerCase().includes(searchTerm.toLowerCase())
      ));

      return true;
    } catch (error) {
      console.error("Error updating appointment status:", error);
      throw error;
    }
  };

  const removeAppointment = async (id) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("You must be logged in");

      const response = await fetch(`http://localhost:5000/api/appointments/delete/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to delete appointment");
      }

      // Update local state
      const updatedAppointments = appointmentList.filter(appointment => appointment.id !== id);
      setAppointmentList(updatedAppointments);
      setFilteredAppointments(updatedAppointments.filter(appointment => 
        searchTerm === "" || 
        appointment.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.doctor_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.status.toLowerCase().includes(searchTerm.toLowerCase()) ||
        appointment.dateFormatted.toLowerCase().includes(searchTerm.toLowerCase())
      ));

      return true;
    } catch (error) {
      console.error("Error removing appointment:", error);
      throw error;
    }
  };

  return {
    appointmentList,
    filteredAppointments,
    searchTerm,
    setSearchTerm,
    error,
    isLoading,
    doctors,
    patients,
    getStatusColor,
    addAppointment,
    updateAppointment,
    updateAppointmentStatus,
    removeAppointment
  };
};

export default useAppointmentData;