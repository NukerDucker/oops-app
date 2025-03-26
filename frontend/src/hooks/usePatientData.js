import { useState, useEffect } from 'react';

const usePatientData = () => {
  const [patientList, setPatientList] = useState([]);
  const [filteredPatients, setFilteredPatients] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedPatientDetails, setSelectedPatientDetails] = useState(null);
  const [historyEntries, setHistoryEntries] = useState([]);

  useEffect(() => {
    fetchPatients();
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

  const fetchPatients = () => {
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
  };

  const updatePatient = (updatedPatient) => {
    return fetch(`http://127.0.0.1:5000/api/patients/update/${updatedPatient.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(updatedPatient),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to update patient");
        return response.json();
      })
      .then((data) => {
        // Update the patient in the list
        const updatedList = patientList.map((patient) =>
          patient.id === updatedPatient.id ? { ...patient, ...updatedPatient } : patient
        );
        setPatientList(updatedList);
        setFilteredPatients(updatedList);
        return data;
      })
      .catch((error) => {
        console.error("Error updating patient:", error);
        throw error;
      });
  };

// Update the createPatient function to add the new patient to the state
const addPatient = (patientData) => {
  return fetch("http://127.0.0.1:5000/api/patients/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify(patientData),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Failed to add patient");
      return response.json();
    })
    .then((data) => {
      // Add the new patient to the list
      const newPatient = {
        id: data.id,
        name: patientData.name,
        age: parseInt(patientData.age),
        gender: patientData.gender,
        contact: patientData.contact,
        image: "Profile-Icon.png", // Default image
      };

      const updatedList = [...patientList, newPatient];
      setPatientList(updatedList);
      setFilteredPatients(updatedList);
      return data;
    });
};

  const deletePatient = (patientId) => {
    return fetch(`http://127.0.0.1:5000/api/patients/delete/${patientId}`, {
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
        const updatedList = patientList.filter(patient => patient.id !== patientId);
        setPatientList(updatedList);
        setFilteredPatients(updatedList);
        return data;
      });
  };

  // Patient history operations
  const fetchPatientHistory = (patientId) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/history`, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to load patient history");
        return response.json();
      })
      .then(data => {
        if (data.histories) {
          const processedPatientsHistory = data.histories.map(entry => ({
            history: entry
          }));
          setHistoryEntries(processedPatientsHistory);
          return processedPatientsHistory;
        } 
        else if (data.history) {
          const processedPatientsHistory = data.history.map(entry => ({
            history: entry.history
          }));
          setHistoryEntries(processedPatientsHistory || []);
          return data.history || [];
        }
        // Handle case where neither format is present
        else {
          setHistoryEntries([]);
          return [];
        }
      });
  };

  const addHistoryEntry = (patientId, entry) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/history/add`, {
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
        setHistoryEntries(prevEntries => [...prevEntries, entry]);
        return data;
      });
  };

  const updateHistoryEntry = (patientId, index, entry) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/history/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ 
        index,
        entry 
      }),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to update history entry");
        return response.json();
      })
      .then(data => {
        const updatedEntries = [...historyEntries];
        updatedEntries[index] = entry;
        setHistoryEntries(updatedEntries);
        return data;
      });
  };

  const deleteHistoryEntry = (patientId, index) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/history/delete`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ index }),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to delete history entry");
        return response.json();
      })
      .then(data => {
        setHistoryEntries(prevEntries => 
          prevEntries.filter((_, i) => i !== index)
        );
        return data;
      });
  };

  // Patient details operations
  const fetchPatientDetails = (patientId) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}`, {
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
        return data;
      });
  };

  // Add treatment
  const addTreatment = (patientId, treatmentData) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/treatments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify(treatmentData),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to add treatment");
        return response.json();
      });
  };

  // Update treatment
  const updateTreatment = (patientId, treatmentId, treatmentData) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/treatments/${treatmentId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify(treatmentData),
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to update treatment");
        return response.json();
      });
  };

  const fetchPatientTreatments = (patientId) => {
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
      });
  };

  // Delete treatment
  const deleteTreatment = (patientId, treatmentId) => {
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/treatments/${treatmentId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to delete treatment");
        return response.json();
      });
  };

  return {
    patientList,
    filteredPatients,
    searchTerm,
    setSearchTerm,
    error,
    isLoading,
    selectedPatientDetails,
    setSelectedPatientDetails,
    historyEntries,
    setHistoryEntries,
    // CRUD operations
    addPatient,
    updatePatient,
    deletePatient,
    // History operations
    fetchPatientHistory,
    addHistoryEntry,
    updateHistoryEntry,
    deleteHistoryEntry,
    // Details operations
    fetchPatientDetails,
    // Treatment operations
    fetchPatientTreatments,
    addTreatment,
    updateTreatment,
    deleteTreatment,
  };
};

export default usePatientData;