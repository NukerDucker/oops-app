import { useState, useEffect } from 'react';

const useMedicalServices = () => {
  const [medications, setMedications] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [selectedMedication, setSelectedMedication] = useState('');
  const [prescriptionQuantity, setPrescriptionQuantity] = useState(1);
  const [selectedDoctor, setSelectedDoctor] = useState('');
  const [calculatedFee, setCalculatedFee] = useState(0);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;
    
    // Fetch medications
    fetch("http://127.0.0.1:5000/api/inventory/medications", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to fetch medications");
        return response.json();
      })
      .then(data => {
        setMedications(data);
      })
      .catch(error => {
        console.error("Error fetching medications:", error);
      });
      
    // Fetch doctors list
    fetch("http://127.0.0.1:5000/api/doctors", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to fetch doctors");
        return response.json();
      })
      .then(data => {
        setDoctors(data);
      })
      .catch(error => {
        console.error("Error fetching doctors:", error);
      });
  }, []);

  // Handle medication change to calculate fees
  const handleMedicationChange = (valueOrEvent) => {
    // Handle both direct value or event object
    const medId = valueOrEvent && valueOrEvent.target ? 
      valueOrEvent.target.value : valueOrEvent;
    
    setSelectedMedication(medId);
    
    const medication = medications.find(med => med.id === medId);
    if (medication) {
      setCalculatedFee(medication.price * prescriptionQuantity);
    }
  };

  // Handle quantity change
  const handleQuantityChange = (valueOrEvent) => {
    // Handle both direct value or event object
    const quantity = valueOrEvent && valueOrEvent.target ? 
      parseInt(valueOrEvent.target.value) || 1 : 
      parseInt(valueOrEvent) || 1;
    
    setPrescriptionQuantity(quantity);
    
    if (selectedMedication) {
      const medication = medications.find(med => med.id === selectedMedication);
      if (medication) {
        setCalculatedFee(medication.price * quantity);
      }
    }
  };

  // Handle doctor change
  const handleDoctorChange = (valueOrEvent) => {
    // Handle both direct value or event object
    const doctorId = valueOrEvent && valueOrEvent.target ? 
      valueOrEvent.target.value : valueOrEvent;
    
    setSelectedDoctor(doctorId);
  };

  // Create prescription
  const createPrescription = (patientId) => {
    if (!selectedMedication || !selectedDoctor) {
      setError("Please select both medication and doctor");
      return Promise.reject("Incomplete data");
    }
    
    const token = localStorage.getItem("token");
    
    return fetch(`http://127.0.0.1:5000/api/patients/${patientId}/prescriptions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        medication_id: selectedMedication,
        doctor_id: selectedDoctor,
        quantity: prescriptionQuantity,
        fee: calculatedFee
      })
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed to create prescription");
        return response.json();
      });
  };

  return {
    medications,
    doctors,
    selectedMedication,
    setSelectedMedication,
    prescriptionQuantity, 
    setPrescriptionQuantity,
    selectedDoctor,
    setSelectedDoctor,
    calculatedFee,
    handleMedicationChange,
    handleQuantityChange,
    handleDoctorChange,  // Added this export
    createPrescription,
    error
  };
};

export default useMedicalServices;