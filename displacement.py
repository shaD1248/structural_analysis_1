from collection_item import CollectionItem

class Displacement(CollectionItem):
    def __init__(self, object_type: str, object_id: int, local_displacement_id: int, supported: bool):
        self.object_type = object_type
        self.object_id = object_id
        self.local_displacement_id = local_displacement_id
        self.supported = supported

    def __str__(self):
        return 'displacement ' + str(self.local_displacement_id) + ' of ' + self.object_type + ' ' + str(self.object_id)
