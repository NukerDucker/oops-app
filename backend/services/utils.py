def get_object_index_in_container(container: list[any], object: any, get_identifier) -> int:
    for i, thing in enumerate(container):
        if get_identifier(object) == get_identifier(thing):
            return i
    return -1
    
def get_object_index_in_container_id(container: list[any], id: int, get_id) -> int:
    for i, thing in enumerate(container):
        if id == get_id(thing):
            return i
    return -1