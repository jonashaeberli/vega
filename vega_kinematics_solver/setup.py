from setuptools import find_packages, setup

from vega.vega_kinematics_solver.vega_kinematics_solver import linear_trajectory_planner

package_name = 'vega_kinematics_solver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jonas',
    maintainer_email='jonas.haeberli@hispeed.ch',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "linear_trajectory_planner = vega_kinematics_solver.linear_trajectory_planner.py"
        ],
    },
)
