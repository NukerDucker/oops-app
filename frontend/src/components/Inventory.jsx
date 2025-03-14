import "../styles/Global.css";
import "../styles/Inventory.css";
import { useState, useEffect } from "react";
import { 
  TableContainer, 
  Table, 
  TableHead, 
  TableBody, 
  TableRow, 
  TableCell, 
  Paper, 
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  IconButton,
  Menu
} from "@mui/material";
// Import any needed icons
// import AddIcon from '@mui/icons-material/Add';
// import SearchIcon from '@mui/icons-material/Search';
// import EditIcon from '@mui/icons-material/Edit';
// import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const InventoryList = () => {
  // User data states
  const [data, setData] = useState(null);
  const [usernames, setUsernames] = useState([]);
  const [roles, setRoles] = useState([]);
  const [access, setAccess] = useState([]);
  const [profile_image_directory, setProfileImageDirectory] = useState([]);
  
  // Inventory specific states
  const [inventory_list, setInventoryList] = useState([]);
  const [filteredInventory, setFilteredInventory] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [inputValue, setInputValue] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentItem, setCurrentItem] = useState({
    id: '',
    name: '',
    count: '',
    category: '',
    unit_price: ''
  });

  useEffect(() => {
    // Get authentication token from local storage
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return;
    }

    // Fetch user data using authentication
    fetch("http://127.0.0.1:5000/api/user-data", {
      headers: {
        "Authorization": `Bearer ${token}`
      },
    })
      .then((response) => {
        if (!response.ok) {
          if (response.status === 401) {
            localStorage.removeItem("token");
            throw new Error("Your session has expired. Please login again.");
          }
          throw new Error("Failed to fetch data from server");
        }
        return response.json();
      })
      .then((userData) => {
        setData(userData);
        
        // Set user data from API response
        setUsernames([userData.username]);
        setRoles([userData.user_type || "User"]);
        setAccess(userData.allow_access || []);
        setProfileImageDirectory([userData.profile_image_directory || "Profile-Icon.png"]);
        
        // Now fetch real supplies data from the API
        return fetch("http://127.0.0.1:5000/api/supplies", {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch supplies data");
        }
        return response.json();
      })
      .then(suppliesData => {
        // Process supplies data from API
        const processedSupplies = suppliesData.map(supply => ({
          id: supply.id,
          name: supply.name,
          count: supply.quantity,  // Map quantity to count
          category: supply.category,
          unit_price: supply.unit_price,
          total_value: supply.total_value,
          // Add a default image path since API doesn't provide images
          image: getCategoryImage(supply.category) // Get image based on category
        }));
        
        setInventoryList(processedSupplies);
        setFilteredInventory(processedSupplies);
        setError(null);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
        setError(error.message);
        setIsLoading(false);
      });
  }, []);

  // Function to assign images based on category
  const getCategoryImage = (category) => {
    // Map categories to image paths for pharmaceuticals
    const categoryImages = {
      "Antibiotics": "antibiotics.png",
      "Analgesics": "analgesics.png",
      "Antidepressants": "antidepressants.png",
      "Antihypertensives": "antihypertensives.png",
      "Antihistamines": "antihistamines.png",
      "Anti-inflammatory": "anti-inflammatory.png",
      "Vaccines": "vaccines.png"
    };
    
    // Return the mapped image or a default one
    return categoryImages[category] || "drug.svg";
  };

  // Search functionality
  useEffect(() => {
    // Filter inventory based on search term
    if (searchTerm.trim() === "") {
      setFilteredInventory(inventory_list);
    } else {
      const searchTermLower = searchTerm.toLowerCase();
      const filtered = inventory_list.filter(item => 
        item.name.toLowerCase().includes(searchTermLower) || 
        item.id.toString().includes(searchTermLower) || 
        item.count.toString().includes(searchTermLower) ||
        item.category.toLowerCase().includes(searchTermLower)
      );
      setFilteredInventory(filtered);
    }
  }, [searchTerm, inventory_list]);

  // Handle form submission for adding or editing items
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEditing) {
      // Add debugging to see exactly what's being sent
      const requestPayload = {
        id: currentItem.id,
        name: currentItem.name,
        quantity: parseInt(currentItem.count),
        unit_price: parseFloat(currentItem.unit_price),
        category: currentItem.category
      };
      console.log("Sending update request with payload:", requestPayload);

      fetch("http://127.0.0.1:5000/api/inventory/update", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(requestPayload),
      })
        .then((response) => {
          if (!response.ok) {
            // Improved error handling
            return response.text().then(text => {
              console.error("Error details:", text);
              throw new Error(`Failed to update item (status: ${response.status}): ${text}`);
            });
          }
          return response.json();
        })
        .then((data) => {
          // Rest of your success handler remains the same
          console.log("Update success:", data);
          
          const updatedList = inventory_list.map(item => 
            item.id === currentItem.id 
              ? {
                  ...item,
                  name: currentItem.name,
                  count: parseInt(currentItem.count), 
                  category: currentItem.category,
                  unit_price: parseFloat(currentItem.unit_price),
                  image: getCategoryImage(currentItem.category)
                } 
              : item
          );
          
          setInventoryList(updatedList);
          setFilteredInventory(updatedList);
          setShowModal(false);
          alert("Item updated successfully!");
        })
        .catch((error) => {
          console.error("Error updating item:", error);
          alert("Failed to update item: " + error.message);
        });
    } else {
      // Add new inventory item
      fetch("http://127.0.0.1:5000/api/inventory/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify({ 
          name: currentItem.name,
          quantity: parseInt(currentItem.count),
          category: currentItem.category,
          unit_price: parseFloat(currentItem.unit_price)
        }),
      })
        .then(response => {
          if (!response.ok) throw new Error("Failed to add item");
          return response.json();
        })
        .then(data => {
          // Add the new item to the inventory list
          const newItem = {
            id: data.id, // Assuming the API returns the new ID
            name: currentItem.name,
            count: parseInt(currentItem.count),
            category: currentItem.category,
            unit_price: parseFloat(currentItem.unit_price),
            total_value: parseInt(currentItem.count) * parseFloat(currentItem.unit_price),
            image: getCategoryImage(currentItem.category)
          };
          
          const newList = [...inventory_list, newItem];
          setInventoryList(newList);
          setFilteredInventory(newList);
          setShowModal(false);
          alert("New inventory item added successfully!");
        })
        .catch(error => {
          console.error("Error adding inventory:", error);
          alert("Failed to add inventory item: " + error.message);
        });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCurrentItem({
      ...currentItem,
      [name]: value
    });
  };

  const handleRemoveItem = (itemId) => {
    fetch("http://127.0.0.1:5000/api/inventory/remove", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("token")}`
      },
      body: JSON.stringify({ 
        inventoryId: itemId
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete item");
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
        const updatedList = inventory_list.filter(inv => inv.id !== itemId);
        setInventoryList(updatedList);
        setFilteredInventory(updatedList);
        alert("Item removed successfully!");
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Failed to remove item: " + error.message);
      });
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

  if (isLoading) return (
    <div className="ContainerPage">
      <div className="loading-container">
        <Typography variant="body1">Loading medication data...</Typography>
      </div>
    </div>
  );

  if (!data) return <Typography>Loading...</Typography>;

  return (
    <>
    <head>
      <title>MedSoft - Inventory</title>
    </head>
   
    <div className="ContainerPage">
      <div className="ContainerPageUIBoundary">
        <div className="ContainerPageLeftPanel">
          <img src="logo.png" className="logo" alt="Logo" />
          <Typography>{roles.join(", ")}</Typography>
          <img
            src={profile_image_directory[0]}
            className="profile-icon"
            alt="Profile"
          />
          <Typography>{usernames.join(", ")}</Typography>
          <div className="HL1"></div>

          <div className="ContainerColumnContainer" style={{alignItems: "center"}}>
            {access.map((access, index) => (
              <div className="Link" key={index}>
                <a href={access.access_link}>{access.access}</a>
              </div>
            ))}
          </div>
        </div>

        <div className="VL1"></div>
        <div className="ContainerPageMiddlePanel">
          <div className="ContainerRowContainer" style={{alignItems: "center", marginTop: "2rem"}}>
            <Typography variant="h5" className="MidPanelTopText" sx={{ fontWeight: 'bold' }}>Drug Inventory</Typography>
            
            {/* Search Bar with Material UI */}
            <TextField
              variant="outlined"
              placeholder="Search by name, ID, category or count"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              size="small"
              sx={{ 
                ml: 2, 
                flex: 1,
                backgroundColor: 'rgba(236, 230, 240, 0.8)',
                borderRadius: '60px',
                '& .MuiOutlinedInput-root': {
                  borderRadius: '60px'
                }
              }}
              InputProps={{
                endAdornment: (
                  <Button sx={{ minWidth: '35px', p: 0 }}>
                    <img src="search-icon.png" alt="Search" style={{ width: '15px', height: '15px' }} />
                  </Button>
                ),
              }}
            />
            
            {/* Register Button with Material UI */}
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
              <img src="plus.png" alt="Register" style={{ width: '20px', marginRight: '8px' }} />
              Register Medication
            </Button>
          </div>
          
          <div className="HL1"></div>
          
          {/* Material UI Table */}
          <TableContainer 
            component={Paper} 
            sx={{ 
              maxHeight: '50rem', 
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
                          sx={{ mr: 1 , backgroundColor: 'var(--accent-color)', color: 'white' }}
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
      </div>
      
      {/* Material UI Dialog for Add/Edit Form */}
      <Dialog open={showModal} onClose={() => setShowModal(false)} maxWidth="sm" fullWidth>
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
            <div>
              <Button onClick={() => setShowModal(false)} color="primary" sx={{ mr: 1 }}>
                Cancel
              </Button>
              <Button type="submit" color="primary" variant="contained">
                {isEditing ? 'Update' : 'Add Item'}
              </Button>
            </div>
          </DialogActions>
        </form>
      </Dialog>
    </div>
    </>
  );
}

export default InventoryList;