import algorithms as algs
import center as c
import numpy as np
import time

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

pnum = 10
alg = algs.Algorithm()
for i in range(pnum):
    party = randomParty(np.random.randint(2,7))
    start_time = time.time()
    try:
        bfs = alg.bfsSearch(party)
    except:
        bfs = None
    bfs_elapsed_time = time.time() - start_time

    print "Time BFS took", bfs_elapsed_time
    if bfs != None:
        print "Outputted sadness divided by size of party + 1", bfs[1]/(len(party.users)+1)
    else:
        print "error"
