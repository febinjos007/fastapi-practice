class StoryException(Exception):
    def __int__(self, name: str):
        self.name = name
