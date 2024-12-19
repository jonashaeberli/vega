from pydoc import doc
import numpy as np
import warnings


class Kinematics:
    def __init__(self):
        self.upper_arm_length = 250 #mm
        self.lower_arm_length = 300 #mm
        
        self.axis_4_offset_x = 60 #mm
        self.axis_4_offset_y = -30 #mm this includes the offset that is created to the y position of the rotation tabel
        self.axis_4_offset_z = -54 #mm

        self.base_offset_x = 20 #mm
        self.base_offset_z = 187 #mm

        self.upper_arm_range = (np.deg2rad(110), np.deg2rad(-5))
        self.lower_arm_range = (np.deg2rad(10), np.deg2rad(-100))
        self.min_lever_distance = 52.5

        self.joint_2_3_angle_offset = np.deg2rad(110)
        self.joint_2_6_angle_offset = np.deg2rad(10)

        self.joint_2_6_lever_angle_offset = np.deg2rad(10)

        warnings.filterwarnings("error", category=RuntimeWarning)


    def inverse_kinematics(self, x=None, y=None, z=None, yaw=None):
        """Calculates the inverse Kinematics for Vega robotic arm"""
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
            return joint_angles

        else:
            print("Invalide inverse kinematics arguments")
            return False
        
    
    def lever_distance(self, joint_2_3_angle, joint_2_6_angle):
        return np.sin(np.pi-(-joint_2_6_angle)-joint_2_3_angle) * self.lever_arm_length
        

    def is_valid_for_collision_check(self, x, z, joint_2_3_angle, joint_2_6_angle):
        return x is not None and z is not None and joint_2_3_angle is not None and joint_2_6_angle is not None

    def is_within_range(self, joint_angle, range_limits):
        return range_limits[0] <= joint_angle <= range_limits[1]

    def check_for_collisions(self, x=None, z=None, joint_2_3_angle=None, joint_2_6_angle=None):
        if not self.is_valid_for_collision_check(x, z, joint_2_3_angle, joint_2_6_angle):
            print("Invalid arguments for collision check")
            return False
        
        try:
            if x >= 90:
                if not self.is_within_range(joint_2_3_angle, self.upper_arm_range):
                    return False
                if not self.is_within_range(joint_2_6_angle, self.lower_arm_range):
                    return False
                if self.lever_distance(joint_2_3_angle, joint_2_6_angle) >= self.min_lever_distance:
                    return True

        except RuntimeWarning:
            pass

        return False

