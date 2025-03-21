import React from "react";
import { Grid2, Typography, Button, Divider } from '@mui/material';

const UserProfile = ({ usernames, roles, profile_image_directory, access }) => {
  return (
    <Grid2 xs={4} sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      borderRight: '1px solid rgba(0, 0, 0, 0.12)',
      padding: 2
    }}>
      <div className="user-card-container" style={{ 
        width: '100%', 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center' 
      }}>
        <img 
          src="logo.png" 
          id="logo" 
          alt="Logo" 
          style={{ maxWidth: '80%', margin: '0'}} 
        />
        <p className="user-type" style={{margin: '1rem 0', padding:'0'}}>
          {Array.isArray(roles) && roles.length > 0 ? roles.join(", ") : "User"}
        </p>
        <img 
          src={Array.isArray(profile_image_directory) && profile_image_directory.length > 0 
            ? profile_image_directory[0] 
            : "Profile-Icon.png"} 
          alt="user-image" 
          style={{ maxWidth: '120px', borderRadius: '50%', margin: '0' }} 
        />
        <p className="username" style={{margin: '1rem 0', padding:'0'}}>
          {Array.isArray(usernames) && usernames.length > 0 ? usernames[0] : "User"}
        </p>
        <Divider variant="middle" style={{ width: '100%'}}/>
        
        {access && access.map((item, index) => (
          <Button 
            href={item.access_link} 
            key={index}
            fullWidth
            variant="contained" 
            sx={{ justifyContent: 'flex-start', padding: '0.5rem 1rem', marginTop: '0.50rem' }}
          >
            {item.access}
          </Button>
        ))}
      </div>
    </Grid2>
  );
};

export default UserProfile;