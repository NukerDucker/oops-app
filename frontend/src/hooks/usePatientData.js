import { useState, useEffect } from 'react';

const usePatientData = () => {
  const [patientList, setPatientList] = useState([]);
  const [filteredPatients, setFilteredPatients] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return;
    }

    fetch("http://127.0.0.1:5000/api/patients", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch patients data");
        }
        return response.json();
      })
      .then(patientData => {
        // Process patient data 
        const processedPatients = patientData.map(patient => ({
          id: patient.id,
          name: patient.name,
          age: patient.age,
          gender: patient.gender,
          contact: patient.contact,
          history: patient.history,
          image: "Profile-Icon.png" // Default image
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
    if (searchTerm.trim() === "") {
      setFilteredPatients(patientList);
    } else {
      const searchTermLower = searchTerm.toLowerCase();
      const filtered = patientList.filter(patient => 
        patient.name.toLowerCase().includes(searchTermLower) || 
        patient.id.toString().includes(searchTermLower) || 
        patient.age.toString().includes(searchTermLower) ||
        (patient.gender && patient.gender.toLowerCase().includes(searchTermLower)) ||
        (patient.contact && patient.contact.toLowerCase().includes(searchTermLower))
      );
      setFilteredPatients(filtered);
    }
  }, [searchTerm, patientList]);

  // Functions to update patient list after CRUD operations
  const addPatient = (newPatient) => {
    const updatedList = [...patientList, {...newPatient, image: "Profile-Icon.png"}];
    setPatientList(updatedList);
    setFilteredPatients(updatedList);
  };

  const updatePatient = (updatedPatient) => {
    const updatedList = patientList.map(patient => 
      patient.id === updatedPatient.id ? {
        ...patient,
        name: updatedPatient.name,
        age: parseInt(updatedPatient.age),
        gender: updatedPatient.gender,
        contact: updatedPatient.contact
      } : patient
    );
    
    setPatientList(updatedList);
    setFilteredPatients(updatedList);
  };

  const deletePatient = (patientId) => {
    const updatedList = patientList.filter(patient => patient.id !== patientId);
    setPatientList(updatedList);
    setFilteredPatients(updatedList);
  };

  return {
    patientList,
    setPatientList,
    filteredPatients,
    searchTerm,
    setSearchTerm,
    error,
    isLoading,
    addPatient,
    updatePatient,
    deletePatient
  };
};

export default usePatientData;