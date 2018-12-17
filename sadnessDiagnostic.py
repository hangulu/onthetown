import center as c
import math as m
import numpy as np


# Return additional travel percentage to chosen location relative to assigned c location
def getDist(user, party, place):
    return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))

# /m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)
error_count = 0
def sadnessDiagnostic(party):
    places = party.filteredPlaces
    if len(places) == 0:
        print "SHIIIIIT SON"
        global error_count
        error_count += 1
        return [0]*4
    users = party.users
    weights = {"dist" : 1., "rating" : 1., "price" : 1., "types" : 1.}
    sadness = [0]*4
    num = len(party.users)*len(places)

    for place in places:
        for i in range(len(users)):
            dist = getDist(users[i], party, place)
            if dist > 0:
                sadness[0] += (dist * weights["dist"])/0.0156106747366
                #* (1/0.0940694970359)
                 # * (1/0.0679126470653)
                 # (0.09179504072728065)


            rating = users[i].ratingPref - place["rating"]
            if rating > 0:
                sadness[1] += (rating * weights["rating"])/0.130747631926
                # * (1/0.186832348864)
                 # * (1/0.109921338687)
                 # (0.163095087303309)

            price = place["price"] - users[i].pricePref
            if price > 0:
                sadness[2] += (price * weights["price"])/0.170200961101
                # * (1/0.313995)
                 # * (1/0.693561666667)
                 # (0.3144504166681268)

            type = 0
            for event in users[i].eventPref:
                if event not in place["types"]:
                    type += 1
            if type == len(users[i].eventPref):
                type = 1.
            else:
                type = 0
            sadness[3] += type * weights["types"]/0.319765608129
            #* (1/0.504125555556)
             # * (1/0.425713472222)
             # (0.5319052430572467)

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
pnum = 10
for i in range(pnum):
    party = randomParty(np.random.randint(2,7))
    print len(party.filteredPlaces)
    sadness = sadnessDiagnostic(party)
    print "Party", i, "User Count", len(party.users)
    print "Party", i, "Distance", sadness[0], "Rating", sadness[1], "Price", sadness[2], "Type", sadness[3]
    total_sadness[0] += sadness[0]
    total_sadness[1] += sadness[1]
    total_sadness[2] += sadness[2]
    total_sadness[3] += sadness[3]
print "Total User Count", count
print "Total Error Count", error_count
print "Total", "Distance", total_sadness[0]/(pnum - error_count), "Rating", total_sadness[1]/(pnum - error_count), "Price", total_sadness[2]/(pnum - error_count), "Type", total_sadness[3]/(pnum - error_count)

# Total -- 50 -- Distance 0.0161592456178 Rating 0.127213537013 Price 0.169797451502 Type 0.457565392461
# Total -- 20 -- Distance 0.0188080062544 Rating 0.138408560697 Price 0.173751310925 Type 0.279295517729
# Total -- 500 -- Distance 0.0156106747366 Rating 0.130747631926 Price 0.170200961101 Type 0.319765608129
    # Error count 3

# Normalized testa
# Total -- 10 -- Distance 1.09756140318 Rating 1.16887866081 Price 0.968105008073 Type 0.870719462553
# Total -- 10 -- Distance 0.841315174016 Rating 1.69979152832 Price 0.656875960548 Type 0.958094400112
# Total -- 10 -- Distance 1.16633972916 Rating 1.01652446126 Price 0.551033347781 Type 0.929086713049
# Total -- 10 -- Distance 1.00351374524 Rating 1.04211459919 Price 0.879781636077 Type 1.09478562689
# Total -- 10 -- Distance 0.785663224253 Rating 1.59192226143 Price 0.879333036906 Type 1.0029138118
# Total -- 10 -- Distance 0.993086300076 Rating 0.811261024419 Price 1.05950515338 Type 0.621396677955
