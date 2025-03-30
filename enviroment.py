import os
import sys

import gpxpy
import gpxpy.gpx

import math
import numpy as np

from scipy.signal import savgol_filter

class Enviroment:
  """
  Class that holds data about the track as well as environment parameters.
  """
  
  def __init__(self):
    # track
    self.gpxFilePath = None
    self.noPoints = 0
    self.lat = None
    self.lon = None
    self.ele = None
    self.segLength = None
    self.distance = None
    self.slope = None
    self.totalDistance = None
    self.totalHeight = None
    self.rho = 1.2

  def setGpxFilePath(self, gpxFilePath):
    self.gpxFilePath = gpxFilePath

  def _readGpxData(self):
    """
    Read gpx track from file give by self.gpxFilePath
    """
    if not os.path.isfile(self.gpxFilePath):
      sys.exit("Not an input file: {}".format(self.gpxFilePath))
    gpxFile = open(self.gpxFilePath, 'r')
    gpx = gpxpy.parse(gpxFile)
    # gpx file type 1
    self.noPoints = 0
    for route in gpx.routes:
      self.noPoints += len(route.points)
    self.lat = np.zeros(self.noPoints)
    self.lon = np.zeros(self.noPoints)
    self.ele = np.zeros(self.noPoints)
    if len(self.lat) != 0:
      i = 0
      for route in gpx.routes:
        for point in route.points:
          self.lat[i] = point.latitude
          self.lon[i] = point.longitude
          self.ele[i] = point.elevation
          i += 1
      return
    # gpx file type 2
    for track in gpx.tracks:
      for segment in track.segments:
        self.noPoints += len(segment.points)
    self.lat = np.zeros(self.noPoints)
    self.lon = np.zeros(self.noPoints)
    self.ele = np.zeros(self.noPoints)
    if len(self.lat) != 0:
      i = 0
      for track in gpx.tracks:
        for segment in track.segments:
          for point in segment.points:
              self.lat[i] = point.latitude
              self.lon[i] = point.longitude
              self.ele[i] = point.elevation
              i += 1

  def _distanceBetweenPoints(self, id2, id1):
    """
    Helper function to calculate distance between two points in gpx track.
    """
    idMin = min(id1, id2)
    idMax = max(id1, id2)
    lat1 = self.lat[idMin]
    lat2 = self.lat[idMax]
    lon1 = self.lon[idMin]
    lon2 = self.lon[idMax]
    ele1 = self.ele[idMin]
    ele2 = self.ele[idMax]
    # from stackoverflow
    R = 6378.137; # Radius of earth in KM
    dLat = lat2 * np.pi / 180.0 - lat1 * np.pi / 180.0
    dLon = lon2 * np.pi / 180.0 - lon1 * np.pi / 180.0
    a = np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180.0) \
        * np.cos(lat2 * np.pi / 180.0) * np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * math.atan2(np.sqrt(a), np.sqrt(1.0-a))
    d = R * c
    distance = d * 1000.0 # meters
    return (distance**2 + (ele2 - ele1)**2)**0.5
    #return distance

  def _smooth(self, x, n=5, window='hanning'):
    if x.size < n:
        raise ValueError("Input vector needs to be larger than window size.")
    if n == 1:  # no need to apply filter
        return x
    if window not in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        msg = "Only possible windows: 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        raise ValueError(msg)

    xadd_left = 2 * x[0] - x[n:0:-1]
    xadd_right = 2 * x[-1] - x[-2:-n - 2:-1]
    x_expanded = np.concatenate((xadd_left, x, xadd_right))

    if window == 'flat':  # moving average
        w = np.ones(n, 'd')
    else:
        w = eval('np.' + window + '(n)')

    y = np.convolve(w / w.sum(), x_expanded, mode='valid')
    istart = int(n / 2) + 1
    return y[istart:istart + len(x)]

  def _postProcessGpxData(self):
    # Calculate segment length
    self.segLength = np.zeros(self.noPoints-1)
    for i in range(0, self.noPoints-1):
      self.segLength[i] = self._distanceBetweenPoints(i+1, i)
    # Calculate segment ele
    self.segEle = np.zeros(self.noPoints-1)
    for i in range(0, self.noPoints-1):
      self.segEle[i] = self.ele[i+1] - self.ele[i]
    # Calculate distance for each point
    self.distance = np.zeros(self.noPoints)
    self.distance[0] = 0.0
    for i in range(1, self.noPoints):
      self.distance[i] = self.distance[i-1] + self.segLength[i-1]
    self.totalDistance = self.distance[-1]
    # Calculate slope for each point
    self.slope = np.zeros(self.noPoints)
    dEle = self.ele[1] - self.ele[0]
    dDis = self.distance[1] - self.distance[0]
    self.slope[0]  = math.asin( dEle / dDis )
    dEle = self.ele[-1] - self.ele[-2]
    dDis = self.distance[-1] - self.distance[-2]
    self.slope[-1]  = math.asin( dEle / dDis )
    for i in range(1, self.noPoints-1):
      dEle = self.ele[i+1] - self.ele[i-1]
      dDis = self.distance[i+1] - self.distance[i-1]
      self.slope[i]  = math.asin( dEle / dDis )

    # calculate total height
    self.totalHeight = 0.0
    for i in range(1, self.noPoints):
      deltaEle = self.ele[i] - self.ele[i-1]
      if deltaEle > 0.0:
        self.totalHeight += deltaEle

  def init(self):
    self._readGpxData()
    self._postProcessGpxData()
