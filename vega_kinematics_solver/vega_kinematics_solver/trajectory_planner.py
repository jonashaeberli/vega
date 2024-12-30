import sys
import os
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
import time
from vega_msgs.action import TrajectoryRequest
from geometry_msgs.msg import Pose
from trajectory_msgs.msg import JointTrajectory

from vega_kinematics_solver.kinematics import Kinematics
from roboticstoolbox.tools.trajectory import Trajectory


class TrajectoryPlanner(Node):

    def __init__(self):
        super().__init__('trajectory_planner')

        self.get_logger().info('trajectory instance created')

        self.linear_trajectory_action = rclpy.action.ActionServer(
            self, TrajectoryRequest, 'plan_trajectory',
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback)
        
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
        self.get_logger().info('Start position{}'.format(goal_msg.start_position))

        feedback_msg = TrajectoryRequest.Feedback()
        # TODO: Provide feedback for planning status
        for i in range(10):
            feedback_msg.status = str(i * 10 + 10)
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)  # Simulating some work

        goal_handle.succeed()
        result = TrajectoryRequest.Result()

        return result



def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(TrajectoryPlanner())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
