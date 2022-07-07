import cherrypy
import secrets
import string
import random
import time
from config import *
from sqlcon import *
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
        user = selector("SELECT * FROM users WHERE username = ? AND password = ?", (body["username"], body["password"]))
        if len(user) == 1:
            token = secrets.token_hex(4)
            expire = int(time.time()) + 7200
            executor("UPDATE users SET access_token = ? WHERE username = ?",(token, body["username"]))
            executor("UPDATE users SET expiration = ? WHERE username = ?",(expire, body["username"]))
            return {"authentication": "OK","token": "{}".format(token)}
        else:
            return {"authentication": "ERROR","token": ""}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def valid(self):
        body = cherrypy.request.json
        expiration = selector("SELECT expiration FROM users WHERE access_token = ?", (body["token"],))
        if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
            return {"authentication": "ERROR"}
        else:
            return {"authentication": "OK"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create(self):
        body = cherrypy.request.json
        invalid = False
        for c in body["username"]:
            if c not in string.ascii_letters + string.digits:
                invalid = True
        if body["username"].rstrip() == "" or selector("SELECT * FROM users WHERE username = ?", (body["username"],)) or invalid:
            return {"creation": "ERROR","password": ""}
        else:
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            executor("INSERT INTO users (username, password, ownerships, access_token, expiration) VALUES (?, ?, '', '', 0)",(body["username"], password))
            return {"creation": "OK", "password": "{}".format(password)}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    initializeDatabase()
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)