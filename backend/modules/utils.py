from typing import List, TypeVar, Callable, Any

T = TypeVar('T')  # Generic type for container elements

def get_object_index_in_container(container: List[T], object: T, get_identifier: Callable[[T], Any]) -> int:
    """Find object index using a custom identifier function"""
    for i, item in enumerate(container):
        if get_identifier(object) == get_identifier(item):
            return i
    return -1
    
def get_object_index_in_container_id(container: List[T], id: int, get_id: Callable[[T], int]) -> int:
    """Find object index by its ID using a custom ID getter function"""
    for i, item in enumerate(container):
        if id == get_id(item):
            return i
    return -1

# Additional utility functions to enhance the module

def find_objects_by_attribute(container: List[T], 
                             attr_name: str, 
                             attr_value: Any) -> List[T]:
    """Find all objects in a container with matching attribute value"""
    return [item for item in container if hasattr(item, attr_name) and 
            getattr(item, attr_name) == attr_value]

def safe_get_by_id(container: List[T], 
                  id_value: int,
                  id_getter: Callable[[T], int]) -> T:
    """Safely get an object by ID or return None if not found"""
    for item in container:
        if id_getter(item) == id_value:
            return item
    return None