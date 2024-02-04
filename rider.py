class Rider:
  """
  Class that holds attributes of the rider such as weigth, power curves, and more.
  """

  def __init__(self):
    self.bodyWeight = None
    self.ftp = None

  def setFtp(self, ftp):
    self.ftp = ftp

  def setWeigth(self, weigth):
    self.bodyWeight = weigth

  def init(self):
    pass
