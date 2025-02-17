# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from sensor_msgs.msg import LaserScan
from custom_msgs.msg import OpenSpace

import math
import random

class OpenSpacePublisher(Node):

    def __init__(self):
        super().__init__('open_space_publisher')
        # self.publisher_dist = self.create_publisher(Float32, 'open_space/distance', 10)
        # self.publisher_ang = self.create_publisher(Float32, 'open_space/angle', 10)

        self.declare_parameters(
            namespace='',
            parameters=[
                ('pub_name', "open_space"),
                ('sub_name', "fake_scan")
            ]
        )
    
        self.publisher_os = self.create_publisher(OpenSpace, self.get_parameter('pub_name').value, 10)

        self.subscription = self.create_subscription(
            LaserScan,
            self.get_parameter('sub_name').value,
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.ranges[:10])

        open_space_msg = OpenSpace()

        open_space_msg.distance = max(msg.ranges)
        open_space_msg.angle = msg.ranges.index(max(msg.ranges)) * msg.angle_increment + msg.angle_min
        
        self.publisher_os.publish(open_space_msg)

        self.get_logger().info('Publishing: "%s"' % open_space_msg.distance)
        self.get_logger().info('Publishing: "%s"' % open_space_msg.angle)

def main(args=None):
    rclpy.init(args=args)
    open_space_publisher = OpenSpacePublisher()

    rclpy.spin(open_space_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    open_space_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()