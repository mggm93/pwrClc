#!/usr/bin/env python3

import gpxpy
import gpxpy.gpx

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm

class Application:

  def __init__(self):
    # track
    self.gpxFilePath = None
    self.noPoints = 0
    self.lati = None
    self.long = None
    self.elev = None
    self.distance = None
    self.slope = None
    # rider
    self.riderWeigthBody = None
    self.riderWeigthBike = None
    self.riderWeigth = None

  def setInput(self):
    # track
    self.gpxFilePath = "input/OetztalRadmarathon.gpx"
    # rider
    self.riderWeigthBody = 77.1
    self.riderWeigthBike = 10.0

  def initRider(self):
    self.riderWeigth = self.riderWeigthBody + self.riderWeigthBike 
    pass

  def readGpxData(self):
    #---check file size
    gpxFile = open(self.gpxFilePath, 'r')
    gpx = gpxpy.parse(gpxFile)
    # gpx file type 1
    for route in gpx.routes:
      self.noPoints += len(route.points)
    self.lati = np.zeros(self.noPoints)
    self.long = np.zeros(self.noPoints)
    self.elev = np.zeros(self.noPoints)
    if len(self.lati) != 0:
      i = 0
      for route in gpx.routes:
        for point in route.points:
          self.lati[i] = point.latitude
          self.long[i] = point.longitude
          self.elev[i] = point.elevation
          i += 1
      return
    # gpx file type 2
    for track in gpx.tracks:
      for segment in track.segments:
        self.noPoints += len(segment.points)
    self.lati = np.zeros(self.noPoints)
    self.long = np.zeros(self.noPoints)
    self.elev = np.zeros(self.noPoints)
    if len(self.lati) != 0:
      i = 0
      for track in gpx.tracks:
        for segment in track.segments:
          for point in segment.points:
              self.lati[i] = point.latitude
              self.long[i] = point.longitude
              self.elev[i] = point.elevation
              i += 1
  def _distanceBetweenPoints(self, id1, id2):
    distance = 0.0
    minId = min(id1, id2)
    maxId = max(id1, id2)
    for i in range(minId, maxId):
      x0 = self.lati[i]
      y0 = self.long[i]
      z0 = 0.0 #self.elev[i]
      x1 = self.lati[i+1]
      y1 = self.long[i+1]
      z1 = 0.0 #self.elev[i+1]
      distance_ = ( (x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2 )**0.5
      distance += distance_
    return distance

  def postProcessGpxData(self):
    # Calculate distance for each point
    self.distance = np.zeros(self.noPoints)
    self.distance[0] = 0.0
    for i in range(1, self.noPoints):
      self.distance[i] = self.distance[i-1] + self._distanceBetweenPoints(i, i-1)
    # Calculate slope for each point
    self.slope = np.zeros(self.noPoints)

  def plot(self):
    fig, axs = plt.subplots(2)
    #
    ax = axs[0]
    ax.set_title("total distance = {}".format(self.distance[-1]))
    ax.plot(self.distance, self.elev)
    #
    ax = axs[1]
    ax.plot(self.lati, self.long)
    #
    plt.show()

def main():
  app = Application()
  app.setInput()
  app.readGpxData()
  app.postProcessGpxData()
  app.plot()

if __name__ == '__main__':
  main()
