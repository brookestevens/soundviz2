import time
import random
import json
import datetime
import aubio
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint

#install pip
#install packages with pipenv install <name>
#start app with pipenv shell
#python server.py

#https://www.apptic.me/blog/getting-started-with-websockets-in-tornado.php

class WebSocketHandler(websocket.WebSocketHandler):
  #avoid 403 error, but specify sites for security
  # def check_origin(self, origin):
  #   allowed = ["http://localhost:3000"]
  #   if origin in allowed:
  #       print("allowed", origin)
  #       return True
  
  # on open of this socket
  def open(self):
    print ('Connection established.')
    #ioloop to wait for 3 seconds before starting to send data
    ioloop.IOLoop.instance().add_timeout(datetime.
    timedelta(seconds=3), self.send_data)

  # close connection
  def on_close(self):
    print ('Connection closed.')

  # websocket does not recieve data  

  # Our function to send new (random) data for charts
  def send_data(self):
    print ("Sending Data")
    #create a bunch of random data for various dimensions we want
    vol = random.randrange(0,255)
    freq = random.randrange(0,255)

    #create a new data point
    point_data = {
    	'vol': vol,
    	'freq' : freq,
    }
    #write the json object to the socket
    self.write_message(json.dumps(point_data))

    #create new ioloop instance to intermittently publish data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data)

#serve the index file
class MainHandler(web.RequestHandler):
  def get(self):
    self.render("public/index.html")

if __name__ == "__main__":
  #create new web app w/ websocket endpoint available at /websocket
  print ("App is listening on port 8001!")
  application = web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/public/(.*)", web.StaticFileHandler, {"path":"./public"}) #serve static dir
  ], autoreload=True)
  application.listen(8001)
  ioloop.IOLoop.instance().start()
