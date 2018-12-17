"""
This module implements the core classes of the social planning search problem:
* User: a user of the program
* Party: a group of users planning to go out together.

It also implements the similarity function, which generates successors to a
given plan by striving for a diversity of options.
"""

import config # make a config.py with an api_key from google places
import googleTypes # a list of all the searcheable google types
import math as m
import numpy as np
import requests
import requests_cache
import urllib, json

# cache searches for tests to save api calls and improve performance during tests
requests_cache.install_cache('googleAPICache')

class User:
    """
    A user of the program.
    """
    def __init__(self, name, lat, lon, pricePref, ratingPref, eventPref):
        """
        Each user is initialized with their location and their preferences
        based on event, price, and ratings.
        name (string): The user's name.
        location (tuple): A tuple of latitude and longitude that encodes the
        user's location.
        organizer (boolean): Whether or not the user is the organizer.
        pricePref (int): The user's price preference as an integer between 0 and 4, inclusive.
        ratingPref (float): The user's preference for a place's rating as an float between 1.0 and 5.0, inclusive.
        eventPref (string): The user's preference for a type of event. All options are in googleTypes.py.
        """
        self.name = name
        self.location = lat, lon
        self.organizer = False
        self.pricePref = pricePref
        self.ratingPref = ratingPref
        self.eventPref = eventPref

class Party:
<<<<<<< HEAD
    def __init__(self):
=======
    """
    This holds the data about a given group of users including their center,
    filtered list, etc, used to find the best events.
    """
    def __init__(self):
        """
        Party is initialized with the list of users at first, if given,
        otherwise an empty list is used.
        users (list): List of User objects.
        center (tuple): Tuple of the center of all users' locations.
        places (list): A list of potential places.
        """
>>>>>>> dd3f0b7f9d7b2b54336addb793f5bda3609a2c0a
        self.users = []
        self.center = None
        self.places = []

    def __str__(self):
        """
        Outputs to improve the interactivity with the user, with descriptors
        based on the party size.
        """
        output = ""
        if len(self.users) == 0:
            output = "The party is empty."
        elif len(self.users) == 1:
            output = "Only " + self.users[0].name + " is in the party."
        else:
            for i in range(len(self.users)-1):
                user = self.users[i]
                output += user.name + ", "
            output += "and " + self.users[-1].name + " are in the party."
        return output

    def findCenter(self):
        """
        The true center of geographical longitudes and latitudes. It averages
        the location of each user, then assigns that to the center of the party.
        """
        x = 0
        y = 0

        for user in self.users:
            x += user.location[0]/len(self.users) # longitudes
            y += user.location[1]/len(self.users) # latitudes

        self.center = (x, y)
<<<<<<< HEAD
        # print "The center of the users is", self.center
=======
        print "The center of the users is: ", self.center
>>>>>>> dd3f0b7f9d7b2b54336addb793f5bda3609a2c0a

    def addToParty(self, user):
        """
        Add a user to the party.
        user (User): A User object.
        """
        # The first person in the party is the organizer
        if not self.users:
            user.organizer = True
            # print user.name + " is the organizer of the party"
        self.users.append(user)
<<<<<<< HEAD
        # print user.name + " has been added to the party"
=======
        print user.name + " has been added to the party"
        # Update the center
