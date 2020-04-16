class Count:
    def __init__(self, name):
        self.name = name
        self.count = 1

    def __int__(self):
        return self.count

    def __str__(self):
        return str(self.name)

    def add_count(self):
        """Add an additional instance"""
        self.count += 1
