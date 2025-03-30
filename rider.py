import sys

class Rider:
  """
  Class that holds attributes of the rider such as weigth, power curves, and more.
  """

  def __init__(self, riderArgs):
    def readProp(propName, defaultValue = None):
      global isPropMissing
      val = defaultValue
      if propName in riderArgs:
        val = riderArgs[propName]
      if val == None:
        isPropMissing = True
        print("Rider property '{}' is missing.".format(propName))
      return val
    global isPropMissing
    isPropMissing = False

    self.weight = readProp("weight")
    self.ftp = readProp("ftp")
    self.cd = readProp("cd", 0.4)
    self.aref = readProp("aref", 1.0)

    if isPropMissing:
      sys.exit("Missing rider properties")

  def init(self):
    # TODO: calc aref from weight ?
    pass