>>>>>>> dd3f0b7f9d7b2b54336addb793f5bda3609a2c0a
        self.findCenter()

    def searchLocation(self, type="", radius=5000):
        """
        Take the center location and search for all possible events within a
        given radius.
        type (string): A type from googleTypes.py.
        radius (int): How far to search from the center.
        """
        # Use config files to secure API keys
        APIKEY = config.api_key

        # Set the parameters and make calls to the Google Places API
        parameters = {"location": str(self.center[0]) + "," + str(self.center[1]), "radius": radius, "type": type, "key": APIKEY}
        response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=parameters)
        data = response.json()

        try:
            # The initial limit of each call is 20, but if a result has a next
            # page token we can get up to 60 results. New calls have to be
            # made, and if there is no next page token, continue.
            next_page_token = data["next_page_token"]
            while next_page_token:
                parameters2 = {"pagetoken": next_page_token, "key": APIKEY}
                response2 = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=parameters2)
                data2 = response2.json()
                try:
                    next_page_token = data2["next_page_token"]
                except:
                    next_page_token = None

                self.addPlaces(data2)
        except:
            pass

        self.addPlaces(data)

    def addPlaces(self, data):
        """
        Iterate through the response data recieved from API calls and add the
        formatted places to the list of all the places. Record the name,
        price, rating, longitude and latitude, address, and types associated
        with the event for each of the results.
        data (dict): The dictionary of Google Places API response data.
        """
        for place in data["results"]:
            name = place["name"] if "name" in place else None
            price = place["price_level"] if "price_level" in place else 2
            rating = place["rating"] if "rating" in place else 3
            location = place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]
            address = place["vicinity"] if "vicinity" in place else None
            types = [str(type) for type in place["types"]] if "types" in place else None

            # Each place is its own dict for easy access to key attributes
            dict = {"name": name,
                    "price": price,
                    "rating": rating,
                    "location": location,
                    "address": address,
                    "types": types}

            if dict not in self.places:
                self.places.append(dict)

    def updatePlaces(self, radius = 5000):
        """
        Iterate through all of the Google types and searches the location for
        each to give all possible locations in the area.
        radius (int): How far to search from the center.
        """
        for type in googleTypes.googleTypes:
            self.searchLocation(type, radius)

    def filterList(self):
        """
        Check if events in the list of total places satisfy at least one user's
        preferences and add those events to a new list. This allows for the
        removal of unnecesary searches through events that would provide no
        utility to any user.
        """
        filteredList = []
        for user in self.users:
            for place in self.places:
                if place not in filteredList:
                    if place["price"] <= user.pricePref and place["rating"] >= user.ratingPref:
                        for pref in user.eventPref:
                            if pref in place["types"]:
                                filteredList.append(place)
        self.filteredPlaces = filteredList

    def updateAll(self):
        """
        Reset and repopulate the list of places. Used when adding a new person
        to the party.
        """
        self.places = []
        rad = 0
        # for i in range(10):
        #     rad += 500
        #     self.updatePlaces(rad)
        self.updatePlaces()
        self.filterList()
<<<<<<< HEAD

    def similarity(self, event, places):
        newList = []
        for place in places:
            similarity = 0
            if place["price"] == event["price"]:
                similarity += 1.
            for type1 in event["types"]:
                for type2 in place["types"]:
                    if type1 == type2:
                        similarity += 1.0/float(len(place["types"]))
            if similarity <= 1.7:
                newList.append(place)
        return newList

    def getDist(self, user, party, place):
        return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))/m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)

    # def sadnessFunction(self, place, party):
    #     weights = {"type" : 1, "price" : 1, "rating" : 1, "dist" : 1}
    #     sadness = []
    #     print place
    #     for user in party.users:
    #         sadness = 0
    #
    #         dist = self.getDist(user, party, place)
    #         if dist > 0:
    #             sadness[user.name] += dist * weights["dist"]
    #         print user.name, "dist = ", dist
    #
    #         rating = user.ratingPref - place["rating"]
    #         if rating > 0:
    #             sadness[user.name] += rating * weights["rating"]
    #         print user.name, "rating = ", rating
    #
    #         price = float(place["price"] - user.pricePref)/4
    #         if price > 0:
    #             sadness[user.name] += price * weights["price"]
    #         print user.name, "price = ", price
    #
    #         type = 0
    #         for event in user.eventPref:
    #             if event not in place["types"]:
    #                 type += 1
    #         if type == len(user.eventPref):
    #             type = 1
    #         else:
    #             type = type/(2*len(user.eventPref))
    #         sadness[user.name] += type
    #         print user.name, "type = ", type
    #
    #     print(sadness)

# tests dont work together for some reason the second keeps data from the first but we can fix that later!
# print "PARTY 1\nPARTY 1\nPARTY 1\nPARTY 1\n"
# party = Party()
# hakeem = User(42.3736, -71.1097)
# louie = User(40.7128, -74.0060)
# amadou = User(41.9645, -73.4408)
# party.addToParty(hakeem)
# party.addToParty(louie)
# party.addToParty(amadou)
#
# print party.findCenter()

# print "PARTY 2\nPARTY 2\nPARTY 2\nPARTY 2\n"
# test 2
party1 = Party()
hakeem1 = User("Hakeem", 40.807835, -73.963957, 4, 5, ["bar", "restaurant"])
louie1 = User("Louie", 40.709013, -74.013692, 3, 4, ["restaurant", "movie"])
amadou1 = User("Amadou", 40.773585, -73.936027, 2, 3, ["night_club", "bar", "restaurant"])
hakeem2 = User("Hakeem", 40.807835, -73.963957, 1, 3, ["bar", "movie"])
louie2 = User("Louie", 40.709013, -74.013692, 2, 4, ["restaurant", "bar"])
amadou2 = User("Amadou", 40.773585, -73.936027, 3, 5, ["night_club", "bar"])
party1.addToParty(hakeem1)
party1.addToParty(louie1)
party1.addToParty(amadou1)
party1.addToParty(hakeem2)
party1.addToParty(louie2)
party1.addToParty(amadou2)
party1.updateAll()

