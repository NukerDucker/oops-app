import React, { useState, useEffect } from "react";
import "../styles/Inventory.css"; // Import Inventory styles
import { Grid2, Typography, Button, Box, Paper, IconButton } from '@mui/material';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIosNew';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import UserProfile from "./UserProfile";
import useUserData from "../hooks/useUserData";

const Main = () => {
  const { 
    data, 
    usernames, 
    roles, 
    access, 
    profile_image_directory, 
    error, 
    isLoading 
  } = useUserData();
  
  const [tasks, setTasks] = useState([]);
  const [weekly_tasks, setWeeklyTasks] = useState([]);
  const [currentSlide, setCurrentSlide] = useState(0);
  
  // Define your slides - replace with your actual slide content/images
  const slides = [
    "https://images.pexels.com/photos/236380/pexels-photo-236380.jpeg?cs=srgb&dl=pexels-pixabay-236380.jpg&fm=jpg",
    "https://images.pexels.com/photos/236380/pexels-photo-236380.jpeg?cs=srgb&dl=pexels-pixabay-236380.jpg&fm=jpg",
    "https://images.pexels.com/photos/236380/pexels-photo-236380.jpeg?cs=srgb&dl=pexels-pixabay-236380.jpg&fm=jpg",
    "https://images.pexels.com/photos/236380/pexels-photo-236380.jpeg?cs=srgb&dl=pexels-pixabay-236380.jpg&fm=jpg",
  ];
  
  const totalSlides = slides.length;
  
  useEffect(() => {
    if (data) {
      setTasks(data.tasks || []);
      setWeeklyTasks(data.weekly_tasks || []);
    }
  }, [data]);

  useEffect(() => {
    // Auto-rotation for carousel
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide + 1) % totalSlides);
    }, 7000); // Change slide every 7 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, [totalSlides]);

  const nextSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % totalSlides);
  };

  const prevSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide - 1 + totalSlides) % totalSlides);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  // Show error message if there was an error fetching data
  if (error) return (
    <div className="ContainerPage">
      <div className="error-container">
        <p className="error-message">{error}</p>
        <Button 
          variant="contained" 
          onClick={() => window.location.href = "/login"}
        >
          Go to Login
        </Button>
      </div>
    </div>
  );

  if (isLoading) return <Typography className="Loading">Loading...</Typography>;

  return (
    <div className="parent-card">
      <Grid2 container spacing={2} sx={{ height: '100%', width: '100%' }}>
        {/* User profile component */}
        <UserProfile 
          usernames={usernames}
          roles={roles}
          profile_image_directory={profile_image_directory}
          access={access}
        />
        
        {/* Right column - Main content */}
        <Grid2 xs={8} sx={{ display: 'flex', flexDirection: 'column', padding: 2, width: '85%' }}>
          <Box sx={{ flexGrow: 0, marginBottom: 2 }}>
            <Typography variant="h5" component="h2" sx={{ mb: 2 }}>
              Welcome Back, <strong>{usernames[0]}</strong>
            </Typography>
          </Box>

          {/* Carousel section */}
          <Box sx={{ 
            flexGrow: 0, 
            height: '40%', 
            mb: 2,
            borderRadius: '10px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
          }}>
            {/* Carousel content stays the same */}
            <div style={{ position: 'relative', height: '100%', width: '100%' }}>
              <img 
                src={slides[currentSlide]} 
                alt={`Slide ${currentSlide + 1}`} 
                style={{ 
                  width: '100%', 
                  height: '100%',
                  maxHeight: '400px', 
                  objectFit: 'cover', 
                  borderRadius: '10px' 
                }}
              />
              <IconButton
                onClick={prevSlide}
                sx={{
                  position: 'absolute',
                  left: '10px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  bgcolor: 'rgba(255, 255, 255, 0.7)',
                  '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.9)' }
                }}
              >
                <ArrowBackIosIcon />
              </IconButton>
              <IconButton
                onClick={nextSlide}
                sx={{
                  position: 'absolute',
                  right: '10px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  bgcolor: 'rgba(255, 255, 255, 0.7)',
                  '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.9)' }
                }}
              >
                <ArrowForwardIosIcon />
              </IconButton>
            </div>
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'center', 
              mt: 1 
            }}>
              {slides.map((_, index) => (
                <Box
                  key={index}
                  onClick={() => goToSlide(index)}
                  sx={{
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    mx: 0.5,
                    bgcolor: currentSlide === index ? 'primary.main' : 'grey.400',
                    cursor: 'pointer',
                    transition: 'background-color 0.3s'
                  }}
                />
              ))}
            </Box>
          </Box>

          {/* Tasks section - unchanged */}
          <Box sx={{ 
            flexGrow: 1, 
            display: 'flex', 
            flexDirection: 'column',
            mt: 2
          }}>
            <Grid2 container spacing={2}>
              {/* Upcoming Appointments */}
              <Grid2 xs={6}>
                <Typography variant="h6" sx={{ mb: 2 }}>Upcoming Appointments</Typography>
                {tasks.length > 0 ? (
                  tasks.map((task, index) => (
                    <Paper
                      key={index}
                      elevation={2}
                      sx={{ 
                        p: 2, 
                        mb: 2, 
                        borderRadius: '10px',
                        '&:hover': { backgroundColor: 'rgba(236, 230, 240, 0.4)' }, 
                        border: '1px solid var(--border-color)'
                      }}
                    >
                      <Typography variant="subtitle1" fontWeight="bold">
                        Appointment #{index + 1}
                      </Typography>
                      <Typography variant="subtitle2">
                        {task.title}
                      </Typography>
                      <Typography variant="body2">
                        {task.description}
                      </Typography>
                    </Paper>
                  ))
                ) : (
                  <Typography variant="body2">No upcoming appointments</Typography>
                )}
              </Grid2>
              
              {/* Weekly Tasks */}
              <Grid2 xs={6}>
                <Typography variant="h6" sx={{ mb: 2 }}>Weekly Tasks</Typography>
                {weekly_tasks.length > 0 ? (
                  weekly_tasks.map((weekly_task, index) => (
                    <Paper
                      key={index}
                      elevation={2}
                      sx={{ 
                        p: 2, 
                        mb: 2, 
                        borderRadius: '10px',
                        '&:hover': { backgroundColor: 'rgba(236, 230, 240, 0.4)' }, 
                        border: '1px solid var(--border-color)'
                      }}
                    >
                      <Typography variant="subtitle1" fontWeight="bold">
                        Weekly Task #{index + 1}
                      </Typography>
                      <Typography variant="subtitle2">
                        {weekly_task.title}
                      </Typography>
                      <Typography variant="body2">
                        {weekly_task.description}
                      </Typography>
                    </Paper>
                  ))
                ) : (
                  <Typography variant="body2">No weekly tasks</Typography>
                )}
              </Grid2>
            </Grid2>
          </Box>
        </Grid2>
      </Grid2>
    </div>
  );
};

export default Main;