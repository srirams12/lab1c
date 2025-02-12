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

import math
import random

class FakeScanPublisher(Node):

    def __init__(self):
        super().__init__('fake_scan_publisher')
        self.publisher_scan = self.create_publisher(LaserScan, 'fake_scan', 10)
        self.publisher_range = self.create_publisher(Float32, 'range_test', 10)

        self.timer_period = 0.05  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        scan = LaserScan()
        # scan.header.stamp = self.get_clock().now()
        scan.header.stamp = rclpy.time.Time().to_msg()
        scan.header.frame_id = 'base_link'
        scan.angle_min = (-2/3) * math.pi
        scan.angle_max = (2/3) * math.pi
        scan.angle_increment = (1/300) * math.pi
        scan.scan_time = self.timer_period
        scan.range_min = 1.0
        scan.range_max = 10.0
        scan.ranges = [random.uniform(1.0, 10.0) for _ in range(401)]




        self.publisher_scan.publish(scan)
        self.get_logger().info('Publishing: "%s"' % scan.ranges[:10])

        range_msg = Float32()
        range_msg.data = 401.0
        self.publisher_range.publish(range_msg)


def main(args=None):
    rclpy.init(args=args)
    fake_scan_publisher = FakeScanPublisher()

    rclpy.spin(fake_scan_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    fake_scan_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()