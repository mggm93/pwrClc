class Rider:
  """
  Class that holds attributes of the rider such as weigth, power curves, and more.
  """

  def __init__(self):
    self.weight = None
    self.ftp = None
    self.cd = 0.5 # 0.4 - 0.6
    self.aref = 1.0

  def setFtp(self, ftp):
    self.ftp = ftp

  def setWeigth(self, weigth):
    self.weight = weigth

  def init(self):
    pass
