import json

class Actor:
    def __init__(self, name, age, link, total_gross, movies):
        self.name = name
        self.age = age
        self.link = link
        self.total_gross = total_gross
        self.movies = movies
        self.weights = {}

    def addEdge(self, movie, weight):
        self.weights[movie.getName()] = weight

    def getEdge(self, movie_name):
        return self.weights[movie_name]

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def getLink(self):
        return self.link

    def setLink(self, link):
        self.link = link

    def getMovies(self):
        return self.weights.keys()

    def getMovieList(self):
        return self.movies

    def setTotalGross(self, total_gross):
        self.total_gross = total_gross

    def getTotalGross(self):
        return self.total_gross

    def getJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=(',', ': '))


