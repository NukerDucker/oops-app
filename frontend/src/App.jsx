import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import React from "react";
import Login from './components/Login.jsx';
import Inventory from './components/Inventory.jsx';
import Main from './components/Main.jsx';
import Patient from './components/Patient.jsx';
import Appointments from './components/Appointments.jsx';
import ProtectedRoute from './components/ProtectedRoute.jsx';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Create a custom theme with your accent color
const theme = createTheme({
  palette: {
    primary: {
      main: '#ad69cc', // Your accent color
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <>
      <head>
        <link rel="icon" type="image/png" href="favicon.png" />
      </head>
      <Router>
        <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/inventory" element={ <ProtectedRoute> <Inventory /> </ProtectedRoute>}/>
            <Route path="/main" element={<ProtectedRoute> <Main /> </ProtectedRoute>} />
            <Route path="/patient" element={<ProtectedRoute> <Patient /> </ProtectedRoute>} />
            <Route path="/appointments" element={<ProtectedRoute> <Appointments /> </ProtectedRoute>} />
        </Routes>
      </Router>
      </>
    </ThemeProvider>
  );
};

export default App;

