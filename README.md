# Tello-Joy
This is a small application that utilizes pygame and opencv-python to allow Tello Drone operators to control the Wifi-based drone using a joystick. In this instance its hardcoded to the Logitech Extreme 3D Pro.

Project is very WIP and more or less here as something to do / tinker with and not intended to be used in any official capacity. 

## Requirements

- Tested on Python 3.9.4
- opencv-python (4.5.1.48)
- pygame (2.0.1)

## Usage

**Notes**: The trigger on the Extreme 3D Pro is used to issue the `LAND` command. The secondary trigger on the stick issues the `TAKE-OFF` command and the throttle slider controls the altitude. Set the altitude to the middle or upper position prior to attempting to take off or the drone simply won't respond. 

1. Plug in your joystick (It's hardcoded to the Logitech Extreme 3D Pro USB at the moment - adjust in joystick.py as necessary)
2. Turn the drone on and connect your PC to your drone's Wifi network
3. Start the application `python app.py`
4. Wait for the video feed to start
5. Use the secondary trigger to launch the drone. 

## Issues

Video feed is delayed between 250-500ms. 

## TODO

- See if video feed can be improved to reduce delay
- Add a HUD
- Add reset method for emergency mode


