import rclpy
from rclpy.node import Node

from vega_kinematics_solver.inverse_kinematics import Kinematics



class LinearTrajectoryPlanner(Node):

    def __init__(self):
        super().__init__('linear_trajectory_planner')

        self.linear_trajectory_action = rclpy.action.ActionServer(
            self, /* action_type */, 'plan_linear_trajectory',
            # callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(LinearTrajectoryPlanner())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
