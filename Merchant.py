class Merchant:
    def __init__(self, id, name, distance):
        self.id = id
        self.name = name
        self.distance = distance

    # Serialize merchant to dictionary to write to JSON
    def serialize(self):
        return {
            "id": self.id
            , "name": self.name 
            , "distance": self.distance
        }

    # Convert a dictionary object load from json to an offer object
    @classmethod
    def convertFromDict(cls, dict):
        id = int(dict["id"])
        name = dict["name"]
        distance = float(dict["distance"])
        return cls(id, name, distance)

