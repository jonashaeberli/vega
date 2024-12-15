import numpy as np
import warnings


class Kinematics:
    def __init__(self):
        self.upper_arm_length = 250 #mm
        self.lower_arm_length = 300 #mm
        
        self.axis_4_offset_x = 35 #mm
        self.axis_4_offset_y = 0 #mm
        self.axis_4_offset_z = -16.25 #mm

        self.base_offset_x = 20 #mm
        self.base_offset_z = 115 #mm

        self.upper_arm_range = (np.deg2rad(115), np.deg2rad(0))
        self.lower_arm_range = (np.deg2rad(0), np.deg2rad(-110))
        self.min_lever_distance = 52.5

        self.joint_2_3_angle_offset = np.deg2rad(110)
        self.joint_2_6_angle_offset = np.deg2rad(-10)

        warnings.filterwarnings("error", category=RuntimeWarning)


    def inverse_kinematics(self, x=None, y=None, z=None):
        if x is not None and y is not None and z is not None:
            x = x - self.axis_4_offset_x - self.base_offset_x
            y = y - self.axis_4_offset_y
            z = z - self.axis_4_offset_z - self.base_offset_z

            joint_1_2_angle = np.arctan(y/x)

            x_y_tan = np.sqrt(x**2 + y**2)

            base_to_tool = np.sqrt(x_y_tan**2 + z**2)

            joint_2_3_angle = np.arccos((self.upper_arm_length**2 + x_y_tan**2 - self.lower_arm_length**2) / (2 * self.upper_arm_length * x_y_tan)) + np.arctan(z/x_y_tan) - self.joint_2_3_angle_offset
            joint_2_6_angle = joint_2_3_angle + np.arccos((self.lower_arm_length**2 + self.upper_arm_length**2 - x_y_tan**2) / (2 * self.lower_arm_length * self.upper_arm_length)) - np.pi - self.joint_2_6_angle_offset

            joint_angles = {'joint_1_2_angle': joint_1_2_angle, 'joint_2_3_angle': joint_2_3_angle, 'joint_2_6_angle': joint_2_6_angle}
            print(joint_angles)
            return

        else:
            print("Invalide inverse kinematics arguments")
            return
        

kinematics = Kinematics()
kinematics.inverse_kinematics(200, 0, 50)