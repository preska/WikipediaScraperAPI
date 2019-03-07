import json
import logging
import urllib.request
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup

from graph.actor import Actor
from graph.graph_library import Graph
from graph.movie import Movie


def getHtmlDoc(link):
    if(link is not ""):
        request = urllib.request.Request(link)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as err:
            logging.error("Error accessing link: " + link)
            return None
        else:
            html_doc = response.read()
        html_doc = BeautifulSoup(html_doc, 'html.parser')
        return html_doc

def graphToJson(g):
    actors = g.getAllActors()
    movies = g.getAllMovies()

    with open("/Users/preska/School/sp19/CS242/sp-19-cs242-assignment2/jsonfiles/actors.json", 'w') as f:
        for k, v in actors.items():
            f.write(v.getJson())

    with open("/Users/preska/School/sp19/CS242/sp-19-cs242-assignment2/jsonfiles/movies.json", 'w') as f:
        for k,v in movies.items():
            f.write(v.getJson())



def jsonToGraph(g):
    with open("/Users/preska/School/sp19/CS242/sp-19-cs242-assignment2/jsonfiles/data.json", 'r') as json_data:
        data = json.load(json_data)

    #add nodes
    for d in data:
        for value in d.items():
            if(value[1]['json_class'] == "Actor"):
                a = Actor(value[1]['name'], value[1]['age'], "", value[1]['total_gross'], value[1]['movies'])
                g.addActor(a)
            else:
                m = Movie(value[1]['name'], value[1]['year'], value[1]['box_office'], value[1]['wiki_page'], value[1]['actors'])
                g.addMovie(m)

    #add edges
    actors = g.getAllActors()
    movies = g.getAllMovies()

    for actor_name in actors:
        actor = g.getActor(actor_name)
        for movie_name in actor.getMovieList():
            movie = g.getMovie(movie_name)
            if(movie is not None):
                actor.addEdge(movie, actor.getAge())

    for movie_name in movies:
        movie = g.getMovie(movie_name)
        for actor_name in movie.getActorList():
            actor = g.getActor(actor_name)
            if(actor is not None):
                movie.addEdge(actor, actor.getAge())

def analyzeData():
    g = Graph()
    jsonToGraph(g)
    actors = g.getAllActors()
    movies = g.getAllMovies()

    #hub actors
    hub_actors = {}
    for actor_name1 in actors:
        for actor_name2 in actors:
            actor1_movielist = g.getActor(actor_name1).getMovieList()
            actor2_movielist = g.getActor(actor_name2).getMovieList()
            if(len(list(set(actor1_movielist).intersection(actor2_movielist)))):
                if(actor_name1 in hub_actors):
                    hub_actors[actor_name1] += 1
                else:
                    hub_actors[actor_name1] = 1

                if(actor_name2 in hub_actors):
                    hub_actors[actor_name2] += 1
                else:
                    hub_actors[actor_name2] = 1
    hub_actors = sorted(hub_actors, key=hub_actors.get, reverse=True)
    print("Hub Actors in order: ", hub_actors)

    #top grossing age group
    top_grossing = {}
    for actor_name in actors:
        actor = g.getActor(actor_name)
        actor_age = actor.getAge()
        actor_grossing = actor.getTotalGross()
        if(actor_age in top_grossing):
            top_grossing[actor_age] += actor_grossing
        else:
            top_grossing[actor_age] = actor_grossing

    colors = list("rgbcmyk")

    x = top_grossing.keys()
    y = top_grossing.values()
    plt.scatter(x,y,color=colors.pop())

    plt.legend(top_grossing.keys())
    plt.show()

    top_grossing = sorted(top_grossing, key=top_grossing.get, reverse=True)
    print("Top grossing age groups in order: ", top_grossing)



#analyzeData()
