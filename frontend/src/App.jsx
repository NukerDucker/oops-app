import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import React from "react";
import Login from './components/Login.jsx';
import Inventory from './components/Inventory.jsx';
import Main from './components/Main.jsx';
import Patient from './components/Patient.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';

function App() {
  return (
    <>
    <head>
      <link rel="icon" type="image/png" href="assets/logo.png" />
    </head>
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
          <Route path="/inventory" element={ <ProtectedRoute> <Inventory /> </ProtectedRoute>}/>
          <Route path="/main" element={<ProtectedRoute> <Main /> </ProtectedRoute>} />
          <Route path="/patient" element={<ProtectedRoute> <Patient /> </ProtectedRoute>} />
      </Routes>
    </Router>
    </>
  );
};

export default App;

