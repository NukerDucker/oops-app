import React, { useState } from "react";
import { 
  Grid2, Typography, Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, Button, AppBar, Box, Toolbar, 
  InputBase, TextField, Dialog, DialogTitle, DialogContent, DialogActions, 
  FormControl, InputLabel, Select, MenuItem, styled, alpha 
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import useUserData from "../hooks/useUserData";
import useInventoryData from "../hooks/useInventoryData";
import UserProfile from "./UserProfile";
import "../styles/Inventory.css";

// Styled components for search
const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));

function Inventory() {
  // Use the custom hooks
  const { 
    usernames, roles, access, profile_image_directory, 
    error: userError, isLoading: userLoading 
  } = useUserData();
  
  const {
    filteredInventory, searchTerm, setSearchTerm,
    error: inventoryError, isLoading: inventoryLoading,
    getCategoryImage, addInventoryItem, updateInventoryItem, removeInventoryItem
  } = useInventoryData();
  
  // Local UI state
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentItem, setCurrentItem] = useState({
    id: '',
    name: '',
    count: '',
    category: '',
    unit_price: ''
  });

  // Handle form submission for adding or editing items
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEditing) {
      updateInventoryItem(currentItem)
        .then(() => {
          setShowModal(false);
          alert("Item updated successfully!");
        })
        .catch((error) => {
          console.error("Error updating item:", error);
          alert("Failed to update item: " + error.message);
        });
    } else {
      addInventoryItem(currentItem)
        .then(() => {
          setShowModal(false);
          alert("New inventory item added successfully!");
        })
        .catch(error => {
          console.error("Error adding inventory:", error);
          alert("Failed to add inventory item: " + error.message);
        });
    }
  };

  // Handle input changes in the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentItem({
      ...currentItem,
      [name]: value
    });
  };

  // Handle item removal
  const handleRemoveItem = (itemId) => {
    removeInventoryItem(itemId)
      .then(() => {
        alert("Item removed successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to remove item: " + error.message);
      });
  };

  const error = userError || inventoryError;
  const isLoading = userLoading || inventoryLoading;

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

  if (isLoading) return (
    <div className="ContainerPage">
      <div className="loading-container">
        <Typography variant="body1">Loading Medication Data...</Typography>
      </div>
    </div>
  );

  return (
      <div className="parent-card">
        <Grid2 container spacing={2} sx={{ height: '100%',width: '100%' }}>
          {/* Left column - User profile */}
          <UserProfile 
            usernames={usernames}
            roles={roles}
            access={access}
            profile_image_directory={profile_image_directory}
          />
          
          {/* Right column - Inventory table */}
          <Grid2 xs={8} sx={{ display: 'flex', flexDirection: 'column', padding: 2, width: '85%' }}>
            {/* Search bar header */}
            <Box sx={{ flexGrow: 0, marginBottom: 2, borderRadius: '30px', backgroundColor: 'none' }}>
              <AppBar position="static" sx={{ backgroundColor: 'none'}}>
                <Toolbar sx={{ backgroundColor: 'none'}}>
                  <Typography
                    variant="h6"
                    noWrap
                    component="div"
                    sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
                  >
                    Inventory
                  </Typography>
                  <Search>
                    <SearchIconWrapper>
                      <SearchIcon />
                    </SearchIconWrapper>
                    <StyledInputBase
                      placeholder="Search…"
                      inputProps={{ 'aria-label': 'search' }}
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </Search>
                  <Button 
                    variant="contained" 
                    onClick={() => {
                      setIsEditing(false);
                      setCurrentItem({
                        id: '',
                        name: '',
                        count: '',
                        category: '',
                        unit_price: ''
                      });
                      setShowModal(true);
                    }}
                    sx={{ 
                      ml: 2, 
                      backgroundColor: 'var(--accent-color)', 
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    Register Medication
                  </Button>
                </Toolbar>
              </AppBar>
            </Box>

            {/* Table container */}
            <div className="table-container" style={{ 
              flexGrow: 1, 
              width: '100%', 
              height: 'calc(90vh - 150px)',
              overflow: 'hidden',
            }}>
              <TableContainer 
                component={Paper} 
                sx={{ 
                  height: '100%',
                  maxHeight: '100%',
                  overflow: 'auto',
                  mt: 2,
                  backgroundColor: 'transparent',
                  boxShadow: 'none'
                }}
              >
                <Table stickyHeader aria-label="inventory table">
                  <TableHead>
                    <TableRow>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '60px' }}>ID</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '80px' }}>Image</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Medication Name</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold' }}>Count</TableCell>
                      <TableCell sx={{ fontWeight: 'bold' }}>Category</TableCell>
                      <TableCell align="right" sx={{ fontWeight: 'bold' }}>Unit Price ($)</TableCell>
                      <TableCell align="center" sx={{ fontWeight: 'bold', width: '120px' }}>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredInventory.length > 0 ? (
                      filteredInventory.map((item) => (
                        <TableRow 
                          key={item.id}
                          sx={{ 
                            '&:hover': { backgroundColor: 'rgba(236, 230, 240, 0.4)' }, 
                            borderRadius: '15px',
                            mb: 1,
                            border: '2px solid var(--border-color)'
                          }}
                        >
                          <TableCell align="center">{item.id}</TableCell>
                          <TableCell align="center">
                            <img 
                              src={item.image} 
                              alt="medication" 
                              style={{ width: '50px', height: '50px', borderRadius: '50%' }}
                            />
                          </TableCell>
                          <TableCell>{item.name}</TableCell>
                          <TableCell align="center">{item.count}</TableCell>
                          <TableCell>{item.category}</TableCell>
                          <TableCell align="right">${parseFloat(item.unit_price).toFixed(2)}</TableCell>
                          <TableCell align="center">
                            <Button
                              variant="contained"
                              size="small"
                              sx={{ mr: 1, backgroundColor: 'var(--accent-color)', color: 'white' }}
                              onClick={() => {
                                setIsEditing(true);
                                setCurrentItem({
                                  id: item.id,
                                  name: item.name,
                                  count: item.count.toString(),
                                  category: item.category,
                                  unit_price: item.unit_price ? item.unit_price.toString() : ''
                                });
                                setShowModal(true);
                              }}
                            >
                              Edit
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    ) : (
                      <TableRow>
                        <TableCell colSpan={7} align="center">No inventory items found</TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </div>
          </Grid2>
        </Grid2>
        
        {/* Dialog for Add/Edit Form */}
        <Dialog 
          open={showModal} 
          onClose={() => setShowModal(false)} 
          maxWidth="sm" 
          fullWidth
        >
          <DialogTitle>
            {isEditing ? 'Edit Medication' : 'Register New Medication'}
          </DialogTitle>
          <form onSubmit={handleSubmit}>
            <DialogContent>
              <TextField
                margin="dense"
                id="name"
                name="name"
                label="Name"
                type="text"
                fullWidth
                variant="outlined"
                value={currentItem.name}
                onChange={handleInputChange}
                required
                sx={{ mb: 2 }}
              />
              
              <TextField
                margin="dense"
                id="count"
                name="count"
                label="Quantity"
                type="number"
                fullWidth
                variant="outlined"
                value={currentItem.count}
                onChange={handleInputChange}
                required
                inputProps={{ min: 0 }}
                sx={{ mb: 2 }}
              />
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel id="category-label">Category</InputLabel>
                <Select
                  labelId="category-label"
                  id="category"
                  name="category"
                  value={currentItem.category}
                  label="Category"
                  onChange={handleInputChange}
                  required
                >
                  <MenuItem value="">Select a category</MenuItem>
                  <MenuItem value="Pain Relief">Pain Relief</MenuItem>
                  <MenuItem value="Antibiotic">Antibiotic</MenuItem>
                  <MenuItem value="Diabetes Management">Diabetes Management</MenuItem>
                  <MenuItem value="Cardiovascular">Cardiovascular</MenuItem>
                  <MenuItem value="Allergy Relief">Allergy Relief</MenuItem>
                  <MenuItem value="Cold & Flu">Cold & Flu</MenuItem>
                  <MenuItem value="Digestive Health">Digestive Health</MenuItem>
                  <MenuItem value="Emergency Allergy Treatment">Emergency Allergy Treatment</MenuItem>
                  <MenuItem value="Sleep Aid">Sleep Aid</MenuItem>
                </Select>
              </FormControl>
              
              <TextField
                margin="dense"
                id="unit_price"
                name="unit_price"
                label="Unit Price"
                type="number"
                fullWidth
                variant="outlined"
                value={currentItem.unit_price}
                onChange={handleInputChange}
                required
                inputProps={{ min: 0, step: "0.01" }}
              />
            </DialogContent>
            <DialogActions sx={{ justifyContent: 'space-between', px: 3, pb: 2 }}>
              {isEditing && (
                <Button 
                  onClick={() => {
                    if(window.confirm("Are you sure you want to delete this item?")) {
                      handleRemoveItem(currentItem.id);
                      setShowModal(false);
                    }
                  }} 
                  color="error" 
                  variant="contained"
                >
                  Delete
                </Button>
              )}
              <Box>
                <Button onClick={() => setShowModal(false)} color="primary" sx={{ mr: 1 }}>
                  Cancel
                </Button>
                <Button type="submit" color="primary" variant="contained">
                  {isEditing ? 'Update' : 'Add Item'}
                </Button>
              </Box>
            </DialogActions>
          </form>
        </Dialog>
      </div>
  );
}

export default Inventory;