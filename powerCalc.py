#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import cm

from enviroment import Enviroment

class Application:

  def __init__(self):
    # track
    self.enviroment = Enviroment()
    # rider
    self.riderWeigthBody = None
    self.riderWeigthBike = None
    self.riderWeigth = None

  def setInput(self):
    # track
    self.enviroment.setGpxFilePath("input/OetztalRadmarathon.gpx")
    # rider
    self.riderWeigthBody = 77.1
    self.riderWeigthBike = 10.0

  def initRider(self):
    self.riderWeigth = self.riderWeigthBody + self.riderWeigthBike 
    pass

  def init(self):
    # track
    self.enviroment.init()

  def plot(self):
    fig, axs = plt.subplots(2)
    #
    ax = axs[0]
    #ax.set_xlim(20, 130)
    ax.set_title("distance = {}km, height = {}hm".format(\
        int(self.enviroment.distance[-1]*0.001), int(self.enviroment.totalHeight)))
    ax.plot(self.enviroment.distance*0.001, self.enviroment.ele)
    #
    ax = axs[1]
    #ax.set_xlim(20, 130)
    ax.plot(self.enviroment.distance*0.001, self.enviroment.slope)
    #
    #ax = axs[2]
    #ax.set_xlim(20, 130)
    #height = np.zeros(self.noPoints)
    #height[0] = self.ele[0]
    #for i in range(1, self.noPoints):
    #  height[i] = height[i-1] + self.slope[i-1] * (self.distance[i] - self.distance[i-1])
    #ax.plot(self.distance*0.001, height)
    #
    plt.show()

def main():
  app = Application()
  app.setInput()
  app.init()
  app.plot()

if __name__ == '__main__':
  main()
