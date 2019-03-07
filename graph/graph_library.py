# Graph library

class Graph:
    def __init__(self):
        self.movie_nodes = {}
        self.actor_nodes = {}

    def getActorKeys(self):
        return self.actor_nodes.keys()

    def getMovieKeys(self):
        return self.movie_nodes.keys()

    def getAllMovies(self):
        return self.movie_nodes

    def getAllActors(self):
        return self.actor_nodes

    def addMovie(self, node):
        if node.getName() not in self.movie_nodes:
            try :
                node.getAge()
            except:
                self.movie_nodes[node.getName()] = node

    def addActor(self, node):
        if node.getName() not in self.actor_nodes:
            try :
                node.getYear()
            except:
                self.actor_nodes[node.getName()] = node

    def getMovie(self, node_name):
        if node_name in self.movie_nodes:
            return self.movie_nodes[node_name]
        else:
            return None

    def getActor(self, node_name):
        if node_name in self.actor_nodes:
            return self.actor_nodes[node_name]
        else:
            return None

    def deleteMovie(self, node):
        if node.getName() in self.movie_nodes:
            if(node in self.movie_nodes):
                del self.movie_nodes[node]

    def deleteActor(self, node):
        if node.getName() in self.actor_nodes:
            if(node in self.actor_nodes):
                del self.actor_nodes[node]
