"""Pytest configuration for ROS2 node tests.

Provides a session-scoped rclpy context so each test can create nodes
without managing init/shutdown manually.
"""

import pytest
import rclpy


@pytest.fixture(scope="session", autouse=True)
def rclpy_session():
    rclpy.init()
    yield
    rclpy.shutdown()
