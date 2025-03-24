import { useState, useEffect } from 'react';

const useInventoryData = () => {
  const [inventory_list, setInventoryList] = useState([]);
  const [filteredInventory, setFilteredInventory] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

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
      "Vaccines": "vaccines.png",
      "Pain Relief": "analgesics.png",
      "Cold & Flu": "antihistamines.png",
      "Allergy Relief": "antihistamines.png",
      "Cardiovascular": "antihypertensives.png",
      "Diabetes Management": "diabetes.png",
      "Digestive Health": "digestive.png",
      "Emergency Allergy Treatment": "allergy.png",
      "Sleep Aid": "sleep.png"
    };
    
    // Return the mapped image or a default one
    return `/images/medications/${categoryImages[category] || "drug.svg"}`;
  };

  const fetchInventory = () => {
    setIsLoading(true);
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return Promise.reject("No authentication token");
    }

    return fetch("http://127.0.0.1:5000/api/inventory", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(response => {
        if (!response.ok) {
          if (response.status === 403) {
            throw new Error("You don't have permission to access inventory");
          }
          throw new Error("Failed to fetch inventory data");
        }
        return response.json();
      })
      .then(inventoryData => {
        // Process inventory data from API
        const processedInventory = inventoryData.map(supply => ({
          id: supply.id,
          name: supply.name,
          count: supply.quantity, // Map quantity to count
          category: supply.category,
          unit_price: supply.unit_price,
          total_value: supply.total_value,
          image: getCategoryImage(supply.category)
        }));
        
        setInventoryList(processedInventory);
        setFilteredInventory(processedInventory);
        setError(null);
        setIsLoading(false);
        return processedInventory;
      })
      .catch((error) => {
        console.error("Error fetching data: ", error);
        setError(error.message);
        setIsLoading(false);
        throw error;
      });
  };

  useEffect(() => {
    fetchInventory().catch(err => console.error("Initial data fetch failed:", err));
  }, []);

  // Search functionality
  useEffect(() => {
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

  // CRUD operations for inventory
  const addInventoryItem = (newItem) => {
    const token = localStorage.getItem("token");
    if (!token) {
      return Promise.reject(new Error("Authentication required"));
    }
    
    // Validate fields before sending
    if (!newItem.name || !newItem.count || !newItem.category || !newItem.unit_price) {
      return Promise.reject(new Error("All fields are required"));
    }
    
    return fetch("http://127.0.0.1:5000/api/inventory/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ 
        name: newItem.name,
        quantity: parseInt(newItem.count),
        category: newItem.category,
        unit_price: parseFloat(newItem.unit_price)
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.error || "Failed to add item");
          });
        }
        return response.json();
      })
      .then(data => {
        // Refresh inventory data to ensure consistency
        return fetchInventory();
      });
  };

  const updateInventoryItem = (updatedItem) => {
    const token = localStorage.getItem("token");
    if (!token) {
      return Promise.reject(new Error("Authentication required"));
    }
    
    // Validate fields before sending
    if (!updatedItem.name || !updatedItem.count || !updatedItem.category || !updatedItem.unit_price) {
      return Promise.reject(new Error("All fields are required"));
    }
    
    return fetch("http://127.0.0.1:5000/api/inventory/update", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ 
        id: updatedItem.id,
        name: updatedItem.name,
        quantity: parseInt(updatedItem.count),
        unit_price: parseFloat(updatedItem.unit_price),
        category: updatedItem.category
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.error || "Failed to update item");
          });
        }
        return response.json();
      })
      .then(() => {
        // Refresh inventory data to ensure consistency
        return fetchInventory();
      });
  };

  const removeInventoryItem = (itemId) => {
    const token = localStorage.getItem("token");
    if (!token) {
      return Promise.reject(new Error("Authentication required"));
    }
    
    return fetch("http://127.0.0.1:5000/api/inventory/remove", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ 
        inventoryId: itemId
      }),
    })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.error || "Failed to delete item");
          });
        }
        return response.json();
      })
      .then(() => {
        // Refresh inventory data to ensure consistency
        return fetchInventory();
      });
  };

  return {
    inventory_list,
    filteredInventory,
    searchTerm,
    setSearchTerm,
    error,
    isLoading,
    getCategoryImage,
    addInventoryItem,
    updateInventoryItem,
    removeInventoryItem,
    refreshInventory: fetchInventory
  };
};

export default useInventoryData;