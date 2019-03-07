import logging

from graph.graph_library import Graph
from webscraper import utils, scraper

def main():
    logging.basicConfig(filename='/Users/preska/School/sp19/CS242/sp-19-cs242-assignment2/logfiles/logfile.log', filemode='w', level=logging.DEBUG)
    g = Graph()
    logging.info('START SCRAPER')
    scraper.startScraper("https://en.wikipedia.org/wiki/Morgan_Freeman", g)
    logging.info('END SCRAPER')
    logging.info('START GRAPH TO JSON CONVERSION')
    utils.graphToJson(g)
    logging.info('END GRAPH TO JSON CONVERSION')
    getMovieGrossedValue(g, "Brubaker")
    getMovieListFromActor(g, "Morgan Freeman")
    getActorListFromMovie(g, "Brubaker")

main()

def getMovieGrossedValue(g, movie):
   return (g.getMovie(movie.getName())).getGrossing()

def getMovieListFromActor(g, actor):
    return (g.getActor(actor.getName())).getMovies()

def getActorListFromMovie(g, movie):
    return (g.getMovie(movie.getName())).getActors()

