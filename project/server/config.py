import os

SERVER  = os.path.abspath(os.path.dirname(__file__))
STORAGE = os.path.normpath(os.path.join(SERVER, '../storage'))
STORAGE_DB = os.path.normpath(os.path.join(STORAGE, '../storage/database.db'))
WATERMARK = os.path.normpath(os.path.join(SERVER, '../client/img/logo.png'))
SHAPE = os.path.normpath(os.path.join(STORAGE, 'temp/shape.png'))
FONT = os.path.normpath(os.path.join(STORAGE, 'arial.ttf'))
KEY = b'umapasswordfixe!'
BLOCKSIZE = 16

LANDING_PAGE = os.path.normpath(os.path.join(SERVER, '../client/landing.html'))
SIGNIN_PAGE_BODY = os.path.normpath(os.path.join(SERVER, '../client/body-signin.html'))
SIGNUP_PAGE_BODY = os.path.normpath(os.path.join(SERVER, '../client/body-signup.html'))
UPLOAD_PAGE_BODY= os.path.normpath(os.path.join(SERVER, '../client/body-upload.html'))
COLLECTIONS_PAGE= os.path.normpath(os.path.join(SERVER, '../client/collections.html'))
ABOUT_PAGE= os.path.normpath(os.path.join(SERVER, '../client/about.html'))
PROFILE_PAGE= os.path.normpath(os.path.join(SERVER, '../client/profile.html'))


SERVER_CONFIG = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': SERVER
    },
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.normpath(os.path.join(SERVER, '../client/css/'))
    },
    '/img': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.normpath(os.path.join(SERVER, '../client/img/'))
    },
    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.normpath(os.path.join(SERVER, '../client/js/'))
    }
}