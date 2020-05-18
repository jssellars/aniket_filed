class Enumeration:
    def __init__(self, id=None, name=None, displayName=None):
        self.id = id
        self.name = name
        self.displayName = displayName

    def ToString(self):
        return self.name
