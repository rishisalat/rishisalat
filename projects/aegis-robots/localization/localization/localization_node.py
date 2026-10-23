#!/usr/bin/env python3

import rclpy
from geometry_msgs.msg import Pose, PoseStamped
from rclpy.node import Node


class LocalizationNode(Node):
    def __init__(self):
        super().__init__("localization_node")

        self.pose_sub = self.create_subscription(
            PoseStamped,
            "/pose_modelcars",
            self.pose_modelcars_callback,
            10,
        )

        self.robot_pose_pub = self.create_publisher(Pose, "/robot_pose", 10)

        self.get_logger().info("Localization node started")

    def pose_modelcars_callback(self, msg: PoseStamped):
        self.robot_pose_pub.publish(msg.pose)


def main(args=None):  # pragma: no cover
    rclpy.init(args=args)
    node = LocalizationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
