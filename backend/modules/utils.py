from typing import List, TypeVar, Callable, Any

T = TypeVar('T')  

def get_object_index_in_container(container: List[T], object: T, get_identifier: Callable[[T], Any]) -> int:
    for i, item in enumerate(container):
        if get_identifier(object) == get_identifier(item):
            return i
    return -1
    
def get_object_index_in_container_id(container: List[T], id: int, get_id: Callable[[T], int]) -> int:
    for i, item in enumerate(container):
        if id == get_id(item):
            return i
    return -1



def find_objects_by_attribute(container: List[T], 
                             attr_name: str, 
                             attr_value: Any) -> List[T]:
    return [item for item in container if hasattr(item, attr_name) and 
            getattr(item, attr_name) == attr_value]

def safe_get_by_id(container: List[T], 
                  id_value: int,
                  id_getter: Callable[[T], int]) -> T:
    for item in container:
        if id_getter(item) == id_value:
            return item
    return None
