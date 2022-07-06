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
    def __init__(self):
        self.users = Users()

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/")

class Users():
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def auth(self):
        body = cherrypy.request.json
        if body["username"] == "admin" and body["password"] == "admin":
            return {"authentication": "OK","token": "jaodh2323jd23jajkd7191ja91jlK"}
        else:
            return {"authentication": "ERROR","token": ""}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    print(SERVER_CONFIG)
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)