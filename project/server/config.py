import os

SERVER  = os.path.abspath(os.path.dirname(__file__))
STORAGE = os.path.normpath(os.path.join(SERVER, '../storage'))
STORAGE_DB = os.path.normpath(os.path.join(STORAGE, '../storage/database.db'))

INDEX_PAGE = os.path.normpath(os.path.join(SERVER, '../client/index.html'))
SIGNIN_PAGE_BODY = os.path.normpath(os.path.join(SERVER, '../client/body-signin.html'))
SIGNUP_PAGE_BODY = os.path.normpath(os.path.join(SERVER, '../client/body-signup.html'))

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