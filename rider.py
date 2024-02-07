class Rider:
  """
  Class that holds attributes of the rider such as weigth, power curves, and more.
  """

  def __init__(self, weight, ftp, cd=0.4, aref=1.0):
    self.weight = weight
    self.ftp = ftp
    self.cd = cd
    self.aref = aref

  def init(self):
    # TODO: calc aref from weight ?
    pass
