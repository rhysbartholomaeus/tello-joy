import pygame

import threading 
import socket
import sys
import time

from tellodrone import Tello
from joystick import Joystick

DEBOUNCE = 0.11

# Axis 0 = Left / Right
# Axis 1 = Forward / Back
# Axis 2 = Rotation
# Axis 3 = Up / Down

joystick = None

# Setup the joystick
# TODO: Add error condition to exit program if it can't find the stick
# def init_joystick():
#   pygame.init()
#   pygame.joystick.init()
#   joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#   for device in joysticks:
#     if (device.get_name() == TARGET_JOYSTICK):
#       print ("Found the Logitech Extreme 3D Pro")
#       global joystick 
#       joystick = device
#     else:
#       exit(1)

def main():
  print("Initialising joystick...")
  joystick = Joystick()
  joystick.initJoystick()
  if (joystick.initalised):
    print("Setting up pygame window...")
    pygame.init()
    
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    screen.fill([0, 0, 0])
    noConnImage = pygame.image.load(r'.\No_Connection_Error.png')
    screen.blit(noConnImage, (0,0))
    print("Initialising connection to drone...")
    drone = Tello()
    # Send command message to initiate the drone
    drone.send_command("command")
    # Enable the stream
    drone.send_command("streamon")
    drone.receive_telemetry()

    stabilized = True
    takeoff = False
    
    startTime = time.time()

    # Start video capture
    drone.get_video()

    while True: 
      drone_feed = pygame.surfarray.make_surface(drone.get_frame())
      #Rotate image - Issue with OpenCV
      drone_feed = pygame.transform.rotate(drone_feed,270)
      drone_feed = pygame.transform.flip(drone_feed, True, False)
      screen.blit(drone_feed, (0,0))
      
      currentTime = time.time()
      eventType = None
      axisX = None # Axis 0 = X
      axisY = None # Axis 1 = Y 
      axisZ = None # Axis 2 = Rotational Z
      height = None # Axis 3 = Height
      for event in pygame.event.get():
        axisX = joystick.getDevice().get_axis(0)
        axisY = joystick.getDevice().get_axis(1)
        axisZ = joystick.getDevice().get_axis(2)
        height = joystick.getDevice().get_axis(3)
        try:
          if(axisX != None or axisY != None or axisZ != None):
            if(axisX == None):
              axisX = 0
            if(axisY == None):
              axisY = 0  
            if(axisZ == None):
              height = 0 
            if((currentTime-startTime) >= DEBOUNCE):
              startTime = time.time()
              print("rc " + str(int(axisX*100)) + " " + str(int(-1*axisY*100)) + " " + str(int(-1*height*100)) + " " + str(int(axisZ*100)))
              drone.send_command("rc " + str(int(axisX*100)) + " " + str(int(-1*axisY*100)) + " " + str(int(-1*height*100)) + " " + str(int(axisZ*100)))
              stabilized = False
          else:
            if(not stabilized):
              drone.send_command("rc 0 0 0 0")
              stabilized = True
          if (joystick.getDevice().get_button(0) == 1):
            print("LAND")
            drone.send_command("land")
          if (joystick.getDevice().get_button(1) == 1):
            print("TAKEOFF")
            drone.send_command("takeoff")
            
        except KeyboardInterrupt:
            # print ('\n . . .\n')
            drone.send_command("land")
            break
      pygame.display.update()
  else:
    print('Joystick failed to initalise... Exiting...')
    exit(1)

if __name__ == "__main__":
    main()
    print("Exiting application...")
    pygame.quit()
    exit(0)