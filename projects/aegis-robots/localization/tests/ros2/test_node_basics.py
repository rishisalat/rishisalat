"""Basic ROS2 node tests using rclpy."""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def test_node_creation():
    node = Node("test_node_creation")
    assert node.get_name() == "test_node_creation"
    node.destroy_node()


def test_publisher_subscriber_roundtrip():
    node = Node("test_pubsub")
    received: list[str] = []

    node.create_subscription(
        String,
        "test_topic",
        lambda msg: received.append(msg.data),
        10,
    )
    publisher = node.create_publisher(String, "test_topic", 10)

    publisher.publish(String(data="hello ros2"))

    end_time = node.get_clock().now().nanoseconds + int(2e9)
    while not received and node.get_clock().now().nanoseconds < end_time:
        rclpy.spin_once(node, timeout_sec=0.1)

    assert received == ["hello ros2"]
    node.destroy_node()
