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
        super().__init__('fake_scan_publisher', allow_undeclared_parameters=True,
                         automatically_declare_parameters_from_overrides=True)

        self.declare_parameters(
            namespace='',
            parameters=[
                ('topic_name', "fake_scan"),
                ('publish_rate', 20.0),
                ('angle_min', (-2/3) * math.pi),
                ('angle_max', (2/3) * math.pi),
                ('range_min', 1.0),
                ('range_max', 10.0),
                ('angle_increment', (1/300) * math.pi),

            ]
        )

        self.publisher_scan = self.create_publisher(LaserScan, self.get_parameter('topic_name').value, 10)
        self.publisher_range = self.create_publisher(Float32, 'range_test', 10)

        self.timer_period = 1.0 / self.get_parameter('publish_rate').value  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        scan = LaserScan()
        # scan.header.stamp = self.get_clock().now()
        scan.header.stamp = rclpy.time.Time().to_msg()
        scan.header.frame_id = 'base_link'
        scan.angle_min = self.get_parameter('angle_min').value
        scan.angle_max = self.get_parameter('angle_max').value
        scan.angle_increment = self.get_parameter('angle_increment').value
        scan.scan_time = self.timer_period
        scan.range_min = self.get_parameter('range_min').value
        scan.range_max = self.get_parameter('range_max').value
        num_scans = int((scan.range_max - scan.range_min) / scan.angle_increment) + 1
        scan.ranges = [random.uniform(scan.range_min, scan.range_max) for _ in range(num_scans)]




        self.publisher_scan.publish(scan)
        self.get_logger().info('Publishing: "%s"' % scan.ranges[:10])

        range_msg = Float32()
        range_msg.data = float(num_scans)
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