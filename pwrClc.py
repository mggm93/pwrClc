#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib import cm

import argparse
import numpy as np
import toml

from constants import *
from enviroment import Enviroment
from rider import Rider
from integrator import Integrator

import math

class Application:

  def __init__(self):
    self.enviroment = Enviroment()
    self.rider = None
    self.integrator = Integrator()

  def readInput(self):
    parser = argparse.ArgumentParser(
        prog="pwrClc",
        description="Bike track calculator based on rider profile and gpx track")
    parser.add_argument('inputFile')
    args = parser.parse_args()
    tomlArgs = toml.load(args.inputFile)
    # rider
    riderArgs = tomlArgs["rider"]
    self.rider = Rider(weight=riderArgs["weight"], ftp=riderArgs["ftp"])
    # track
    self.enviroment.setGpxFilePath(tomlArgs["track"]["filePath"])

  def init(self):
    self.enviroment.init()
    self.rider.init()
    self.integrator.setEnviroment(self.enviroment)
    self.integrator.setRider(self.rider)
    self.integrator.init()

  def run(self):
    self.speed, self.power, self.time = self.integrator.getSpeedPowerTime()
    self.kjoule = self.integrator.getEnergy(self.power, self.time) * 0.001

  def printSummay(self):
    t = self.time[-1]
    s = int(t % 60)
    t = t // 60
    m = int(t % 60)
    h = int(t // 60)
    print("Finish time: {}:{}:{}".format(h, m, s))
    def printStats(name, array):
      mina = np.min(array)
      maxa = np.max(array)
      avga = 0.0
      for i in range(1,len(self.time)):
        avga += array[i] * (self.time[i] - self.time[i-1])
      avga /= self.time[-1]
      print("{}: min={:.2f}, max={:.2f}, avg={:.2f}".format(name, mina, maxa, avga))
    printStats("Speed", self.speed * mps2kph)
    printStats("Power", self.power)
    kcal = int(self.kjoule * joule2cal)
    kcalPerHour = math.ceil(kcal / (self.time[-1] / 60**2))
    print("kcal: {:.2f} ".format(kcal))
    print("kcal/h: {:.2f} -> {:.2f} g sugar".format(kcalPerHour, kcalPerHour / kcalPerGSugar))
    print("total : {:.2f}km, {:.2f}hm".format(self.enviroment.totalDistance*.001,\
        self.enviroment.totalHeight))

  def plot(self):
    fig, axs = plt.subplots(2)
    # altitude/speed over distance
    ax = axs[0]
    #
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
    # 3D map
    axs[1].remove()
    axs[1] = fig.add_subplot(2, 1, 2, projection='3d')
    ax = axs[1]
    color = 'gray'
    ax.plot(self.enviroment.lon, self.enviroment.lat, self.enviroment.ele, color=color)
    #
    plt.tight_layout()
    plt.show()

def main():
  app = Application()
  app.readInput()
  app.init()
  app.run()
  app.printSummay()
  app.plot()

if __name__ == '__main__':
  main()
