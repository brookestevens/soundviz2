import time
import random
import json
import datetime
import sys
from aubio import pvoc, source, float_type
from numpy import zeros, log10, vstack
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint

#web server docs
#https://www.apptic.me/blog/getting-started-with-websockets-in-tornado.php

#the audio thing

def get_spectrogram(filename, samplerate = 0):
  print("here")
  win_s = 512                                        # fft window size
  hop_s = win_s // 2                                 # hop size
  fft_s = win_s // 2 + 1                             # spectrum bins

  a = source(filename, samplerate, hop_s)            # source file
  if samplerate == 0: samplerate = a.samplerate
  pv = pvoc(win_s, hop_s)                            # phase vocoder
  specgram = zeros([0, fft_s], dtype=float_type)     # numpy array to store spectrogram

  # analysis
  while True:
      samples, read = a()                              # read file
      specgram = vstack((specgram,pv(samples).norm))   # store new norm vector
      if read < a.hop_size: break

  time_step = hop_s / float(samplerate)

  def get_rounded_ticks( top_pos, step, n_ticks ):
      top_label = top_pos * step
      # get the first label
      ticks_first_label = top_pos * step / n_ticks
      # round to the closest .1
      ticks_first_label = round ( ticks_first_label * 10. ) / 10.
      # compute all labels from the first rounded one
      ticks_labels = [ ticks_first_label * n for n in range(n_ticks) ] + [ top_label ]
      # get the corresponding positions
      ticks_positions = [ ticks_labels[n] / step for n in range(n_ticks) ] + [ top_pos ]
      # convert to string
      ticks_labels = [  "%.1f" % x for x in ticks_labels ]
      # return position, label tuple to use with x/yticks
      return ticks_positions, ticks_labels
  
  print(get_rounded_ticks ( len(specgram), time_step, 10 ))
  #x_ticks, x_labels = get_rounded_ticks ( len(specgram), time_step, n_xticks )
  #y_ticks, y_labels = get_rounded_ticks ( len(specgram[0]), (samplerate / 1000. / 2.) / len(specgram[0]), n_yticks )

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

  # Function to send data
  def send_data(self):
    get_spectrogram(sys.argv[1], 256)

    # init the sound visualizer here
    # sys.argv[1] -> song file
    # for(i in song smaple){
    #   analyze stuff
    #   self.send_data
    # }

    for i in range(100):
      # point_data = {
      #   'vol': random.randrange(0,255),
      #   'freq' : random.randrange(0,255),
      # }
      point_data = {'spectrum' : get_spectrogram(sys.argv[1], 256)}
      self.write_message(json.dumps(point_data))
      self.send_data
      time.sleep(1)

    #write the json object to the socket
    #self.write_message(json.dumps(point_data))

    #create new ioloop instance to intermittently publish data
    #ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data)

#serve the index file
class MainHandler(web.RequestHandler):
  def get(self):
    self.render("public/index.html")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: %s <filename>" % sys.argv[0])
    sys.exit()
  else:
    #create new web app w/ websocket endpoint available at /websocket
    print ("App is listening on port 8001!")
    application = web.Application([
      (r"/", MainHandler),
      (r"/websocket", WebSocketHandler),
      (r"/public/(.*)", web.StaticFileHandler, {"path":"./public"}) #serve static dir
    ], autoreload=True)
    application.listen(8001)
    ioloop.IOLoop.instance().start()
