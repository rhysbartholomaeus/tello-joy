import socket
import threading
import time

import cv2

# Modified from: https://github.com/dji-sdk/Tello-Python/blob/master/Single_Tello_Test/tello.py

# Telemetry modified from: https://github.com/dbaldwin/DroneBlocks-Tello-Camera-With-Python-OpenCV/blob/master/lib/telemetry.py

class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.socket.bind((self.local_ip, self.local_port))

        # Thread to manage return status
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)

        self.MAX_TIME_OUT = 15.0

        self.telemetry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.telemetry_address = ('', 8890)
        self.telemetry_data = ""

        # From SDK User Guide - Page 6
        self.telemetry_indices = {
            "pitch": 0,
            "roll": 1,
            "yaw": 2,
            "altitude": 9,
            "battery": 10,
            "baro": 11
        }

        self.frame_size = (480, 360)
        self.video_size = (960, 720)
        self.video_capture = None

        self.battery_level = None
        self.pitch = None
        self.roll = None
        self.yaw = None
        self.altitude = None
        self.baro = None

        self.commanded_alt = None

    def send_command(self, command):
        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print("Sending command: " + command)

    def _receive_thread(self):
        """Listen to responses from the Tello.
        Runs as a thread, sets self.response to whatever the Tello last returned.
        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

               #self.log[-1].add_response(self.response)
            except socket.error as exc:
                print ("Caught exception socket.error : %s" % exc)

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log

    def get_video(self):
      self.video_capture = cv2.VideoCapture('udp://0.0.0.0:11111')
      _, frame = self.video_capture.read()

    # Get the image frame
    def get_frame(self):
      _, self.frame = self.video_capture.read()
      frame = cv2.resize(self.frame, self.video_size)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      #_, jpeg = cv2.imencode('image.jpg', frame)
      overlay = frame.copy()
      output = frame.copy()
      alpha = 0.75
      cv2.putText(overlay, "DRONE CAM01",(10, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.putText(overlay, "PITCH: {}".format(self.pitch),(10, 610), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.putText(overlay, "YAW: {}".format(self.yaw),(200, 610), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.putText(overlay, "ALT: {}".format(self.altitude),(10, 650), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.putText(overlay, "ALT (B): {}".format(self.altitude),(230, 650), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.putText(overlay, "BAT: {}%".format(self.battery_level),(10, 690), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), 1)
      cv2.addWeighted(overlay, alpha, output, 1 - alpha,0, output)
      return output

    def receive_telemetry(self):
      self.telemetry_socket.bind(self.telemetry_address)

      def recv():
          while True:
              try:
                  response, _ = self.telemetry_socket.recvfrom(256)
                  response = response.decode(encoding="utf-8")
                  self.parse_telemetry(response)                
              except Exception as e:
                  print("Error receiving: " + str(e))
                  break
      thread = threading.Thread(target=recv)
      thread.setDaemon(True)
      thread.start()

    def parse_telemetry(self, data):
      if(data != None or data != ""):
        data = data.split(";")
        self.pitch = data[self.telemetry_indices["pitch"]].split(":")[1]
        self.roll = data[self.telemetry_indices["roll"]].split(":")[1]
        self.yaw = data[self.telemetry_indices["yaw"]].split(":")[1]
        self.altitude = data[self.telemetry_indices["altitude"]].split(":")[1]
        self.battery_level = data[self.telemetry_indices["battery"]].split(":")[1]
        self.baro = data[self.telemetry_indices["baro"]].split(":")[1]

    # Clean-up
    def __del__(self):
      self.telemetry_socket.close()
      if self.video_capture:
          self.video_capture.release()