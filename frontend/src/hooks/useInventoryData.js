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
      "Cardiovascular": "antihypertensives.png"
    };
    
    // Return the mapped image or a default one
    return categoryImages[category] || "drug.svg";
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No authentication token found. Please login.");
      setIsLoading(false);
      return;
    }

    fetch("http://127.0.0.1:5000/api/supplies", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
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
          count: supply.quantity,
          category: supply.category,
          unit_price: supply.unit_price,
          total_value: supply.total_value,
          image: getCategoryImage(supply.category)
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
        if (!response.ok) throw new Error("Failed to add item");
        return response.json();
      })
      .then(data => {
        const addedItem = {
          id: data.id,
          name: newItem.name,
          count: parseInt(newItem.count),
          category: newItem.category,
          unit_price: parseFloat(newItem.unit_price),
          total_value: parseInt(newItem.count) * parseFloat(newItem.unit_price),
          image: getCategoryImage(newItem.category)
        };
        
        const newList = [...inventory_list, addedItem];
        setInventoryList(newList);
        setFilteredInventory(newList);
        return addedItem;
      });
  };

  const updateInventoryItem = (updatedItem) => {
    const token = localStorage.getItem("token");
    
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
          return response.text().then(text => {
            throw new Error(`Failed to update item: ${text}`);
          });
        }
        return response.json();
      })
      .then(() => {
        const updatedList = inventory_list.map(item => 
          item.id === updatedItem.id 
            ? {
                ...item,
                name: updatedItem.name,
                count: parseInt(updatedItem.count), 
                category: updatedItem.category,
                unit_price: parseFloat(updatedItem.unit_price),
                image: getCategoryImage(updatedItem.category)
              } 
            : item
        );
        
        setInventoryList(updatedList);
        setFilteredInventory(updatedList);
        return updatedItem;
      });
  };

  const removeInventoryItem = (itemId) => {
    const token = localStorage.getItem("token");
    
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
        if (!response.ok) throw new Error("Failed to delete item");
        return response.json();
      })
      .then(() => {
        const updatedList = inventory_list.filter(inv => inv.id !== itemId);
        setInventoryList(updatedList);
        setFilteredInventory(updatedList);
        return itemId;
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
    removeInventoryItem
  };
};

export default useInventoryData;