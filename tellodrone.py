import socket
import threading
import time

import cv2

# Modified from: https://github.com/dji-sdk/Tello-Python/blob/master/Single_Tello_Test/tello.py

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

        self.frame_size = (480, 360)
        self.video_size = (960, 720)
        self.video_capture = None

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
      
      return frame

    
    def __del__(self):
      if self.video_capture:
          self.video_capture.release()