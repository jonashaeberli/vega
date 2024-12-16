import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue  # Import ParameterValue

import xacro

def generate_launch_description():

    ####### DATA INPUT ##########
    package_description = "vega_description"
    urdf_file = 'vega_description_chain.xacro'

    ####### DATA INPUT END ##########
    print("Fetching URDF ==>")
    robot_model_path = os.path.join(
        get_package_share_directory(package_description))

    xacro_file = os.path.join(robot_model_path, 'urdf', urdf_file)

    # convert XACRO file into URDF
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher_node',
        emulate_tty=True,
        parameters=[{
            'use_sim_time': True,
            'robot_description': doc.toxml(),
        }],
        output="screen"
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
    )

    # RVIZ Configuration
    rviz_config_dir = os.path.join(get_package_share_directory(package_description), 'rviz', 'urdf_vis.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        name='rviz_node',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', rviz_config_dir]
    )

    # create and return launch description object
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])

