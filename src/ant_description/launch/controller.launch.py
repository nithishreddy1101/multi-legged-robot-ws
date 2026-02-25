import rclpy
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    ant_grip_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ant_grip_controller", "--controller-manager", "/controller_manager"],
    )

    ant_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["ant_controller", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        ant_controller_spawner,
        ant_grip_controller_spawner
    ])