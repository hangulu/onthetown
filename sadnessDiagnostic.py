"""
This module implements the functions to run diagnostics on the sadness function
and empirically determine weights.
"""

import center as c
import math as m
import numpy as np

def getDist(user, party, place):
    """
    Compare the distance that a user must travel to the location to the
    distance that a user must travel the geographical center. If this is
    greater than 0, the user must travel more to go to the venue than they
    would travel to go to the center.
    user (User object): A user.
    party (Party object): A party.
    place (dict): A potential place.

    return: Float of the difference between distances to the venue and
    center.
    """
    dist_to_venue = m.sqrt((user.location[0] - place["location"][0]) ** 2 + (user.location[1] - place["location"][1]) ** 2)
    dist_to_center = m.sqrt((user.location[0] - party.center[0]) ** 2 + (user.location[1] - party.center[1]) ** 2)
    return dist_to_venue - dist_to_center


# Keep track of the sadness stemming from each of the 4 contributing factors
error_count = 0
def sadnessDiagnostic(party):
    """
    Run diagnostics on the sadnessFunction.
    party (Party object): A given party.

    return: a list of sadness scores.
    """
    # Get initital list of venues
    places = party.filteredPlaces

    # Exit when list is empty
    if len(places) == 0:
        global error_count
        error_count += 1
        return [0] * 4

    # Get list of users
    users = party.users
    # Option to view weighted output
        # weights = {"dist" : 1./0.0156106747366, "rating" : 1./0.130747631926, "price" : 1./0.170200961101, "types" : 1./0.319765608129}
    # Initialize list of sadness
    sadness = [0] * 4

    # Iterate through all the places
    for place in places:
        for i in range(len(users)):
            # Get distance-attributed sadness
            dist = getDist(users[i], party, place)
            if dist > 0:
                sadness[0] += dist

            # Get rating-attributed sadness
            rating = users[i].ratingPref - place["rating"]
            if rating > 0:
                sadness[1] += rating

            # Get price-attributed sadness
            price = place["price"] - users[i].pricePref
            if price > 0:
                sadness[2] += price

            # Get type-attributed sadness
            type = 0
            for event in users[i].eventPref:
                if event not in place["types"]:
                    type += 1
            if type == len(users[i].eventPref):
                type = 1.
            else:
                type = 0
            sadness[3] += type

    # Get sadness per factor per user
    num = len(party.users)*len(places)
    sadness[0] = sadness[0] / num
    sadness[1] = sadness[1] / num
    sadness[2] = sadness[2] / num
    sadness[3] = sadness[3] / num

    return sadness

# Create party of specified length with random user preferences
def randomParty(num):
    """
    Generate a random party object of a certain size.
    num (int): The size of the party.
    """
    # List of various coordinates in New York City
    # Possible coordinates, in New York City.
    coordlist = [(40.503780, -74.257985),
                 (40.910901, -73.908623),
                 (40.742613, -73.709127),
                 (40.597664, -73.763148),
                 (40.612447, -74.090254),
                 (40.770627, -73.958057),
                 (40.754135, -73.872459),
                 (40.718946, -73.808422),
                 (40.665516, -73.868019),
                 (40.653366, -73.970087),
                 (40.661236, -73.742950),
                 (40.560440, -73.920751)]

    # List of potential types
    typelist = ["bar", "restaurant", "night_club", "movie_theater", "cafe"]
    # Initialize party
    party = c.Party()
    # Initialize list to hold users coordinates
    coords = []
    # For each user:
    for i in range(num):
        # Get unique coordinates
        coord = coordlist[np.random.randint(0,len(coordlist))]
        while coord in coords:
            coord = coordlist[np.random.randint(0,len(coordlist))]
        coords.append(coord)
        # Get unique username
        username = "User" + str(i)
        # Get random rating, uniform continuous [2,5]
        rating = 2 + 3*np.random.random_sample()
        # Get random price, uniform discrete [1,4]
        price = np.random.randint(1,5)
        # Get random type preferences of size 1-3
        types = np.random.choice(typelist,size = np.random.randint(1,4),replace = False)
        # Create user
        user = c.User(username, coord[0], coord[1], price, rating, types)
        # Add user to party
        party.addToParty(user)

    party.updateAll()
    return party

# Get average sadness attributed to factors over specified number of random parties
total_sadness = [0] * 4
pnum = 10
# Run simulations
for i in range(pnum):
    party = randomParty(np.random.randint(2,7))
    sadness = sadnessDiagnostic(party)
    print "Party", i, "User Count", len(party.users)
    print "Party", i, "Distance", sadness[0], "Rating", sadness[1], "Price", sadness[2], "Type", sadness[3]
    total_sadness[0] += sadness[0]
    total_sadness[1] += sadness[1]
    total_sadness[2] += sadness[2]
    total_sadness[3] += sadness[3]
print "Total Error Count", error_count
# Return average over parties, but adjust for error_count
print "Total", "Distance", total_sadness[0] / (pnum - error_count), "Rating", total_sadness[1] / (pnum - error_count), "Price", total_sadness[2] / (pnum - error_count), "Type", total_sadness[3] / (pnum - error_count)