print len(party1.places)
print "filtered", len(party1.filteredPlaces)

count = 0
for place in party1.filteredPlaces:
    if place["price"] == None or place["rating"] == None:
        count += 1
print "count", count

# test for similarity fumction
# list = party1.filteredPlaces
# randEvent = np.random.choice(list)
# newList = party1.similarity(randEvent, party1.filteredPlaces)
# for i in range(10):
#     print len(newList)
#     list = newList
#     randEvent = np.random.choice(list)
#     newList = party1.similarity(randEvent, list)

# test for sadness function
# party1.sadnessFunction(np.random.choice(party1.filteredPlaces), party1)
=======
        self.assignSadness()

    def getDist(self, user, place):
        """
        Compare the distance that a user must travel to the location to the
        distance that a user must travel the geographical center. If this is
        greater than 0, the user must travel more to go to the venue than they
        would travel to go to the center.
        user (User object): A user.
        place (dict): A potential place.

        return: Float of the difference between distances to the venue and
        center.
        """
        dist_to_venue = m.sqrt((user.location[0] - place["location"][0]) ** 2 + (user.location[1] - place["location"][1]) ** 2)
        dist_to_center = m.sqrt((user.location[0] - self.center[0]) ** 2 + (user.location[1] - self.center[1]) ** 2)
        return dist_to_venue - dist_to_center

    def sadnessFunction(self, place):
        """
        Evaluate how each user in the party is affected by a specific event's
        type, price, rating, and distance, based on their preferences.
        place (dict): A potential place.

        return: List of the "sadness" incurred by a place for each user in the
        party.
        """
        # weights is used to establish priorities among preferences
        weights = {"type": 1., "price": 1., "rating": 1., "dist": 1.}

        # normalizers is used to normalize the sadness function to make its
        # output more intuitive
        normalizers = {"type": 0.504125555556, "price": 0.313995, "rating": 0.186832348864, "dist": 0.0940694970359}

        # Initialize the sadness list
        sadness = [0] * len(self.users)

        # Iterate through the list of users and calculate their sadness
        for i in range(len(self.users)):
            # Distance
            dist = self.getDist(self.users[i], place)
            if dist > 0:
                sadness[i] += dist * weights["dist"] / normalizers["dist"]

            # Rating
            rating = self.users[i].ratingPref - place["rating"]
            if rating > 0:
                sadness[i] += rating * weights["rating"] / normalizers["rating"]

            # Price
            price = float(place["price"] - self.users[i].pricePref)
            if price > 0:
                sadness[i] += price * weights["price"] / normalizers["price"]

            # Event type
            type = 0
            for event in self.users[i].eventPref:
                if event not in place["types"]:
                    type += 1
            if type == len(self.users[i].eventPref):
                type = 1
            else:
                type = type / (2 * len(self.users[i].eventPref))
            sadness[i] += type / normalizers["type"]

        return sadness

    def assignSadness(self):
        """
        Assign a sadness list to each event. This makes it such that
        evaluations of sadness are not unnecessarily repeated during search.
        """
        for place in self.filteredPlaces:
            sadness = self.sadnessFunction(place)
            place["sadness"] = sadness

def similarity(event, places):
    """
    Return a list of dissimilar events to the given event. This is the
    successor function used in the search tree: a node's successors are the
    list of dissimilar options for the next choice.
    event (dict): A potential place/event.
    places (list): All potential places.

    return: List of dissimilar places.
    """
    dissimilar = []
    for place in places:
        similarity = 0
        if place["price"] == event["price"]:
            similarity += 1.
        for type1 in event["types"]:
            for type2 in place["types"]:
                if type1 == type2:
                    similarity += 1.0 / float(len(place["types"]))
        # 1.67 is the empirically generated threshold for similarity
        # The empirical process behind this is described in the paper
        if similarity <= 1.67:
            dissimilar.append(place)
    return dissimilar
>>>>>>> dd3f0b7f9d7b2b54336addb793f5bda3609a2c0a
