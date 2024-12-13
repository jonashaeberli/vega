#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState

class PassiveJointHandler(Node):
    def __init__(self):
        super().__init__('passive_joint_handler')

        update_rate = 200 #Hz
        self.passive_joints = ['Joint_3_4', 'Joint_4_5', 'Joint_6_7', 'Joint_2_8', 'Joint_8_9', 'Joint_9_10']

        self.publisher_ = self.create_publisher(JointState, 'passive_joint_states', 10)

        self.subscription = self.create_subscription(
            JointState, 'joint_states', self.handle_joint_states, 10)

        self.target_joints = ['Joint_1_2', 'Joint_2_3', 'Joint_2_6']

        self.rotation_angle = None
        self.upper_arm_angle = None
        self.lower_arm_angle = None

    def publish_passive_joint_states(self, passive_joint_positions):
        msg = JointState()
        for index, joint_name in enumerate(self.passive_joints):
            msg.name.append(joint_name)
            msg.position.append(passive_joint_positions[joint_name])

        #self.get_logger().info('Publishing passive joint values')
        self.publisher_.publish(msg)

    def handle_joint_states(self, msg):
        joint_angles = dict(zip(msg.name, msg.position))
        self.rotation_angle = joint_angles[self.target_joints[0]]
        self.upper_arm_angle = joint_angles[self.target_joints[1]]
        self.lower_arm_angle = joint_angles[self.target_joints[2]]
        #self.get_logger().info(f'Activ Joint values: Rotation: {self.rotation_angle} Upper_Arm: {self.upper_arm_angle} Lower_Arm: {self.lower_arm_angle}')

        passive_joint_positions = self.calculate_passive_joint_positions()
        self.publish_passive_joint_states(passive_joint_positions)

    def calculate_passive_joint_positions(self):
        passive_joint_positions = {
        'Joint_3_4': - self.upper_arm_angle - self.lower_arm_angle,
        'Joint_4_5': - self.lower_arm_angle,
        'Joint_6_7': - self.lower_arm_angle - self.upper_arm_angle,
        'Joint_2_8': - self.upper_arm_angle,
        'Joint_8_9': self.upper_arm_angle,
        'Joint_9_10': self.lower_arm_angle
        }
        return passive_joint_positions
         


def main (args=None):
        rclpy.init(args=args)
        
        pjh = PassiveJointHandler()

        rclpy.spin(pjh)

        pjh.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()