from Merchant import Merchant
from datetime import datetime

class Offer:
    def __init__(self, id, title, description, category, merchants, valid_to):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.merchants = merchants
        self.valid_to = valid_to

    # Serialize merchant to dictionary to write to JSON
    def serialize(self):
        return {
            "id": self.id
            , "title": self.title 
            , "description": self.description
            , "category": self.category 
            , "merchants": [item.serialize() for item in self.merchants]
            , "valid_to": self.valid_to.strftime('%Y-%m-%d')
        }

    # Convert a dictionary object load from json to an offer object
    @classmethod
    def convertFromDict(cls, dict):
        merchantsArr = []
        for merchant in dict["merchants"]:
            merchantsArr.append(Merchant.convertFromDict(merchant))
        id = int(dict["id"])
        title = dict["title"]
        description = dict["description"]
        category = int(dict["category"])
        valid_to = datetime.strptime(dict["valid_to"], '%Y-%m-%d').date()
        return cls(id, title, description, category, merchantsArr, valid_to)