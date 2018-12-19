"""
This module implements tests for the social planning search problem.
"""
from center import *
import algorithms as alg

# Test 1
print "PARTY 1\nPARTY 1\nPARTY 1\nPARTY 1\n"
party = Party()
hakeem = User("Hakeem", 40.807835, -73.963957, 4, 5, ["bar", "restaurant"])
louie = User("Louie", 40.709013, -74.013692, 3, 4, ["restaurant", "movie"])
amadou = User("Amadou", 40.773585, -73.936027, 2, 3, ["night_club", "bar", "restaurant"])
party.addToParty(hakeem)
party.addToParty(louie)
party.addToParty(amadou)
party.updateAll()
print len(party.places)
print "filtered", len(party.filteredPlaces)

# Test 2
print "PARTY 2\nPARTY 2\nPARTY 2\nPARTY 2\n"
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

# Test the sadness function
print "Sadness function tests: \n"
print party1.sadnessFunction(np.random.choice(party1.filteredPlaces))

algs = alg.Algorithm()

# Testing algorithms
solution = algs.dfsSearch(party1)
print "DFS Solution"
totalAverageSadness = 0
for sol in solution[0]:
    averageSadness =  sum(sol["sadness"])/len(sol["sadness"])
    print str(sol["name"]), averageSadness
    totalAverageSadness += averageSadness

print "\nTotal Average Sadness\n", totalAverageSadness

solution = algs.greedySearch(party1)
print "Greedy Solution"
totalAverageSadness = 0
for sol in solution[0]:
    averageSadness =  sum(sol["sadness"])/len(sol["sadness"])
    print str(sol["name"]), averageSadness
    totalAverageSadness += averageSadness

print "\nTotal Average Sadness\n", totalAverageSadness

solution = algs.astarSearch(party1)
print "A* Solution"
totalAverageSadness = 0
for sol in solution[0]:
    averageSadness =  sum(sol["sadness"])/len(sol["sadness"])
    print str(sol["name"]), averageSadness
    totalAverageSadness += averageSadness

print "\nTotal Average Sadness\n", totalAverageSadness

# BFS and DFS take a long time, uncomment if you have the patience.

solution = algs.bfsSearch(party1)
print "BFS Solution"
totalAverageSadness = 0
for sol in solution[0]:
    averageSadness =  sum(sol["sadness"])/len(sol["sadness"])
    print str(sol["name"]), averageSadness
    totalAverageSadness += averageSadness

print "\nTotal Average Sadness\n", totalAverageSadness

solution = algs.ucsSearch(party1)
print "UCS Solution"
totalAverageSadness = 0
for sol in solution[0]:
    averageSadness =  sum(sol["sadness"])/len(sol["sadness"])
    print str(sol["name"]), averageSadness
    totalAverageSadness += averageSadness

print "\nTotal Average Sadness\n", totalAverageSadness
