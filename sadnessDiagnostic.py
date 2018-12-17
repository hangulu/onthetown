import center as c
import math as m
import numpy as np


# Return additional travel percentage to chosen location relative to assigned c location
def getDist(user, party, place):
    return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))

# /m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)

def sadnessDiagnostic(party):
    places = c.party1.filteredPlaces
    users = party.users
    weights = {"dist" : 1., "rating" : 1., "price" : 1., "types" : 1.}
    sadness = [0]*4
    num = len(party.users)*len(places)

    for place in places:
        for i in range(len(users)):
            dist = getDist(users[i], party, place)
            if dist > 0:
                sadness[0] += dist * weights["dist"] * (1/0.0940694970359)
                 # * (1/0.0679126470653)

            rating = users[i].ratingPref - place["rating"]
            if rating > 0:
                sadness[1] += rating * weights["rating"] * (1/0.186832348864)
                 # * (1/0.109921338687)

            price = place["price"] - users[i].pricePref
            if price > 0:
                sadness[2] += price * weights["price"] * (1/0.313995)
                 # * (1/0.693561666667)

            type = 0.
            for event in users[i].eventPref:
                if event not in place["types"]:
                    type += 1.
            if type == len(users[i].eventPref):
                type = 1.
            else:
                type = type/(2*len(users[i].eventPref))
            sadness[3] += type * weights["types"] * (1/0.504125555556)
             # * (1/0.425713472222)

    sadness[0] = sadness[0]/num
    sadness[1] = sadness[1]/num
    sadness[2] = sadness[2]/num
    sadness[3] = sadness[3]/num

    return sadness
count = 0
def randomParty(num):
    coordlist = [(40.503780, -74.257985), (40.910901, -73.908623), (40.742613, -73.709127),
                (40.597664, -73.763148), (40.612447, -74.090254), (40.770627, -73.958057),
                (40.754135, -73.872459), (40.718946, -73.808422), (40.665516, -73.868019),
                (40.653366, -73.970087), (40.661236, -73.742950), (40.560440, -73.920751)]
    typelist = ["bar", "restaurant", "night_club", "movie_theater", "cafe"]
    party = c.Party()
    coords = []
    for i in range(num):
        coord = coordlist[np.random.randint(0,len(coordlist))]
        while coord in coords:
            coord = coordlist[np.random.randint(0,len(coordlist))]
        coords.append(coord)
    for i in range(num):
        global count
        count += 1
        username = "User" + str(i)
        coord = coords[np.random.randint(0,len(coords))]
        rating = 2 + 3*np.random.random_sample()
        price = np.random.randint(1,5)
        types = np.random.choice(typelist,size = np.random.randint(1,4),replace = False)
        # for i in range(np.random.randint(1,4)):
        #     types.append(np.random.choice(typelist))
        user = c.User(username, coord[0], coord[1], price, rating, types)
        party.addToParty(user)
    party.updateAll()
    return party

total_sadness = [0]*4
pnum = 400
for i in range(pnum):
    party = randomParty(np.random.randint(2,7))
    sadness = sadnessDiagnostic(party)
    print "Party", i, "User Count", len(party.users)
    print "Party", i, "Distance", sadness[0], "Rating", sadness[1], "Price", sadness[2], "Type", sadness[3]
    total_sadness[0] += sadness[0]
    total_sadness[1] += sadness[1]
    total_sadness[2] += sadness[2]
    total_sadness[3] += sadness[3]
print "Total User Count", count
print "Total", "Distance", total_sadness[0]/pnum, "Rating", total_sadness[1]/pnum, "Price", total_sadness[2]/pnum, "Type", total_sadness[3]/pnum
