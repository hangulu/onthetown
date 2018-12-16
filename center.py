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
    A user of the program
    """
    def __init__(self, name, lat, lon, pricePref, ratingPref, eventPref):
        """
        Each user is initialized with their location and their preferences
        based on event, price, and ratings.
        """
        self.name = name
        self.location = lat, lon
        self.organizer = False
        self.pricePref = pricePref
        self.ratingPref = ratingPref
        self.eventPref = eventPref

class Party:
    """
    This holds the data about a given group of users including their center,
    filtered list, etc, used to find the best events.
    """
    def __init__(self):
        """
        Party is initialized with the list of users at first if it is given,
        otherwise it is null.
        """
        self.users = []
        self.center = None
        self.places = []

    def __str__(self):
        """
        Outputs to improve the interactivity with the user, descriptors based
        on the party size.
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
            y += user.location[1]/len(self.users)# latitudes

        self.center = (x, y)
        print "The center of the users is", self.center

    def addToParty(self, user):
        """
        The party is a list of users, so we append the user to the list
        """
        if not self.users:
            user.organizer = True # first person in the party is the organizer
            print user.name + " is the organizer of the party"
        self.users.append(user)
        print user.name + " has been added to the party"
        self.findCenter() # as we add users we update the center.

    def searchLocation(self, type="", radius=5000):
        """
        This is the function that takes the center location and searched for all
        the possible events in the radius.

        The type input is any one of the types from googleTypes.py. The radius
        is dependent on how far we want to search out.
        """
        APIKEY = config.api_key # created our own config files to protect api_key
        # seting the parameters and making calls to the google places api
        parameters = {"location": str(self.center[0])+","+str(self.center[1]),"radius":radius, "type":type,"key":APIKEY}
        response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=parameters)
        data = response.json()

        try:
            # the initial limit of each call is 20, but if a result has a next
            # page token we can get up to 60 results, but new calls have to be
            # made, if there is no next page token, then it will just pass.
            next_page_token = data["next_page_token"]
            while next_page_token:
                parameters2 = {"pagetoken" : next_page_token, "key" : APIKEY}
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
        Iterates through the response data recieved from API calls and adds the
        places in our format to the list of all the places. We record the name,
        price, rating, longitude and latitude, address, and types associated with
        the event for each of the results.
        """
        for place in data["results"]:
            name = place["name"] if "name" in place else None
            price = place["price_level"] if "price_level" in place else 2
            rating = place["rating"] if "rating" in place else 3
            location = place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"]
            address = place["vicinity"] if "vicinity" in place else None
            types = [str(type) for type in place["types"]] if "types" in place else None

            # each place is its own dict for easy access to what you're looking for
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
        Iterates through all of the google types and searches the location fpr
        each, to give all possible locations in the area.
        """
        for type in googleTypes.googleTypes:
            self.searchLocation(type, radius)

    def filterList(self):
        """
        Based on the inputs of each user for the preferences, this function looks
        to see if an event in the total places list satisfies at least one persons
        preferences and adds it to the list of filtered.

        This allows us to remove unnecesary seatches through events that would
        provide no utility to any user.
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
        The updateAll function resets the places and repopulates it.

        It is meant to be used upon adding a new person to the party where the
        center changes.
        """
        self.places = []
        rad = 0
        for i in range(10):
            rad += 500
            self.updatePlaces(rad)
        self.filterList()
        self.assignSadness()

    def similarity(self, event, places):
        """
        This is a funtion that tests out the similarity of a given event to the
        rest of the list and filters the events that are too similar, outputing
        a list of events that are different the a selected event.

        This is going to be used in the search tree, i.e. if a variable is chosen
        we want to have a domain of dissimilar options for the next choice.
        """
        newList = []
        for place in places:
            similarity = 0
            if place["price"] == event["price"]:
                similarity += 1.
            for type1 in event["types"]:
                for type2 in place["types"]:
                    if type1 == type2:
                        similarity += 1.0/float(len(place["types"]))
            if similarity <= 1.67:
                newList.append(place)
        return newList

    def getDist(self, user, party, place):
        """
        Calculates the % distance fthat a user must travel to the location, vs.
        the geographical center which is the most fair.

        If this is greater than 0, the user must travel more to go to go to the
        venue than they would travel to go to the center.
        """
        return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))/m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)

    def sadnessFunction(self, place, party):
        """
        Sadness function evaluates the how each person in the party is affected
        by a specific event's type, price, rating, and distance, based on their preferences.

        The output is a list of the "sadness" rating for each user in the party.
        """
        # weights here are used to place emphasis on certain preferences more than others
        weights = {"type" : 1., "price" : 1., "rating" : 1., "dist" : 1.}
        sadness = [0] * len(party.users)

        for i in range(len(party.users)):
            dist = self.getDist(party.users[i], party, place)
            if dist > 0:
                sadness[i] += dist * weights["dist"]

            rating = party.users[i].ratingPref - place["rating"]
            if rating > 0:
                sadness[i] += rating * weights["rating"]

            price = float(place["price"] - party.users[i].pricePref)
            if price > 0:
                sadness[i] += price * weights["price"]

            type = 0
            for event in party.users[i].eventPref:
                if event not in place["types"]:
                    type += 1
            if type == len(party.users[i].eventPref):
                type = 1
            else:
                type = type/(2*len(party.users[i].eventPref))
            sadness[i] += type

        return sadness

    def assignSadness(self):
        """
        Assign a sadness to each event in the form of a list, where each person's
        sadness is at an index of the list.

        This makes it so that when we are searching through the tree, we do not
        havee to evaluate at each step, the "values" will be there.
        """
        for place in self.filteredPlaces:
            sadness = self.sadnessFunction(place, self)
            place["sadness"] = sadness


# tests dont work together for some reason the second keeps data from the first but we can fix that later!
# print "PARTY 1\nPARTY 1\nPARTY 1\nPARTY 1\n"
# party = Party()
# hakeem = User("Hakeem", 40.807835, -73.963957, 4, 5, ["bar", "restaurant"])
# louie = User("Louie", 40.709013, -74.013692, 3, 4, ["restaurant", "movie"])
# amadou = User("Amadou", 40.773585, -73.936027, 2, 3, ["night_club", "bar", "restaurant"])
# party.addToParty(hakeem)
# party.addToParty(louie)
# party.addToParty(amadou)
# party.updateAll()
# print len(party.places)
# print "filtered", len(party.filteredPlaces)


print "PARTY 2\nPARTY 2\nPARTY 2\nPARTY 2\n"
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
print "similarity function tests \n"
list = party1.filteredPlaces
randEvent = np.random.choice(list)
newList = party1.similarity(randEvent, party1.filteredPlaces)
for i in range(7):
    print len(newList)
    list = newList
    randEvent = np.random.choice(list)
    newList = party1.similarity(randEvent, list)

# test for sadness function
print "random sadness function tests \n"
print party1.sadnessFunction(np.random.choice(party1.filteredPlaces), party1)
