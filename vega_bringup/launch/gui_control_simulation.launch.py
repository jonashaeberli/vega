from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    vega_description_launch_dir = os.path.join(get_package_share_directory('vega_description'), 'launch')
    launch_file_path_description = os.path.join(vega_description_launch_dir, 'display_no_gui.launch.py')

    vega_gui_launch_dir = os.path.join(get_package_share_directory('vega_gui'), 'launch')
    launch_file_path_gui = os.path.join(vega_gui_launch_dir, 'gui.launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_file_path_description),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_file_path_gui),
        )
    ])
