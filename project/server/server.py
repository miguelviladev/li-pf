import cherrypy
import secrets
import string
import random
import time
import os
import io

from cherrypy.lib import file_generator
from config import *
from sqlcon import *
from imgproc import *


class Root(object):
	def __init__(self):
			self.api = Api()
	@cherrypy.expose
	def index(self):
			return open(LANDING_PAGE).read()
		
	@cherrypy.expose
	def collections(self, id = None):
		if id == None:
			return open(SCRIPT_COLLECTIONS).read()
		else:
			return "dsasa"
		
	@cherrypy.expose
	def about(self):
			return open(ABOUT_PAGE).read()
		
	@cherrypy.expose
	def profile(self):
			return open(PROFILE_PAGE).read()
		
	@cherrypy.expose
	def upload(self):
		return open(SCRIPT_UPLOAD).read()

	@cherrypy.expose
	def signin(self):
		return open(SCRIPT_SIGNIN).read()

	@cherrypy.expose
	def signup(self):
		return open(SCRIPT_SIGNUP).read()




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

		@cherrypy.expose
		@cherrypy.tools.json_in()
		@cherrypy.tools.json_out()
		def collections(self):
			body = cherrypy.request.json
			expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body['token'],))
			if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
				return {"status": "FORBIDDEN", "body": ""}
			else:
				return {"status": "OK", "body": open(COLLECTIONS_PAGE_BODY).read()}



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
		def __init__(self):
			self.image = CromosImg()

		@cherrypy.expose
		@cherrypy.tools.json_out()
		def index(self, id = None):
			if id == None:
				images = selector("SELECT * FROM images", ())
			else:
				images = selector("SELECT * FROM images WHERE collection = ?", (id,))
			return images if len(images) > 0 else {"status": "ERROR", "message": "No images found"}

		@cherrypy.expose
		@cherrypy.tools.json_in()
		@cherrypy.tools.json_out()
		def collections(self):
			body = cherrypy.request.json
			expiration = selector("SELECT expiry FROM tokens WHERE token = ?", (body["token"],))
			if body["token"] == None or len(expiration) == 0 or expiration[0][0] < int(time.time()):
				return {'status': 'ERROR'}
			else:
				collections = selector("SELECT * FROM collections", ())
				return {"status": "OK", "message": "Got collections", "body": collections} if len(collections) > 0 else {"status": "OK", "message": "No collections found"}

		@cherrypy.expose
		@cherrypy.tools.json_in()
		@cherrypy.tools.json_out()
		def upload(self):
			body = cherrypy.request.json
			text_to_remove = body["image"][:body["image"].index(",")]
			base64_image = body["image"].replace(text_to_remove, "")

			image_name = body["name"].capitalize()
			image_collection = body["collection"].title()
			image_extension = text_to_remove[text_to_remove.index("/")+1:text_to_remove.index(";")]
			image_hash = hashImage(base64_image)
			if selector("SELECT * FROM images WHERE hash = ?", (image_hash,)):
						return {"status": "ERROR","message": "similar image already exists"}

			os.makedirs(os.path.normpath(os.path.join(STORAGE,"temporary/")), exist_ok=True)
			os.makedirs(os.path.normpath(os.path.join(STORAGE,"protected/")), exist_ok=True)
			os.makedirs(os.path.normpath(os.path.join(STORAGE,"original/")), exist_ok=True)

			temp_image_path = os.path.normpath(os.path.join(STORAGE,f"temporary/{image_hash}.{image_extension}"))
			water_image_path = os.path.normpath(os.path.join(STORAGE,f"protected/{image_hash}.{image_extension}"))
			original_image_path = os.path.normpath(os.path.join(STORAGE,f"original/{image_hash}.{image_extension}"))

			writeImage(base64_image, temp_image_path)
			writeWatermarkedImage(temp_image_path, water_image_path, WATERMARK)
			writeImage(encryptImage(base64_image), original_image_path)

			executor("INSERT INTO images (name, collection, hash, extension) VALUES (?, ?, ?, ?)",(image_name, image_collection, image_hash, image_extension))

			if not selector("SELECT * FROM collections WHERE name = ?", (image_collection,)):
						owner = selector("SELECT username FROM tokens WHERE token = ?", (body["token"],))[0][0]
						executor("INSERT INTO collections (name, owner) VALUES (?, ?)",(image_collection, owner,))
			return {"status": "OK"}

class CromosImg(object):
		@cherrypy.expose
		def index(self, id):
			cherrypy.response.headers['Content-Type'] = "image/png"

			image_data = selector("SELECT * FROM images WHERE identifier = ?", (id,))

			if len(image_data) == 0:
				return {"status": "ERROR", "message": "Image not found"}

			image_path = os.path.normpath(os.path.join(STORAGE,f"protected/{image_data[0][3]}.{image_data[0][2]}"))

			with open(image_path, "rb") as image:
				image_bytes = image.read()

			image_buffer = io.BytesIO(image_bytes)
			image_buffer.seek(0)

			return file_generator(image_buffer)

if __name__ == '__main__':
		cherrypy.config.update({'server.socket_port': 10005})
		initializeDatabase()
		cherrypy.quickstart(Root(), '/', SERVER_CONFIG)