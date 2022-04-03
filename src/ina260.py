#!/usr/bin/env python
# coding: UTF-8

from __future__ import print_function

import serial
import rospy
import roslib
import numpy as np
import datetime
import csv
import time

import struct


from std_msgs.msg import Float32

if __name__ == '__main__':
    try:
        rospy.init_node('ina260', anonymous=True)
        r = rospy.Rate(10)  
        ina_current = rospy.Publisher(
            "current", Float32, queue_size=10)
        ina_voltage = rospy.Publisher(
            "voltage", Float32, queue_size=10)

        # timeoutを秒で設定（default:None)ボーレートはデフォルトで9600
        ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=3)

        rec_count = 0
        rec_data = [0]*4
        rec_flag = 0


        while not rospy.is_shutdown():
            line = ser.read()  # 行終端'¥n'までリードする
            
            # tmp = int.from_bytes(line, byteorder='big')
            # tmp = struct.unpack('>HH', line)
            tmp = np.frombuffer(line, dtype=np.uint8)
            tmp = int(tmp)
            #print(tmp)
            if   tmp == 118:#asciiのv
                 rec_flag = 'v'
            elif tmp == 105:
                 rec_flag = 'i'
            elif rec_flag == 'v':
                rec_data[rec_count] = tmp
                #print(tmp)
                #print(rec_count)
                rec_count += 1
                if rec_count == 4:
                    rec_flag = 0
                    rec_count = 0

                    voltage = int(rec_data[0] | rec_data[1] << 8 | rec_data[2] << 16 | rec_data[3] << 24)
                    if rec_data[3] >= 8: #正負判定
                        voltage = -(voltage ^ 0xffffffff)

                    voltage = float(voltage) / 1000
                    
                    print("v")
                    print(voltage)

                    data1 = Float32()
                    data1.data = voltage
                    ina_voltage.publish(data1)
            elif rec_flag == 'i':
                rec_data[rec_count] = tmp
                #print(tmp)
                #print(rec_count)
                rec_count += 1
                if rec_count == 4:
                    rec_flag = 0
                    rec_count = 0

                    current = int(rec_data[0] | rec_data[1] << 8 | rec_data[2] << 16 | rec_data[3] << 24)

                    if rec_data[3] >= 8: #正負判定
                        current = -(current ^ 0xffffffff)

                    current = float(current) / 1000
                        
                    print("i")
                    print(current)

                    data2 = Float32()
                    data2.data = current
                    ina_current.publish(data2)

    except rospy.ROSInterruptException:
        ser.close()
        pass
