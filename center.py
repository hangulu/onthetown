import config
import math as m
import requests
import urllib, json

class User:

    def __init__(self, lat, lon):
        self.location = lat, lon

class Party:
    def __init__(self, users = []):
        self.users = users
        self.center = None
        self.places = []

    def __str__(self):
        if len(self.users) == 0:
            return "The party is empty"

    def findCenter(self):
        x = 0
        y = 0

        for user in self.users:
            x += user.location[0]/len(self.users)
            print x
            y += user.location[1]/len(self.users)
            print y

        self.center = (x, y)

    def addToParty(self, user):
        self.users.append(user)

    def searchLocation(self, type="", radius=5000):
        APIKEY = config.api_key
        parameters = {"location": str(self.center[0])+","+str(self.center[1]),"radius":radius, "type":type,"key":APIKEY}

        response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=parameters)
        data = response.json()

        for place in data["results"]:
            name = str(place["name"]) if "name" in place else None
            price = place["price_level"] if "price_level" in place else None
            rating = place["rating"] if "rating" in place else None
            location = place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]
            address = str(place["vicinity"]) if "vicinity" in place else None
            types = [str(type) for type in place["types"]] if "types" in place else None

            self.places.append({"name": name, # each place is its own dict for easy access to what you're looking for
                                "price": price,
                                "rating": rating,
                                "location": location,
                                "address": address,
                                "types": types})


# tests dont work together for some reason the second keeps data from the first but we can fix that later!
print "PARTY 1\nPARTY 1\nPARTY 1\nPARTY 1\n"
# party = Party()
# hakeem = User(42.3736, -71.1097)
# louie = User(40.7128, -74.0060)
# amadou = User(41.9645, -73.4408)
# party.addToParty(hakeem)
# party.addToParty(louie)
# party.addToParty(amadou)
#
# print party.findCenter()

print "PARTY 2\nPARTY 2\nPARTY 2\nPARTY 2\n"

party1 = Party()
hakeem1 = User(40.807835,-73.963957)
louie1 = User(40.709013,-74.013692)
amadou1 = User(40.773585,-73.936027)
party1.addToParty(hakeem1)
party1.addToParty(louie1)
party1.addToParty(amadou1)
party1.findCenter()
print party1.center
party1.searchLocation("bar")
print party1.places
