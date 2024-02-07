import numpy as np
from scipy import optimize

from enviroment import Enviroment
from rider import Rider

from constants import *

class StrategyBase:
  def __init__(self, rider):
    self.power = rider.ftp * 0.8
    self.maxSpeed = 60.0 * kph2mps
  def getPower(self, speed = 0.0, slope = 0.0):
    if speed > self.maxSpeed or slope * rad2grad < -5.0:
      return 0.0
    else:
      return self.power
  def clipSpeed(self, speed):
    return min(self.maxSpeed, speed)

class Integrator:
  """
  Class to perform relevant integrations.
  """

  def __init__(self):
    self.enviroment = None
    self.rider = None
    self.strategy = None

  def setEnviroment(self, enviroment):
    self.enviroment = enviroment

  def setRider(self, rider):
    self.rider = rider

  def init(self):
    self.strategy = StrategyBase(self.rider)

  def getSpeedAndPower(self):
    if self.rider == None or self.enviroment == None:
      sys.exit("Integrator needs rider and enviroment !")
    noPoints = self.enviroment.noPoints
    speed = np.zeros(noPoints)
    power = np.zeros(noPoints)
    power[0] = self.strategy.getPower()
    dx = 1.0 # meter
    for i in range(1, noPoints):
      segId = i - 1
      segLength = self.enviroment.segLength[segId]
      slope = self.enviroment.slope[segId]
      noSubSteps = max(1, math.ceil(segLength / dx))
      dx_ = segLength / noSubSteps
      speed_ = speed[i-1]
      speed[i] = 0.0
      power[i] = 0.0
      dt = 0.0
      for j in range(noSubSteps):
        power_ = self.strategy.getPower(speed_, slope)
        F_power = power_/max(0.01, speed_)
        F_gravity = - self.rider.weight * g * math.sin(slope)
        F_drag = - 0.5 * self.enviroment.rho * self.rider.cd * self.rider.aref * speed_**2.0
        F_res = F_power + F_drag + F_gravity
        acc = F_res / self.rider.weight
        sign = lambda x: (1, -1)[x<0]
        speed_ = self.strategy.clipSpeed(speed_ + sign(acc) * (abs(acc) * dx_)**0.5)
        dt_ = dx_ / speed_
        dt += dt_
        speed[i] += speed_ * dt_
        power[i] += power_ * dt_
      speed[i] /= dt
      power[i] /= dt
    return speed, power
