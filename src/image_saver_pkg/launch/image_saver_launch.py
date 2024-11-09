from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='image_saver_pkg',
            executable='image_saver',
            name='image_saver_node',
            output='screen',
            parameters=[
                {'save_directory': '/home/coastz/ros2_ws/src/image_saver_pkg/data'},
            ],
        ),
    ])
