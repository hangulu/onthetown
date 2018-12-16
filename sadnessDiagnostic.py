import center
import math as m
import numpy as np

# Return additional travel percentage to chosen location relative to assigned center location
def getDist(user, party, place):
    return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))/m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)

def sadnessDiagnostic(place, party):
    weights = {"types" : 1, "price" : 1, "rating" : 1, "dist" : 1}
    sadness = {"types" : 0, "price" : 0, "rating" : 0, "dist" : 0}

    for user in party.users:
        dist = getDist(user, party, place)
        if dist > 0:
            sadness["dist"] += dist * weights["dist"]

        rating = user.ratingPref - place["rating"]
        if rating > 0:
            sadness["rating"] += rating * weights["rating"]

        price = float(place["price"] - user.pricePref)
        if price > 0:
            sadness["price"] += price * weights["price"]

        type = 0
        for event in user.eventPref:
            if event not in place["types"]:
                type += 1.
        if type == len(user.eventPref):
            type = 1.
        else:
            type = type/(2*len(user.eventPref))
        sadness["types"] += type * weights["types"]

    return sadness

final_dist = 0
final_rating = 0
final_price = 0
final_types = 0
num = 6*len(center.party1.filteredPlaces)
for place in center.party1.filteredPlaces:
    sadness = sadnessDiagnostic(place, center.party1)
    final_dist += sadness["dist"]
    final_rating += sadness["rating"]
    final_price += sadness["price"]
    final_types += sadness["types"]

print final_dist/num, final_rating/num, final_price/num, final_types/num
