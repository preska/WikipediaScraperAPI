import unittest

from graph.actor import Actor
from graph.graph_library import Graph
from graph.movie import Movie


class TestGraph(unittest.TestCase):
    g = Graph()

    #Create actors and movies
    actor1 = Actor("actor1", 25, "https://www.actor1.com")
    actor2 = Actor("actor2", 45, "https://www.actor2.com")
    movie1 = Movie("movie1", "2018", "320830983", "https://www.movie1.com")
    movie2 = Movie("movie2",  "2013", "12038130", "https://www.movie2.com")

    def testAddActorAndGets(self):
        self.g.addActor(self.actor1)
        self.assertEqual((self.g.getActor(self.actor1.getName())).getName(), 'actor1')
        self.assertEqual((self.g.getActor(self.actor1.getName())).getAge(), 25)
        self.assertEqual((self.g.getActor(self.actor1.getName())).getLink(), "https://www.actor1.com")

    def testAddMovieAndGets(self):
        self.g.addMovie(self.movie1)
        self.assertEqual((self.g.getMovie(self.movie1.getName())).getName(), 'movie1')
        self.assertEqual((self.g.getMovie(self.movie1.getName())).getGrossing(), '320830983')


def main():
    g = TestGraph()
    g.testAddActorVertex()
