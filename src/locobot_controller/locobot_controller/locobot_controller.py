import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist, Pose, Quaternion
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import math
import tf_transformations

class LocobotController(Node):
    def __init__(self):
        super().__init__('locobot_controller')
        self.image_subscriber = self.create_subscription(Image, '/locobot/camera_frame_sensor/image_raw', self.image_callback, 10)
        self.vel_publisher = self.create_publisher(Twist, '/locobot/diff_drive_controller/cmd_vel_unstamped', 10)
        self.bridge = CvBridge()
        self.target_block_pose = None

    def image_callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error("CvBridge Error: {0}".format(e))
            return

        # Use the provided perception code for color detection
        # Assuming you want to detect a specific color, say 'red'
        color_mask = 'r' # Change this to 'g', 'b', or 'y' for green, blue, or yellow respectively
        mask_img = self.student_function_1(cv_image, color_mask=color_mask)

        # Assuming mask_img contains the desired blocks highlighted
        # You can then use the mask_img to find the block's position, navigate and manipulate the arm accordingly
        # For example, finding contours in the mask_img and then navigating to the centroid of the detected block

    def student_function_1(self, color_img, color_mask='r'):
        hsv_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
        if color_mask == 'r':
            lower_red1 = np.array([0, 70, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 70, 50])
            upper_red2 = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)
        elif color_mask == 'g':
            lower_green = np.array([35, 70, 50])
            upper_green = np.array([85, 255, 255])
            mask = cv2.inRange(hsv_img, lower_green, upper_green)
        elif color_mask == 'b':
            lower_blue = np.array([100, 70, 50])
            upper_blue = np.array([140, 255, 255])
            mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
        elif color_mask == 'y':
            lower_yellow = np.array([25, 70, 50])
            upper_yellow = np.array([35, 255, 255])
            mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
        
        if color_mask in ['r', 'g', 'b', 'y']:
            mask_img = cv2.bitwise_and(color_img, color_img, mask=mask)
        else:
            mask_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask_img[mask == 0] = 0
        
        return mask_img


    def navigate_to_block(self):
        """
        This function calculates the control action required to navigate the robot towards the target pose.
        It uses a simple proportional controller to generate velocity commands based on the error between the current pose and the target pose.
        """
        # Wait for a valid target pose to be available
        if self.target_pose is None:
            self.get_logger().info("Waiting for a valid target pose...")
            return

        # Calculate error between current pose (point_P as a proxy for robot's position) and target pose
        err_x = self.target_pose.position.x - self.current_pose.position.x
        err_y = self.target_pose.position.y - self.current_pose.position.y
        error_distance = np.sqrt(err_x**2 + err_y**2)

        # Proportional control parameters
        Kp_linear = 0.5
        Kp_angular = 2.0

        # Calculate control signals
        linear_speed = Kp_linear * error_distance
        angular_speed = Kp_angular * np.arctan2(err_y, err_x)

        # Create and publish Twist message
        velocity_command = Twist()
        velocity_command.linear.x = linear_speed if error_distance > self.goal_reached_error else 0.0
        velocity_command.angular.z = angular_speed if error_distance > self.goal_reached_error else 0.0
        self.mobile_base_vel_publisher.publish(velocity_command)

        # Check if the target pose is reached within a threshold
        if error_distance <= self.goal_reached_error:
            self.get_logger().info("Target pose reached. Stopping the robot.")
            # Stop the robot
            velocity_command.linear.x = 0.0
            velocity_command.angular.z = 0.0
            self.mobile_base_vel_publisher.publish(velocity_command)
            # Update state or handle next action


    def pick_up_block(self, block_pose):
        # Wait for the action server
        self.arm_action_client.wait_for_server()
        self.gripper_action_client.wait_for_server()

        # Open the gripper before picking up
        self.set_gripper_width(0.04)  # Open the gripper (width in meters)

        # Approach the block
        approach_pose = block_pose
        approach_pose.position.z += 0.1  # Adjust Z to be above the block
        self.move_to_pose(approach_pose)

        # Lower the arm to pick up the block
        pick_pose = block_pose
        self.move_to_pose(pick_pose)

        # Close the gripper to grab the block
        self.set_gripper_width(0.0)  # Close the gripper

        # Lift the block
        lift_pose = block_pose
        lift_pose.position.z += 0.1  # Lift the block up
        self.move_to_pose(lift_pose)

    def move_to_pose(self, pose):
        goal = MoveGroupGoal()
        goal.request.target_pose = pose
        # Send the goal
        self.arm_action_client.send_goal(goal)
        # Wait for the result
        self.arm_action_client.wait_for_result()

    def set_gripper_width(self, width):
        goal = MoveGroupGoal()
        goal.request.width = width  # Set the target width for the gripper
        # Send the goal
        self.gripper_action_client.send_goal(goal)
        # Wait for the result
        self.gripper_action_client.wait_for_result()

def main(args=None):
    rclpy.init(args=args)
    locobot_controller = LocobotController()
    rclpy.spin(locobot_controller)
    locobot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
