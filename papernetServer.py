#coding=utf-8 
from __future__ import division
import os, os.path
import cherrypy
import string
import json

import searchServer
import exploreServer
import LDAServer

class Papernet_index(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')
    def dashboard(self):
        return open('dashboard.html')
    def explore(self):
        return open('explore.html')
    def LDA(self):
        return open('LDA.html')



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        
        '/dashboard': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },

        '/explore': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },   

        '/LDA': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },    
        
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './'
        }
    }

    webapp = Papernet_index()
    webapp.dashboard = searchServer.Papernet_dashboardService()
    webapp.explore = exploreServer.Papernet_exploreService()
    webapp.LDA = LDAServer.Papernet_LDAService()
    cherrypy.server.socket_host= "0.0.0.0"
    cherrypy.quickstart(webapp, '/', conf)




