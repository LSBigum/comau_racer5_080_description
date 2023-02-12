import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'comau_racer5_080_description'
    package_path = os.path.join(get_package_share_directory(package_name))
    launch_directory = os.path.join(package_path, 'launch')

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([launch_directory, '/gazebo.launch.py']),)
        
    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([launch_directory, '/rviz2.launch.py']),)

    return LaunchDescription([
        gazebo,
        rviz
    ])