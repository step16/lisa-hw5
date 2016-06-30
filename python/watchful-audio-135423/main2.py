#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import json
from google.appengine.api import urlfetch

import networkx as nx
import sys
sys.path.insert(0, 'lib')

import webapp2
import cgi
import logging
import urllib

class MainPage(webapp2.RequestHandler):
    def get(self):
		
		
		self.response.write("""<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	<body>
		<form action="/result" method="POST">
			<input type=text name=station_from><br></input>
			<input type=text name=station_to><br></input>
			<input type=submit value=Search></input>
		</form>
	</body>
</html>""")

class ResultPage(webapp2.RequestHandler):

	def post(self):
		station_from = self.request.get("station_from")
		station_to = self.request.get("station_to")
		
		req = urllib.urlopen('http://fantasy-transit.appspot.com/net?format=json')
		js = json.load(req)
	
		G = nx.Graph()
		N = []
		E = []
		for line in js:
			for station in line["Stations"]:
				if station not in N:
					N.append(station)

		for line in js:
			for index in range(len(line["Stations"]) - 1):
				E.append(station[index], station[index + 1])

		G.add_nodes_from(N)
		G.add_edges_from(E)
		

		
		self.response.headers["Content-Type"] = "text/html; charset=utf-8"
		self.response.out.write("""<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	<body>
		""")
		
		self.response.out.write(station_from.encode('utf-8'))
		self.response.out.write(""" から """)
		self.response.out.write(station_to.encode('utf-8'))
		self.response.out.write("""　に行く経路は """)
		self.response.out.write(nx.dijkstra_path(G, station_from, station_to).encode('utf-8'))
		self.response.out.write("""です。
			</body>
			</html>
		""")
		



app = webapp2.WSGIApplication([("/transit", MainPage),
                               ("/result", ResultPage)],
                              debug=True)