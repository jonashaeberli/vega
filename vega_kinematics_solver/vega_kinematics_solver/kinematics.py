import numpy as np
import warnings


class Kinematics:
    def __init__(self):
        self.upper_arm_length = 250 #mm
        self.lower_arm_length = 300 #mm
        
        self.axis_4_offset_x = 30 #mm
        self.axis_4_offset_y = 3.5 #mm this includes the offset that is created to the y position of the rotation tabel
        #currently it is using the distance to the lower corner of Link_5
        self.axis_4_offset_z = -20 #mm

        self.base_offset_x = 20 #mm
        self.base_offset_z = 187 #mm

        self.upper_arm_range = (np.deg2rad(110), np.deg2rad(-5))
        self.lower_arm_range = (np.deg2rad(10), np.deg2rad(-100))
        self.min_lever_distance = 52.5

        self.joint_2_3_angle_offset = np.deg2rad(110)
        self.joint_2_6_angle_offset = np.deg2rad(10)

        self.joint_2_6_lever_angle_offset = np.deg2rad(10)

        warnings.filterwarnings("error", category=RuntimeWarning)


    def inverse_kinematics(self, x=None, y=None, z=None):
        if x is not None and y is not None and z is not None:
            # z offset is independet of the rotation angle therfor we can already set it here
            # x and y we can only set after we know the rotation angle of the joint_1_2
            z = z - self.axis_4_offset_z - self.base_offset_z

            #first determin the angle of the rotating joint with paying attention to the y rotation offset parameter
            x_y_tan = np.hypot(x, y)
            x_y_angle = np.arctan(y/x)
            x_y_angle_offset = np.arcsin(self.axis_4_offset_y/x_y_tan)

            joint_1_2_angle = x_y_angle + x_y_angle_offset

            x_y_tan_offset_corrected = np.sqrt(x_y_tan**2 - self.axis_4_offset_y**2) - self.base_offset_x - self.axis_4_offset_x
            base_to_tool = np.hypot(x_y_tan_offset_corrected, z)

            # joint_2_3 is the upper arm c
            joint_2_3_angle = np.arccos((self.upper_arm_length**2 + base_to_tool**2 - self.lower_arm_length**2) / (2 * self.upper_arm_length * base_to_tool)) + np.arctan(z/x_y_tan_offset_corrected)
            joint_2_3_deg = np.rad2deg(joint_2_3_angle)
            print(f'upper arm deg: {joint_2_3_deg}')

            # joint_2_6 is the lower arm angle
            joint_2_6_angle = joint_2_3_angle + np.arccos((self.lower_arm_length**2 + self.upper_arm_length**2 - base_to_tool**2) / (2 * self.lower_arm_length * self.upper_arm_length)) - np.pi
            joint_2_6_deg = np.rad2deg(joint_2_6_angle)
            print(f'lower arm deg: {joint_2_6_deg}')

            # apply offsets
            joint_2_3_angle = self.joint_2_3_angle_offset - joint_2_3_angle
            joint_2_6_angle = joint_2_6_angle + self.joint_2_6_lever_angle_offset - self.joint_2_6_angle_offset

            joint_angles = {'joint_1_2_angle': np.rad2deg(joint_1_2_angle), 'joint_2_3_angle': np.rad2deg(joint_2_3_angle), 'joint_2_6_angle': np.rad2deg(joint_2_6_angle)}
            print(joint_angles)
            return

        else:
            print("Invalide inverse kinematics arguments")
            return