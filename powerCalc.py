#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np

from constants import *
from enviroment import Enviroment
from rider import Rider
from integrator import Integrator

import math

class Application:

  def __init__(self):
    self.enviroment = Enviroment()
    self.rider = Rider()
    self.integrator = Integrator()

  def setInput(self):
    self.enviroment.setGpxFilePath("input/OetztalRadmarathon.gpx")
    self.rider.setWeigth(78.0+10.0)
    self.rider.setFtp(280)

  def init(self):
    self.enviroment.init()
    self.rider.init()
    self.integrator.setEnviroment(self.enviroment)
    self.integrator.setRider(self.rider)
    self.integrator.init()

  def run(self):
    self.speed, self.power = self.integrator.getSpeedAndPower()
    self.time = np.zeros_like(self.speed)
    for i in range(1, len(self.time)):
      self.time[i] = self.time[i-1] + self.enviroment.segLength[i-1] / self.speed[i]
    t = self.time[i-1]
    s = int(t % 60)
    t = t // 60
    m = int(t % 60)
    h = int(t // 60)
    print("Finish time: {}:{}:{}".format(h, m, s))

  def plot(self):
    fig, axs = plt.subplots(1)
    #
    #ax = axs[0]
    ax = axs
    ax.set_title("distance = {}km, height = {}hm".format(\
        int(self.enviroment.distance[-1]*0.001), int(self.enviroment.totalHeight)))
    color = 'gray'
    ax.set_xlabel('distance [km]', color=color)
    ax.set_ylabel('elevation [m]', color=color)
    ax.tick_params(labelcolor=color)
    ax.plot(self.enviroment.distance*0.001, self.enviroment.ele, color=color)
    #
    ax2 = ax.twinx()
    color = 'red'
    ax2.set_xlabel('distance [km]', color=color)
    ax2.set_ylabel('speed [kph]', color=color)
    ax2.tick_params(labelcolor=color)
    ax2.plot(self.enviroment.distance*m2km, self.speed*mps2kph, color=color)
    #
    plt.show()

def main():
  app = Application()
  app.setInput()
  app.init()
  app.run()
  app.plot()

if __name__ == '__main__':
  main()
