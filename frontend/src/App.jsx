import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import React from "react";
import Login from './components/Login.jsx';
import PatientRegistration from './components/PatientRecord.jsx';
import NurseQueue from './components/NurseQueue.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import ProfilePage from './components/ProfilePage.jsx';

function App() {
  return (
    <>
    <head>
      <link rel="icon" type="image/png" href="assets/logo.png" />
    </head>
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
      
              </Routes>
    </Router>
    </>
  );
};

export default App;

