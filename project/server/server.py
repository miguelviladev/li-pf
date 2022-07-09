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
        return open(LANDING_PAGE).read()
      
    @cherrypy.expose
    def collections(self):
        return open(COLLECTIONS_PAGE).read()
      
    @cherrypy.expose
    def about(self):
        return open(ABOUT_PAGE).read()
      
    @cherrypy.expose
    def profile(self):
        return open(PROFILE_PAGE).read()
      
    @cherrypy.expose
    def upload(self):
        return """
            <!DOCTYPE html>
            <html lang="pt-PT">
              <head>
                <!-- Meta Tags Necessárias -->
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <!-- CSS do Bootstrap -->
                <link rel="stylesheet" href="./css/bootstrap.min.css" />
                <!-- CSS do FontAwesome -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
                <!-- CSS Personalizado -->
                <link rel="stylesheet" href="./css/global-style.css" />
                <link rel="stylesheet" href="./css/navbar-style.css" />
                <link rel="stylesheet" href="./css/upload-style.css" />
                <!-- JS Personalizado -->
                <script src="./js/navbar.js"></script>
                <!-- Favicon -->
                <link rel="icon" type="image/x-icon" href="./img/favicon.png" />
                <title>Upload</title>
              </head>
              <body data-bs-spy="scroll" data-bs-offset="200" data-bs-target=".navbar">
                <main>
                  <script>
                    async function verify() {
                      const options = {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({"token": localStorage.getItem('token')})
                      };
                      const response = await (await fetch('/api/pages/upload', options)).json();
                      if (response.status == 'OK') {                 
                        document.getElementsByTagName('main')[0].innerHTML = response.body;
                      } else {
                        window.location.href = '/';
                      }
                    };
                    verify();
                  </script>
                </main>
                <script src="./js/upload.js"></script>
                <script src="./js/bootstrap.bundle.min.js"></script>
                <script src="./js/jquery-3.6.0.min.js"></script>
              </body>
            </html>
        """

    @cherrypy.expose
    def signin(self):
        return """
            <!DOCTYPE html>
            <html lang="pt-PT">
              <head>
                <!-- Meta Tags Necessárias -->
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <!-- CSS do Bootstrap -->
                <link rel="stylesheet" href="/css/bootstrap.min.css" />
                <!-- CSS do FontAwesome -->
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                <!-- CSS Personalizado -->
                <link rel="stylesheet" href="/css/global-style.css" />
                <link rel="stylesheet" href="/css/navbar-style.css" />
                <link rel="stylesheet" href="/css/signinup-style.css" />
                <!-- JS Personalizado -->
                <script src="/js/navbar.js"></script>
                <!-- Favicon -->
                <link rel="icon" type="image/x-icon" href="/img/favicon.png">
                <title>Iniciar Sessão</title>
              </head>
              <body data-bs-spy="scroll" data-bs-offset="200" data-bs-target=".navbar">
                <main>
                  <script>
                    async function verify() {
                      const options = {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({"token": localStorage.getItem('token')})
                      };
                      const response = await (await fetch('/api/pages/signin', options)).json();
                      if (response.status == 'OK') {                 
                        document.getElementsByTagName('main')[0].innerHTML = response.body;
                      } else {
                        window.location.href = '/';
                      }
                    };
                    verify();
                  </script>
                </main>
                <script src="./js/signin.js"></script>
                <script src="./js/bootstrap.bundle.min.js"></script>
              </body>
            </html>
        """

    @cherrypy.expose
    def signup(self):
        return """
            <!DOCTYPE html>
            <html lang="pt-PT">
              <head>
                 <!-- Meta Tags Necessárias -->
                 <meta charset="UTF-8" />
                 <meta name="viewport" content="width=device-width, initial-scale=1" />
                 <!-- CSS do Bootstrap -->
                 <link rel="stylesheet" href="./css/bootstrap.min.css" />
                 <!-- CSS do FontAwesome -->
                 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                 <!-- CSS Personalizado -->
                 <link rel="stylesheet" href="./css/global-style.css" />
                 <link rel="stylesheet" href="./css/navbar-style.css" />
                 <link rel="stylesheet" href="./css/signinup-style.css" />
                 <!-- JS Personalizado -->
                 <script type="module" src="./js/authrestriction.js"></script>
                 <script src="./js/navbar.js"></script>
                 <!-- Favicon -->
                 <link rel="icon" type="image/x-icon" href="./img/favicon.png">
                 <title>Criar Conta</title>
              </head>
              <body data-bs-spy="scroll" data-bs-offset="200" data-bs-target=".navbar">
                <main>
                  <script>
                    async function verify() {
                      const options = {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({"token": localStorage.getItem('token')})
                      };
                      const response = await (await fetch('/api/pages/signup', options)).json();
                      if (response.status == 'OK') {                 
                        document.getElementsByTagName('main')[0].innerHTML = response.body
                      } else {
                        window.location.href = '/';
                      }
                    };
                    verify();
                  </script>
                </main>
                <script src="./js/signup.js"></script>
                <script src="./js/bootstrap.bundle.min.js"></script>
              </body>
            </html>
        """




class Api(object):

    def __init__(self):
        self.users = Users()
        self.pages = Pages()
        self.cromos = Cromos()

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/")




class Pages():

    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def landing(self):
      body = cherrypy.request.json
      expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body['token'],))
      if body['token'] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
        return {'status': 'OK1', 'body': '<a id="a-button-action" href="/signin"><button id="button-action" type="button" class="btn btn-primary">Autenticação <i class="fa-solid fa-key"></i></button></a>'}
      else:
        return {'status': 'OK', 'body': '<a id="a-button-action" href="/collections"><button id="button-action" type="button" class="btn btn-primary">Ver Coleções <i class="fa-solid fa-images"></i></button></a>'}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def signin(self):
        body = cherrypy.request.json
        expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body['token'],))
        if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
            return {"status": "OK", "body": open(SIGNIN_PAGE_BODY).read()}
        else:
            return {"status": "FORBIDDEN", "body": ""}
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def signup(self):
        body = cherrypy.request.json
        expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body['token'],))
        if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
            return {"status": "OK", "body": open(SIGNUP_PAGE_BODY).read()}
        else:
            return {"status": "FORBIDDEN", "body": ""}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def upload(self):
        body = cherrypy.request.json
        expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body['token'],))
        if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
            return {"status": "FORBIDDEN", "body": ""}
        else:
            return {"status": "OK", "body": open(UPLOAD_PAGE_BODY).read()}



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
            executor("INSERT INTO tokens (token, expiry, username) VALUES (?, ?, ?)",(token, expire, body["username"],))
            return {"authentication": "OK","token": "{}".format(token)}
        else:
            return {"authentication": "ERROR","token": ""}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def valid(self):
        body = cherrypy.request.json
        expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body["token"],))
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
            executor("INSERT INTO users (username, password, owimages) VALUES (?, ?, '')",(body["username"], password))
            return {"creation": "OK", "password": "{}".format(password)}



@cherrypy.popargs("id")
class Cromos():

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, id = None):
      if id == None:
        images = selector("SELECT * FROM images", ())
      else:
        images = selector("SELECT * FROM images WHERE collection = ?", (id,))
      return images if len(images) > 0 else {"status": "ERROR", "message": "No images found"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self):
      print(cherrypy.request.body.read())
      return {"status": "OK"}


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 10005})
    initializeDatabase()
    cherrypy.quickstart(Root(), '/', SERVER_CONFIG)