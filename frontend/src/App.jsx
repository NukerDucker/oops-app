import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import React from "react";
import Login from './components/Login.jsx';

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

