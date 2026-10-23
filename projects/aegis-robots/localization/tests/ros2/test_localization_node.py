"""Integration test for LocalizationNode.

Spins up the real node and drives it through a publisher/subscriber pair,
verifying that a pose received on /pose_modelcars is republished on
/robot_pose as described in the system architecture.
"""

import rclpy
from geometry_msgs.msg import Pose, PoseStamped

from localization.localization_node import LocalizationNode


def _spin_until(node, condition, timeout_sec=2.0):
    end_time = node.get_clock().now().nanoseconds + int(timeout_sec * 1e9)
    while not condition() and node.get_clock().now().nanoseconds < end_time:
        rclpy.spin_once(node, timeout_sec=0.1)


def test_localization_node_starts_and_names_correctly():
    node = LocalizationNode()
    assert node.get_name() == "localization_node"
    node.destroy_node()


def test_localization_node_republishes_pose_modelcars_as_robot_pose():
    node = LocalizationNode()
    received: list[Pose] = []

    node.create_subscription(
        Pose,
        "/robot_pose",
        lambda msg: received.append(msg),
        10,
    )
    pose_modelcars_pub = node.create_publisher(PoseStamped, "/pose_modelcars", 10)

    stamped = PoseStamped()
    stamped.pose.position.x = 1.5
    stamped.pose.position.y = -2.0
    stamped.pose.position.z = 0.0
    stamped.pose.orientation.w = 1.0
    pose_modelcars_pub.publish(stamped)

    _spin_until(node, lambda: len(received) > 0)

    assert len(received) == 1
    assert received[0].position.x == stamped.pose.position.x
    assert received[0].position.y == stamped.pose.position.y
    assert received[0].orientation.w == stamped.pose.orientation.w

    node.destroy_node()
