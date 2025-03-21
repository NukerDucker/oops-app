import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Helmet } from 'react-helmet';
import "../styles/Login.css";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import FilledInput from "@mui/material/FilledInput";

import LoginIcon from "@mui/icons-material/Login";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",  // Default test username
    password: ""     // Default test password
  });
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const handleMouseDownPassword = (event) => event.preventDefault();
  const handleSubmit = (e) => {
    e.preventDefault();
    // Send the login request to the backend
    fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.access_token) {
          // Store token in localStorage
          localStorage.setItem("token", data.access_token);
          navigate("/main");
        } else {
          alert("Login failed");
        }
      })
      .catch((err) => {
        console.error("Error during login:", err);
        alert("Login failed");
      });
  };

  return (
<>
    <Helmet>
      <title>MedSoft - Login</title>
    </Helmet>
    <div className="container-page">
      <main className="login-container">
      <div className="login-header">
        <img src="logo.png" alt="MedSoft Logo" className="login-logo" />
      </div>
        <TextField
          required
          name="username"
          label="Username"
          value={formData.username}
          onChange={handleChange}
          sx={{ width: '100%', margin: '1rem' }}
          variant="filled"
        />
        
        <FormControl sx={{ width: '100%', margin: '1rem' }} variant="filled">
          <InputLabel htmlFor="filled-password-input">Password</InputLabel>
          <FilledInput
            id="filled-password-input"
            name="password"
            type={showPassword ? "text" : "password"}
            value={formData.password}
            onChange={handleChange}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label={showPassword ? "hide password" : "show password"}
                  onClick={togglePasswordVisibility}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
          />
        </FormControl>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <Button
          type="submit"
          variant="contained"
          sx={{ borderRadius: '10px', width: '30%', height: '3rem', margin: '3px', bgcolor: '#AD69CC', color: 'rgb(242, 242 ,247)' }}
          endIcon={<LoginIcon />}
          fullWidth
          onClick={handleSubmit}
        >
          Sign In
        </Button>
      </main>
    </div>
    </>
  );
};

export default Login;
