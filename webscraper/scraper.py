import logging
import re

from graph.actor import Actor
from graph.movie import Movie
from webscraper import utils

# Citations: https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#            https://stackoverflow.com/questions/54875196/beautifulsoup-find-a-div-tag-by-the-text-inside/54875716#54875716

movie_threshold = 125
actor_threshold = 250

def scrapeActor(link, g):
    actor_page = utils.getHtmlDoc(link)
    if(actor_page is None):
        return None

    name = actor_page.find('h1').text
    #print(name)

    age = actor_page.find('span', attrs={'class': 'noprint ForceAgeToShow'})
    if(age is not None):
        age = age.text
        age = age.split()[1]
        age = int(age[:-1])
        #print(age)
    if(age is None):
        logging.warning("Age info not found for " + name)
        return
    a = Actor(name, age, link)
    g.addActor(a)
    return a

def scrapeMovie(link, g):
    movie_page = utils.getHtmlDoc(link)
    if(movie_page is None):
        return None

    name = movie_page.find('h1').text
    #print(name)

    year = movie_page.find(text="Release date")
    if(year is not None):
        year = year.find_next('td').text
        if year[-1] == ']':
            year = year[:-3]
        for word in year.split():
            if len(word) == 4:
                try:
                    year = word
                    break
                except ValueError:
                    logging.warning("Year info not found for " + name)
                    pass
    else:
        year = "2019"

    #print(year)

    grossing = movie_page.find(text="Box office")
    if grossing is not None:
        grossing = grossing.find_next('td').text
    else:
        logging.warning("Grossing value could not be found for " + name)
        m = Movie(name, year, 0, link)
        g.addMovie(m)
        return m

    if (grossing[0] == '$'):
        grossing = grossing[1:]

    if grossing[0] != '$':
        logging.warning("Grossing value could not be found for " + name)
        m = Movie(name, year, 0, link)
        g.addMovie(m)
        return m

    if grossing[-7:] == "million":
        multiplier = 1000000
    elif grossing[-7:] == "billion":
        multiplier = 1000000000
    else:
        grossing = re.sub(r'\D', '', grossing)
        m = Movie(name, year, int(grossing), link)
        g.addMovie(m)
        return m

    if grossing[-1] == ']':
        grossing = grossing[:-3]

    grossing = grossing.split()[0]
    try:
        grossing = int(grossing)
    except ValueError:
        grossing = float(grossing)

    grossing = int(grossing) * multiplier

    m = Movie(name, year, grossing, link)
    g.addMovie(m)
    return m

def scrapeMovieForActorList(link, g):
    movie_page = utils.getHtmlDoc(link)
    if(movie_page is None):
        return None

    movie = scrapeMovie(link, g)
    if(movie is not None):
        cast = movie_page.find(id="Cast")
        if(cast is not None):
            ul = cast.find_next('ul')
            for li in ul.findAll('li'):
                a = li.find_next('a')
                if(a is not None):
                    actor_link = "https://en.wikipedia.org" + a.get('href')
                    #print(actor_link)
                    actor = scrapeActor(actor_link, g)
                    if(actor is not None):
                        if(actor.getAge() is not None):
                            edge_weight = actor.getAge()
                        else:
                            edge_weight = 0
                        movie.addEdge(actor, edge_weight)
                        actor.addEdge(movie, edge_weight)
    else:
        logging.info("Cast info not found")

def scrapeActorForMovieList(link, g):
    actor_page = utils.getHtmlDoc(link)
    if(actor_page is None):
        return None

    actor = scrapeActor(link, g)
    if actor is not None:
        film = actor_page.find(id="Film")
        if(film is not None):
            table = film.find_next('table')
            for tr in table.findAll('tr'):
                a = tr.find_next('a')
                movie_link = 'https://en.wikipedia.org' + a.get('href')
                movie = scrapeMovie(movie_link, g)
                addToGraph(actor, movie, movie_link, g)
                if len(g.getActorKeys()) > actor_threshold:
                    break
        else:
            film = actor_page.find(id="Filmography")
            if(film is not None):
                ul = film.find_next('ul')
                for li in ul.findAll('li'):
                    a = li.find_next('a')
                    movie_link = 'https://en.wikipedia.org' + a.get('href')
                    movie = scrapeMovie(movie_link, g)
                    addToGraph(actor, movie, movie_link, g)
                    if len(g.getActorKeys()) > actor_threshold:
                        break

def addToGraph(actor, movie, movie_link, g):
    if movie is not None:
        if actor.getAge() is not None:
            edge_weight = actor.getAge()
        else:
            edge_weight = 0
        movie.addEdge(actor, edge_weight)
        actor.addEdge(movie, edge_weight)
        scrapeMovieForActorList(movie_link, g)

def startScraper(link, g):
    actor_page = utils.getHtmlDoc(link)
    if(actor_page is None):
        return None

    if(actor_page.find(id="Film") is not None or actor_page.find(id="Filmography") is not None):
        scrapeActorForMovieList(link, g)
        actor_list = list(g.getActorKeys())
        for actor in actor_list:
            scrapeActorForMovieList((g.getActor(actor)).getLink(), g)
            if(len(g.getMovieKeys()) > movie_threshold):
                break
    else:
        logging.error("Film not found")
        return -1
    return 0
