import json

class Movie:
    def __init__(self, name, year, grossing, link, actors):
        self.name = name
        self.year = year
        self.grossing = grossing
        self.link = link
        self.actors = actors
        self.weights = {}

    def addEdge(self, actor, weight_val):
        self.weights[actor.getName()] = weight_val

    def getActors(self):
        return self.weights.keys()

    def getName(self):
        return self.name

    def getGrossing(self):
        return self.grossing

    def getActorList(self):
        return self.actors

    def setName(self, name):
        self.name = name

    def setYear(self, year):
        self.year = year

    def setGrossing(self, grossing):
        self.grossing = grossing

    def setLink(self, link):
        self.link = link

    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': '))
