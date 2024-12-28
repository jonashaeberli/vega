from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the path to the launch file in package_a
    vega_description_launch_dir = os.path.join(get_package_share_directory('vega_description'), 'launch')
    launch_file_path = os.path.join(vega_description_launch_dir, 'display_no_gui.launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_file_path),
        )
    ])
