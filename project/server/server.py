import cherrypy
from config import *
import os

class Root(object):
    def __init__(self):
        self.api = Api()

    @cherrypy.expose
    def index(self):
        return open(INDEX_PAGE).read()

    @cherrypy.expose
    def signin(self):
        return open(SIGNIN_PAGE).read()

    @cherrypy.expose
    def signup(self):
        return open(SIGNUP_PAGE).read()

class Api(object):
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/")

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    print(SERVER_CONFIG)
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)