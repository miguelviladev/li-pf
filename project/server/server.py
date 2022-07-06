import cherrypy
from config import *
import os

class Root(object):
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        return open(INDEX_PAGE).read()


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    print(SERVER_CONFIG)
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)
    