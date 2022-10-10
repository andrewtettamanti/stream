#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import uhd
import numpy as np
import rospy
from geometry_msgs.msg import PoseStamped

pose_x = None
pose_y = None


# ROS Stuff
def callback(data):
    pose_x = data.pose.position.x
    pose_y = data.pose.position.y
    

TOPIC="/car/car_pose"
rospy.init_node('listener', anonymous=True)
rospy.Subscriber(TOPIC, PoseStamped, callback)



usrp = uhd.usrp.MultiUSRP()
num_samps = 10000 # number of samples received
center_freq = 770e6 # Hz
sample_rate = 50e6 # Hz
gain = 50 # dB

usrp.set_rx_rate(sample_rate, 0)
usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
usrp.set_rx_gain(gain, 0)

# Set up the stream and receive buffer
st_args = uhd.usrp.StreamArgs("fc32", "sc16")
st_args.channels = [0]
metadata = uhd.types.RXMetadata()
streamer = usrp.get_rx_stream(st_args)
recv_buffer = np.zeros(streamer.get_max_num_samps, dtype=np.complex64)
#recv_buffer = np.zeros((1, 1000), dtype=np.complex64)

# Start Stream

stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
stream_cmd.stream_now = True
streamer.issue_stream_cmd(stream_cmd)

samples = []
x_pose=[]
y_pose=[]

while pose_X==True:
    streamer.recv(recv_buffer, metadata)
    samples.append(recv_buffer[0])
    x_pose.append(pose_x)
    y_pose.append(pose_y)

# Stop Stream
stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
streamer.issue_stream_cmd(stream_cmd)
samples=np.array(samples)
x_pose=np.array(x_pose)
y_pose=np.array(y_pose)

np.savez('stream.npz', name1=samples, name2=x_pose,name3=y_pose)

