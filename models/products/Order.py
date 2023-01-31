class Order:
    def __init__(self, id, item):
        self.id = id
        self.item = item

    def get_id(self):
        return self.id

    def get_item(self):
        return self.item

    def set_item(self, item):
        self.item = item
