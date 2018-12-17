import center
import numpy as np

def similarity(event, places):
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

# test
list = center.party1.filteredPlaces
randEvent = np.random.choice(list)
newList = similarity(randEvent, center.party1.filteredPlaces)
for i in range(10):
    print len(newList)
    list = newList
    randEvent = np.random.choice(list)
    newList = similarity(randEvent, list)
