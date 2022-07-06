import os

SERVER  = os.path.abspath(os.path.dirname(__file__))

INDEX_PAGE = os.path.normpath(os.path.join(SERVER, '../client/index.html'))

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