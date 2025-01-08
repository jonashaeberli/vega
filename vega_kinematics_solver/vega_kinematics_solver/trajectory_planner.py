import sys
import os
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
import time
import numpy as np
from vega_msgs.action import TrajectoryRequest
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState

from vega_kinematics_solver.kinematics import Kinematics
from roboticstoolbox.tools.trajectory import Trajectory, ctraj, quintic
from spatialmath import SE3


class TrajectoryPlanner(Node):

    def __init__(self):
        super().__init__('trajectory_planner')

        self.kinematics = Kinematics()

        self.get_logger().info('trajectory instance created')

        self.linear_trajectory_action = rclpy.action.ActionServer(
            self, TrajectoryRequest, 'plan_trajectory',
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback)
        
        self._publisher = self.create_publisher(JointState, 'control_joints', 10)
        
    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal: {}'.format(goal_request))
        #TODO: check if goal position is within work envelope of the robot
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Goal was canceled: {}'.format(goal_handle.goal_id))
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Unpacking positions...')
        goal_msg = goal_handle.request
        start_pos = goal_msg.waypoints[0]
        if len(goal_msg.waypoints) > 2:
            for i in range(len(goal_msg.waypoints) - 2):
                via_pos = goal_msg.waypoints[i+1]
        end_pos = goal_msg.waypoints[len(goal_msg.waypoints)-1]

        T0 = SE3(start_pos.position.x , start_pos.position.y, start_pos.position.z) * SE3.RPY([0.0, 0.0, 0.0])
        T1 = SE3(end_pos.position.x, end_pos.position.y, end_pos.position.z) * SE3.RPY([0.0, 0.0, 0.0])

        quintic_interpolation = quintic(0,1,100)
        s = quintic_interpolation.q

        cartesian_trajectory = ctraj(T0, T1, s=s)

        # Prepare arrays for x, y, z, and yaw (psi)
        x_vals = []
        y_vals = []
        z_vals = []
        yaw_vals = []
        steps = []

        # Loop through the SE3 poses
        for pose in cartesian_trajectory:

            translation = pose.data[0][0:3, 3]

            x_vals.append(translation[0])
            y_vals.append(translation[1])
            z_vals.append(translation[2])
            
            euler_angles = SE3.rpy(pose, 'rad')
            yaw_vals.append(euler_angles[0])

        inverse_trajectory = []

        for pos in range(len(cartesian_trajectory)):
            inverse_trajectory.append(self.kinematics.inverse_kinematics(x_vals[pos], y_vals[pos], z_vals[pos], yaw_vals[pos]))

        # Assuming inverse_trajectory is a list of trajectory points

        while True:  # This will create an infinite loop that goes back and forth
            for traj_point in inverse_trajectory:
                # Extracting the values directly
                joint_values = [traj_point[key] for key in ['joint_1_2', 'joint_2_3', 'joint_2_6', 'joint_11_tool']]

                # Creating the message and publishing it
                msg = JointState()
                msg.name = ['joint_1_2', 'joint_2_3', 'joint_2_6', 'joint_11_tool']
                msg.position = joint_values  # Assign the extracted values
                self.get_logger().info('Publishing message')
                self._publisher.publish(msg)
                time.sleep(1/100)
            
            # Reverse the trajectory for the back-and-forth motion
            for traj_point in reversed(inverse_trajectory):
                # Extracting the values directly
                joint_values = [traj_point[key] for key in ['joint_1_2', 'joint_2_3', 'joint_2_6', 'joint_11_tool']]

                # Creating the message and publishing it
                msg = JointState()
                msg.name = ['joint_1_2', 'joint_2_3', 'joint_2_6', 'joint_11_tool']
                msg.position = joint_values  # Assign the extracted values
                self.get_logger().info('Publishing message')
                self._publisher.publish(msg)
                time.sleep(1/100)


        feedback_msg = TrajectoryRequest.Feedback()

        feedback_msg.status = str(1)
        goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = TrajectoryRequest.Result()

        return result



def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(TrajectoryPlanner())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
