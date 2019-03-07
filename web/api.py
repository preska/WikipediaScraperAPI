from flask import Flask, Response, json
from flask import request

from graph.actor import Actor
from graph.graph_library import Graph
from graph.movie import Movie
from webscraper.utils import jsonToGraph, graphToJson

app = Flask(__name__)

g = Graph()
jsonToGraph(g)

@app.route('/')
def index():
    return "Movies and Actors REST API"

'''
/actors?name=”Bob”
Filters out all actors that don’t have “Bob” in their name
'''
@app.route('/actors', methods=['GET'])
def getActors():
    response = ""
    name = request.args.get('name')
    actors = g.getAllActors()
    for actor_name in actors:
        if(name in actor_name):
            actor = g.getActor(actor_name)
            response += actor.getJson()

    if(response is not ""):
        return Response(response, status=200, mimetype='application/json')
    else:
        return Response(response, status=404, mimetype='application/json')

'''
/movies?name=”Shawshank&Redemption”
Filters out all actors that don’t have “Shawshank&Redemption” in their name
'''
@app.route('/movies', methods=['GET'])
def getMovies():
    response = ""
    name = request.args.get('name')
    movies = g.getAllMovies()
    for movie_name in movies:
        if(name in movie_name):
            movie = g.getMovie(movie_name)
            response += movie.getJson()

    if(response is not ""):
        return Response(response, status=200, mimetype='application/json')
    else:
        return Response(response, status=404, mimetype='application/json')

'''
/actors/Bruce_Willis
Returns the first Actor object that has name “Bruce Willis”, displays actor attributes and metadata
'''
@app.route('/actors/<actor_name>', methods=['GET'])
def getActor(actor_name):
    actor = g.getActor(actor_name)
    if(actor is not None):
        return Response(actor.getJson(), status=200, mimetype='application/json')
    else:
        return Response({}, status=404, mimetype='application/json')


'''
/movies/Shawshank_Redemption
Returns the first Movie object that has correct name, displays movie attributes and metadata
'''
@app.route('/movies/<movie_name>', methods=['GET'])
def getMovie(movie_name):
    movie = g.getMovie(movie_name)
    if(movie is not None):
        return Response(movie.getJson(), status=200, mimetype='application/json')
    else:
        return Response({}, status=404, mimetype='application/json')

#PUT
'''
Leverage PUT requests to update standing content in backend
'''
@app.route('/actors/<actor_name>', methods=['PUT'])
def putActor(actor_name):
    actor = g.getActor(actor_name)
    content = request.get_json()
    for key, value in content.items():
        if(key == 'name'):
            actor.setName(value)
        elif(key == 'age'):
            actor.setAge(value)
        elif(key == 'link'):
            actor.setLink(value)
        elif(key == 'total_gross'):
            actor.setTotalGross(value)
        elif(key == 'movie'):
            actor.addEdge(value, actor.getAge())
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

'''
Leverage PUT requests to update standing content in backend
'''
@app.route('/movies/<movie_name>', methods=['PUT'])
def putMovie(movie_name):
    movie = g.getMovie(movie_name)
    content = request.get_json()
    for key, value in content.items():
        if(key == 'name'):
            movie.setName(value)
        elif(key == 'year'):
            movie.setYear(value)
        elif(key == 'link'):
            movie.setLink(value)
        elif(key == 'grossing'):
            movie.setGrossing(value)
        elif(key == 'actor'):
            movie.addEdge(value, 0)
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

#POST
'''
Leverage POST requests to ADD content to backend
'''
@app.route('/actors/<foo>', methods=['POST'])
def postActor(foo):
    content = request.get_json()
    a = Actor(None, None, None, None, None)
    for key, value in content.items():
        if(key == 'name'):
            a.setName(value)
        elif(key == 'age'):
            a.setAge(value)
        elif(key == 'link'):
            a.setLink(value)
        elif(key == 'total_gross'):
            a.setTotalGross(value)
        elif(key == 'movie'):
            a.addEdge(value, a.getAge())
    g.addActor(a)
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

'''
Leverage POST requests to ADD content to backend
'''
@app.route('/movies/<foo>', methods=['POST'])
def postMovie(foo):
    content = request.get_json()
    m = Movie(None, None, None, None, None)
    for key, value in content.items():
        if(key == 'name'):
            m.setName(value)
        elif(key == 'year'):
            m.setYear(value)
        elif(key == 'link'):
            m.setLink(value)
        elif(key == 'grossing'):
            m.setGrossing(value)
        elif(key == 'actor'):
            m.addEdge(value, 0)
    g.addMovie(m)
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

#DELETE
'''
/actors/:{actor_name}
Leverage DELETE requests to REMOVE content from backend
'''
@app.route('/actors/<actor_name>', methods=['DELETE'])
def deleteActor(actor_name):
    actor = g.getActor(actor_name)
    g.deleteActor(actor)
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

'''
/movies/:{movie_name}
Leverage DELETE requests to REMOVE content from backend
'''
@app.route('/movies/<movie_name>', methods=['DELETE'])
def deleteMovie(movie_name):
    movie = g.getMovie(movie_name)
    g.deleteMovie(movie)
    graphToJson(g)
    return Response({}, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
