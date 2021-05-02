import pygame

TARGET_JOYSTICK = "Logitech Extreme 3D Pro USB"

class Joystick:
  def __init__(self):
      self.joystick = None
      self.initalised = False

  def initJoystick(self):
      pygame.joystick.init()
      joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

      for device in joysticks:
        if (device.get_name() == TARGET_JOYSTICK):
          print ("Found " + TARGET_JOYSTICK)
          self.joystick = device
          self.initalised = True
      if(not self.initalised):
        print ("Could not find " + TARGET_JOYSTICK +". Is it connected?")
  def getDevice(self):
    return self.joystick