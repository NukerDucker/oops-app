from .base_entity import BaseEntity
class Task(BaseEntity):
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
