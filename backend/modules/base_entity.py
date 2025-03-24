from typing import ClassVar

class BaseEntity:
    current_id: ClassVar[int] = 0
    
    @classmethod
    def generate_id(cls) -> int:
        cls.current_id += 1
        return cls.current_id
    
    def __init__(self) -> None:
        self._id = self.__class__.generate_id()
    
    @property
    def id(self) -> int:
        return self._id
