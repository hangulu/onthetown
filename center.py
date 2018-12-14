import math as m
import urllib, json
import requests

class User:

    def __init__(self, lat, lon):
        self.location = lat, lon

class Party:
    def __init__(self, users = []):
        self.users = users
        self.center = None

    def findCenter(self):
        x = 0
        y = 0

        for user in self.users:
            x += user.location[0]/len(self.users)
            y += user.location[1]/len(self.users)

        self.center = (x, y)
        return x, y

    def addToParty(self, user):
        self.users.append(user)

    def searchLocation(self):
        APIKEY = "AIzaSyBRN11_2sbGIcL9IXZ4ZxAhOVcw7EGPf1k"
        location = "{lat},{lng}".format(lat = self.center[0], lng = self.center[1])
        type = "bar"
        radius = 5000
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={APIKEY}".format(location = location, radius = radius, type = type,APIKEY = APIKEY)

        response = requests.get(url)
        res = json.loads(response.text)
        for result in res["results"]:
          info = " ".join(map(str,[result["name"],result["geometry"]["location"]["lat"],result["geometry"]["location"]["lng"],result.get("rating",0),result["place_id"]]))
          print info

# tests
party = Party()
hakeem = User(42.3736, -71.1097)
louie = User(40.7128, -74.0060)
amadou = User(41.9645, -73.4408)
party.addToParty(hakeem)
party.addToParty(louie)
party.addToParty(amadou)

print party.findCenter()
print party.searchLocation()
