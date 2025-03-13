class Task:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }