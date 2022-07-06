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
        #user = selector("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(body["username"], body["password"]))
        user = selector("SELECT * FROM users WHERE username = ? AND password = ?", (body["username"], body["password"]))
        if len(user) == 1:
            token = secrets.token_hex(4)
            expire = int(time.time()) + 7200
            splited_tokens = user[0][3].split("#")
            if len(splited_tokens)> 9:
                del splited_tokens[0]
                splited_tokens.append(f"{secrets.token_hex(16)},{expire}")
            else:
                splited_tokens.append(f"{secrets.token_hex(16)},{expire}")
            executor("UPDATE users SET access_tokens = ? WHERE username = ?",("#".join(splited_tokens), body["username"]))
            return {"authentication": "OK","token": "{}".format(token)}
        else:
            return {"authentication": "ERROR","token": ""}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def create(self):
        body = cherrypy.request.json
        if body["username"].rstrip() == "" or selector("SELECT * FROM users WHERE username = ?", (body["username"],)):
            return {"creation": "ERROR","password": ""}
        else:
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            executor("INSERT INTO users (username, password, ownerships, access_tokens) VALUES (?, ?, '', '')",(body["username"], password))
            return {"creation": "OK", "password": "{}".format(password)}

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    initializeDatabase()
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)