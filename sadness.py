import center

# def getDist(user, party, place):
#     return (m.sqrt((user.location[0]-place["location"][0])**2+(user.location[1]-place["location"][1])**2) - m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2))/m.sqrt((user.location[0]-party.center[0])**2+(user.location[1]-party.center[1])**2)
#
# def sadnessFunction(place, party):
#     weights = {"type" : 1, "price" : 1, "rating" : 1, "dist" : 1}
#     sadness = {}
#     print place
#     for user in party.users:
#         sadness[user.name] = 0
#
#         dist = getDist(user, party, place)
#         if dist > 0:
#             sadness[user.name] += dist * weights["dist"]
#
#         rating = user.ratingPref - place["rating"]
#         if rating > 0:
#             sadness[user.name] += rating * weights["rating"]
#
#         price = user.pricePref - place["price"]
#         if price > 0:
#             sadness[user.name] += price * weights["price"]
#
#         for event in user.eventPref:
#             if event not in place["type"]
#
#     print(sadness)
#
#
# sadnessFunction(party1.places[1], party1)
