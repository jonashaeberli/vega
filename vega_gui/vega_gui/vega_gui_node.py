from shlex import join
import sys
import rclpy

from rclpy.node import Node

from interactive_markers import InteractiveMarkerServer
from visualization_msgs.msg import InteractiveMarker
from visualization_msgs.msg import InteractiveMarkerControl
from visualization_msgs.msg import Marker

from vega_kinematics_solver.kinematics import Kinematics

from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState
from interactive_markers import InteractiveMarkerServer
from visualization_msgs.msg import InteractiveMarker
from visualization_msgs.msg import InteractiveMarkerControl
from visualization_msgs.msg import InteractiveMarkerFeedback

from geometry_msgs.msg import Quaternion


class VegaGuiNode(Node):
    def __init__(self):
        super().__init__('vega_gui_node')
        self.response_data = {}
        self.kinematics = Kinematics()

        # publisher to move robot
        self._publisher = self.create_publisher(JointState, 'control_joints', 10)

    def create_interactive_marker(self):
        self.get_logger().info('start interactive marker server')
        self.interactive_marker_server = InteractiveMarkerServer(self, 'control_marker')
        int_marker = InteractiveMarker()
        int_marker.header.frame_id = 'link_1'
        int_marker.pose.position = Point(x=0.5, y=0.5, z=0.0)
        int_marker.scale = 1.0

        int_marker.name = 'control vega'
        int_marker.description = 'Simple 4-DOF Control for vega robotic arm'

        interaction_mode = InteractiveMarkerControl.MOVE_ROTATE_3D

        control = InteractiveMarkerControl()
        control.always_visible = True
        int_marker.controls.append(control)
        int_marker.controls[0].interaction_mode = interaction_mode

        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 1.0
        control.orientation.y = 0.0
        control.orientation.z = 0.0
        self.normalizeQuaternion(control.orientation)
        control.name = 'move_x'
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        control.orientation_mode = InteractiveMarkerControl.FIXED
        int_marker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 1.0
        control.orientation.z = 0.0
        self.normalizeQuaternion(control.orientation)
        control.name = 'rotate_z'
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        int_marker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 1.0
        control.orientation.z = 0.0
        self.normalizeQuaternion(control.orientation)
        control.name = 'move_z'
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        control.orientation_mode = InteractiveMarkerControl.FIXED
        int_marker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation.w = 1.0
        control.orientation.x = 0.0
        control.orientation.y = 0.0
        control.orientation.z = 1.0
        self.normalizeQuaternion(control.orientation)
        control.name = 'move_y'
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        control.orientation_mode = InteractiveMarkerControl.FIXED
        int_marker.controls.append(control)

        self.interactive_marker_server.insert(int_marker, feedback_callback=self.interactive_marker_feedback)
        self.interactive_marker_server.applyChanges()
        
    

    def normalizeQuaternion(self, quaternion_msg):
        norm = quaternion_msg.x**2 + quaternion_msg.y**2 + quaternion_msg.z**2 + quaternion_msg.w**2
        s = norm**(-0.5)
        quaternion_msg.x *= s
        quaternion_msg.y *= s
        quaternion_msg.z *= s
        quaternion_msg.w *= s


    def interactive_marker_feedback(self, feedback):
        log_prefix = (
            f"Feedback from marker '{feedback.marker_name}' / control '{feedback.control_name}'"
        )

        log_mouse = ''
        if feedback.mouse_point_valid:
            log_mouse = (
                f'{feedback.mouse_point.x}, {feedback.mouse_point.y}, '
                f'{feedback.mouse_point.z} in frame {feedback.header.frame_id}'
            )

        if feedback.event_type == InteractiveMarkerFeedback.BUTTON_CLICK:
            self.get_logger().info(f'{log_prefix}: button click at {log_mouse}')
        elif feedback.event_type == InteractiveMarkerFeedback.MENU_SELECT:
            self.get_logger().info(
                f'{log_prefix}: menu item {feedback.menu_entry_id} clicked at {log_mouse}'
            )
        elif feedback.event_type == InteractiveMarkerFeedback.POSE_UPDATE:
            self.get_logger().info(
                f'{log_prefix}: pose changed\n'
                f'position: '
                f'{feedback.pose.position.x}, {feedback.pose.position.y}, {feedback.pose.position.z}\n'
                f'orientation: '
                f'{feedback.pose.orientation.w}, {feedback.pose.orientation.x}, '
                f'{feedback.pose.orientation.y}, {feedback.pose.orientation.z}\n'
                f'frame: {feedback.header.frame_id} '
                f'time: {feedback.header.stamp.sec} sec, '
                f'{feedback.header.stamp.nanosec} nsec'
            )
            self.set_robot_position(x=feedback.pose.position.x, y=feedback.pose.position.y, z=feedback.pose.position.z, yaw=0.0)
        elif feedback.event_type == InteractiveMarkerFeedback.MOUSE_DOWN:
            self.get_logger().info(f'{log_prefix}: mouse down at {log_mouse}')
        elif feedback.event_type == InteractiveMarkerFeedback.MOUSE_UP:
            self.get_logger().info(f'{log_prefix}: mouse up at {log_mouse}')

    def set_robot_position(self, x, y, z, yaw):
        msg = JointState()
        joint_angles = self.kinematics.inverse_kinematics(x*1000,y*1000,z*1000,yaw)

        if joint_angles == {}:
            self.get_logger().info(f'ik failed')

        for joint, angle in joint_angles.items():
            msg.name.append(joint)
            msg.position.append(angle)

        self.get_logger().info(f'Publishing message: {msg}')
        self._publisher.publish(msg)
            
        


    def cleanup_interactive_marker(self):
        self.interactive_marker_server.shutdown()
