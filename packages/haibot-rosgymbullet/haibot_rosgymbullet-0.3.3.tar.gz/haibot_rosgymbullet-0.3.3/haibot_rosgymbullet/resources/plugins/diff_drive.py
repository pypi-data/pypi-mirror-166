import rospy
from geometry_msgs.msg import Twist


class DiffDrive:
    def __init__(self, pybullet, robot, **kwargs):
        self.pb = pybullet
        self.robot = robot

        try:
            name = kwargs["name"]
            parameters = rospy.get_param("~" + name)
            # parameters = {'plugins': [{'module': 'haibot_rosgymbullet.resources.plugins.body_vel_control', 'class': 'cmdVelCtrl'}, {'module': 'haibot_rosgymbullet.resources.plugins.odometry', 'class': 'simpleOdometry'}, {'module': 'haibot_rosgymbullet.resources.plugins.control', 'class': 'Control'}, {'module': 'haibot_rosgymbullet.resources.plugins.joint_state_pub', 'class': 'joinStatePub'}, {'module': 'haibot_rosgymbullet.resources.plugins.laser_scanner', 'class': 'laserScanner'}, {'module': 'haibot_rosgymbullet.resources.plugins.rgbd_camera', 'class': 'RGBDCamera'}, {'module': 'haibot_rosgymbullet.resources.plugins.diff_drive', 'class': 'DiffDrive', 'name': 'diff_drive_controller'}], 'loop_rate': 80.0, 'gravity': -9.81, 'max_effort': 10.0, 'use_intertia_from_file': False, 'laser': {'frame_id': 'base_scan', 'angle_min': -2.26889, 'angle_max': 2.26889, 'num_beams': 75, 'range_min': 0.05, 'range_max': 5.6, 'beam_visualisation': True}, 'rgbd_camera': {'frame_id': 'kinect_link', 'resolution': {'width': 640, 'height': 480}}, 'diff_drive_controller': {'left_joints': ['joint_left_wheel'], 'right_joints': ['joint_right_wheel'], 'wheel_separation': 1.0, 'wheel_radius': 0.05, 'cmd_vel': '/cmd_vel'}} + name
        except Exception:
            rospy.logerr("Not loading plugin {}".format(self.__class__.__name__))
            import traceback
            traceback.print_exc()
            self.no_execution = True
            return

        # joint information preparation
        self.revolute_joints_id_name = kwargs["rev_joints"]
        self.revolute_joints_name_id = {v: k for k, v in self.revolute_joints_id_name.items()}

        # a flag to monitor if anything went wrong
        self.no_execution = False

        cmd_vel_topic = parameters.get("cmd_vel", "~cmd_vel")
        self.cmd_vel_subscriber = rospy.Subscriber(cmd_vel_topic, Twist, self.cmd_vel_callback)

        if (wheel_separation := parameters.get("wheel_separation", None)) is None:
            rospy.logwarn("No wheel_separation provided, using 1.0 as default")
            wheel_separation = 1.0
        self.wheel_separation = wheel_separation
        if (wheel_radius := parameters.get("wheel_radius", None)) is None:
            rospy.logwarn("No wheel_radius provided, using 0.05 as default")
            wheel_radius = 0.05
        self.wheel_radius = wheel_radius

        if (left_joints := parameters.get("left_joints", None)) is None:
            rospy.logerr("No left_joints provided")
            self.no_execution = True
            return
        if isinstance(left_joints, list) is False and type(left_joints) == str:
            left_joints = [left_joints]
        if (right_joints := parameters.get("right_joints", None)) is None:
            rospy.logerr("No right_joints provided")
            self.no_execution = True
            return
        if isinstance(right_joints, list) is False and type(right_joints) == str:
            right_joints = [right_joints]

        self.joint_indices = {"left": [], "right": []}
        for side in ["left", "right"]:
            for joint_name in eval(side + "_joints"):
                if joint_name not in self.revolute_joints_name_id:
                    rospy.logerr("Could not find joint {} in urdf".format(joint_name))
                    self.no_execution = True
                    return
                self.joint_indices[side].append(self.revolute_joints_name_id[joint_name])

        self.cmd_vel: Twist = Twist()

    def cmd_vel_callback(self, msg: Twist):
        self.cmd_vel = msg

    def get_wheel_speeds(self):
        vx = self.cmd_vel.linear.x
        wz = self.cmd_vel.angular.z
        left = (vx - wz * self.wheel_separation / 2.0) / self.wheel_radius
        right = (vx + wz * self.wheel_separation / 2.0) / self.wheel_radius
        return {"left": left, "right": right}

    def execute(self):
        if not self.no_execution:
            speeds = self.get_wheel_speeds()
            for side in ["left", "right"]:
                indices = self.joint_indices[side]
                self.pb.setJointMotorControlArray(
                    bodyUniqueId=self.robot,
                    jointIndices=indices,
                    controlMode=self.pb.VELOCITY_CONTROL,
                    targetVelocities=[speeds[side] for _ in range(len(indices))]
                )