from pydoc import doc
import numpy as np
import warnings


class Kinematics:
    def __init__(self):
        self.upper_arm_length = 250.0 #mm
        self.lower_arm_length = 300.0 #mm
        
        self.axis_4_offset_x = 60.0 #mm
        self.axis_4_offset_y = -30.0 #mm this includes the offset that is created to the y position of the rotation tabel
        self.axis_4_offset_z = -54.0 #mm

        self.base_offset_x = 20.0 #mm
        self.base_offset_z = 187.0 #mm

        self.upper_arm_range = (np.deg2rad(110), np.deg2rad(-5))
        self.lower_arm_range = (np.deg2rad(10), np.deg2rad(-100))

        self.joint_2_3_angle_offset = np.deg2rad(110)
        self.joint_2_6_angle_offset = np.deg2rad(10)

        self.joint_2_6_lever_angle_offset = np.deg2rad(10)

        warnings.filterwarnings("error", category=RuntimeWarning)


    def inverse_kinematics(self, x=None, y=None, z=None, yaw=None):
        """Calculates the inverse Kinematics for Vega robotic arm"""
        try:
            if x is not None and y is not None and z is not None:
                if yaw is None:
                    yaw = 0 #rad
                # z offset is independet of the rotation angle therfor we can already set it here
                # x and y we can only set after we know the rotation angle of the joint_1_2
                z = z - self.axis_4_offset_z - self.base_offset_z

                #first determin the angle of the rotating joint with paying attention to the y rotation offset parameter
                x_y_tan = np.hypot(x, y)
                x_y_angle = np.arctan(y/x)
                x_y_angle_offset = np.arcsin(self.axis_4_offset_y/x_y_tan)


                # joint_1_2 is the base rotation angle
                joint_1_2_angle = x_y_angle + x_y_angle_offset

                x_y_tan_offset_corrected = np.sqrt(x_y_tan**2 - self.axis_4_offset_y**2) - self.base_offset_x - self.axis_4_offset_x
                base_to_tool = np.hypot(x_y_tan_offset_corrected, z)

                # joint_2_3 is the upper arm c
                joint_2_3_angle = np.arccos((self.upper_arm_length**2 + base_to_tool**2 - self.lower_arm_length**2) / (2 * self.upper_arm_length * base_to_tool)) + np.arctan(z/x_y_tan_offset_corrected)

                # joint_2_6 is the lower arm angle
                joint_2_6_angle = joint_2_3_angle + np.arccos((self.lower_arm_length**2 + self.upper_arm_length**2 - base_to_tool**2) / (2 * self.lower_arm_length * self.upper_arm_length)) - np.pi

                #joint_11_tool is the wrist rotation angle
                joint_11_tool_angle = np.pi - joint_1_2_angle

                # apply offsets
                joint_2_3_angle = self.joint_2_3_angle_offset - joint_2_3_angle
                joint_2_6_angle = joint_2_6_angle + self.joint_2_6_lever_angle_offset - self.joint_2_6_angle_offset

                joint_angles = {'joint_1_2': joint_1_2_angle, 'joint_2_3': joint_2_3_angle, 'joint_2_6': joint_2_6_angle, 'joint_11_tool': joint_11_tool_angle}
                return joint_angles
            
        except RuntimeWarning as rw:
            return {}

        else:
            print("Invalide inverse kinematics arguments")
            return False

