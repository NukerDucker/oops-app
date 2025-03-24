import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

// Material UI imports
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import FilledInput from "@mui/material/FilledInput";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";

// Icons
import LoginIcon from "@mui/icons-material/Login";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const handleMouseDownPassword = (event) => event.preventDefault();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setIsLoading(true);
    
    try {
      console.log("Sending login request:", formData);
      
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      console.log("Response status:", response.status);
      const data = await response.json();
      console.log("Response data:", data);
      
      if (!response.ok) {
        throw new Error(data.error || `Server returned ${response.status}`);
      }
      
      // Store the token (check both formats for compatibility)
      const token = data.access_token || data.token;
      if (token) {
        localStorage.setItem("token", token);
        
        // Also store user info if available
        if (data.user) {
          localStorage.setItem("user", JSON.stringify(data.user));
        }
        
        // Redirect to main page or first available route
        const userObj = data.user || {};
        const access = userObj.access || userObj.allow_access || [];
        
        let redirectPath = "/main";
        if (access.length > 0) {
          redirectPath = access[0].path || "/main";
        }
        
        navigate(redirectPath);
      } else {
        throw new Error("No access token received");
      }
    } catch (error) {
      console.error("Login error:", error);
      setErrorMessage(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container-page">
      <Container maxWidth="sm">
        <Box className="login-container">
          <div className="login-header">
            <img src="/logo.png" alt="MedSoft Logo" className="login-logo" />
          </div>
          
          <form onSubmit={handleSubmit} className="login-form">
            <TextField
              required
              name="username"
              label="Username"
              value={formData.username}
              onChange={handleChange}
              fullWidth
              margin="normal"
              variant="filled"
            />
            
            <FormControl fullWidth margin="normal" variant="filled">
              <InputLabel htmlFor="filled-password-input">Password</InputLabel>
              <FilledInput
                id="filled-password-input"
                name="password"
                type={showPassword ? "text" : "password"}
                value={formData.password}
                onChange={handleChange}
                required
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
            
            {errorMessage && (
              <Alert severity="error" sx={{ width: '100%', mt: 2 }}>
                {errorMessage}
              </Alert>
            )}
            
            <Button
              type="submit"
              variant="contained"
              sx={{ 
                borderRadius: '10px', 
                height: '3rem', 
                margin: '3px',
                mt: 3, 
                bgcolor: '#AD69CC', 
                color: 'rgb(242, 242, 247)',
                '&:hover': {
                  bgcolor: '#8A4FBA'
                } 
              }}
              endIcon={<LoginIcon />}
              fullWidth
              disabled={isLoading}
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </Button>
          </form>
        </Box>
      </Container>
    </div>
  );
};

export default Login;
