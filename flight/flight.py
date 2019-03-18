#!/usr/bin/python
# importing
import math, rospy
from tqdm import tqdm
from clever import srv
from aerosol import Aerosol
# from neopixel import *
from std_srvs.srv import Trigger
from mavros_msgs.srv import SetMode
from mavros_msgs.srv import CommandBool

class Flight:
    def __init__(self):
        # proxy init
	self.set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
        self.navigate = rospy.ServiceProxy('/navigate', srv.Navigate)
        self.set_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        self.arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        self.get_telemetry = rospy.ServiceProxy('/get_telemetry', srv.GetTelemetry)
        self.set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
        self.set_rates = rospy.ServiceProxy('/set_rates', srv.SetRates)
        self.frame_id = 'aruco_map'
        # z speed check
        if abs(self.get_telemetry("aruco_map").vz) > 1:
            print "show aruco's and run the script again"
            exit()
        print "init done"

    def take_off(self):
        print "take off begin"
        zp = 1
        self.navigate(z=zp, speed=1, frame_id='fcu_horiz', auto_arm=True)
        self.sleep(1.2)

    def get_distance(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def get_to(self, xp, yp, zp, sp=0.3, yaw=0, yaw_rate=0, auto_arm=False, tol=0.45, freq=10):
        print "navigate to:", xp, yp, zp
        print self.navigate(frame_id='aruco_map', x=xp, y=yp, z=zp, speed=sp, yaw=yaw, yaw_rate=yaw_rate, update_frame=True)
        print "waiting for right tolerance"
        while True:
            telem = self.get_telemetry(frame_id='aruco_map')
            distance = self.get_distance(xp, yp, zp, telem.x, telem.y, telem.z)
            print distance
            if distance < tol:
                print("I am at x :" + str(xp) + "  y :" + str(yp) + "  z :" + str(zp))
                break
            self.sleep(1/freq, show=False)

    def set_to(self, x, y, z, distance, delay_ratio, yaw=0):
        print self.set_position(x=x, y=y, z=z, frame_id='aruco_map', yaw=1.57)
        self.sleep(distance * delay_ratio, show=False)


	print self.set_attitude(yaw=1.57)
        # trying to draw a path
        # try:
        for i in tqdm(range(1, len(coordinates))):
            spray = coordinates[i]["spray"]
            if can.value != spray:
                can.spray(spray)
            self.set_to(coordinates[i]["x"], y, coordinates[i]["y"],
                        self.get_distance(coordinates[i]["x"], y, coordinates[i]["y"], coordinates[i-1]["x"], y, coordinates[i-1]["y"]),
                        delay_ratio, yaw=self.wall_yaw)
        # save last point if flight is interrupted


        # landing
        self.land()

    def sleep(self, time, show=True):
        if show:
            print "sleeping for:", time
        rospy.sleep(time)

    def land(self):
        print "Landing..."
        self.set_mode(base_mode=0, custom_mode='AUTO.LAND')
