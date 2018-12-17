import center
import math as m
import numpy as np

# Return additional travel percentage to chosen location relative to assigned center location
def getDist(user, party, place):
    return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))/m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)

def sadnessFunction(place, party):
    weights = {"type" : 1, "price" : 1, "rating" : 1, "dist" : 1}
    sadness = {}
    print place
    for user in party.users:
        sadness[user.name] = 0

        dist = getDist(user, party, place)
        if dist > 0:
            sadness[user.name] += dist * weights["dist"]
        print user.name, "dist = ", dist

        rating = user.ratingPref - place["rating"]
        if rating > 0:
            sadness[user.name] += rating * weights["rating"]
        print user.name, "rating = ", rating

        price = float(place["price"] - user.pricePref)/4
        if price > 0:
            sadness[user.name] += price * weights["price"]
        print user.name, "price = ", price

        type = 0
        for event in user.eventPref:
            if event not in place["types"]:
                type += 1
        if type == len(user.eventPref):
            type = 1
        else:
            type = type/(2*len(user.eventPref))
        sadness[user.name] += type
        print user.name, "type = ", type

    print(sadness)


sadnessFunction(np.random.choice(center.party1.filteredPlaces), center.party1)
