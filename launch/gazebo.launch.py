import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import (OnProcessStart, OnProcessExit)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

from launch_ros.actions import Node

import xacro

def generate_launch_description():
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    #             )
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])]
        ),
        launch_arguments={"verbose": "true"}.items(),
    )
        
    package_name = 'comau_racer5_080_description'
    package_path = os.path.join(
        get_package_share_directory(package_name))
        
    # xacro_file = os.path.join(package_path, 'urdf', 'comau.urdf.xacro')
    xacro_file = os.path.join(package_path, 'urdf', 'comau_racer5_080.xacro')
    # xacro_file = os.path.join(package_path, 'urdf', 'example_robot.urdf.xacro')
    
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': doc.toxml(), 
                        'use_sim_time': True}]
    )
        
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'joint_state_broadcaster'],
        output='screen'
    )
        
    spawn_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    ) 
        
    load_arm_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'arm_controller'],
        output='screen'
    )
        
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', '/robot_description',
                        '-entity', package_name],
                        output='screen')
                        
    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_controller,
                on_exit=[load_arm_controller],
            )
        ),
        spawn_controller,
        gazebo,
        node_robot_state_publisher,
        spawn_entity
    ])