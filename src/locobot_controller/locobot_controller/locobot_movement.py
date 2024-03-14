#!/usr/bin/env python3



import rclpy

from rclpy.action import ActionClient

from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, PointStamped

from nav_msgs.msg import Odometry

from locobot_autonomy.action import MoveBase

from geometry_msgs.msg import Pose

import math

# import time



class MoveBaseClient(Node):



    def __init__(self):

        super().__init__('movebase_client')

        self._action_client = ActionClient(self, MoveBase, 'movebase')

        self.arm_working_range = 0.3

        # self.start_time = time.time()

    ######################NEW CODE START#########################################

        self.robot_position = None

        self.robot_orientation = None

        self._send_goal_future = None



        self.robot_pose_subscriber = self.create_subscription(

            Odometry,

            '/odom',

            self.robot_pose_callback,

            10)

        

        self.block_pose_subscriber = self.create_subscription(

            PointStamped,

            'block_location', ################# CHANGE THIS TO THE CORRECT TOPIC 

            self.block_pose_callback,

            10)



        self.get_logger().info('MoveBaseClient has been initialized.')



    def robot_pose_callback(self, msg: Odometry):

        self.robot_position = msg.pose.pose.position

        self.robot_orientation = msg.pose.pose.orientation

        # self.get_logger().info(f'Robot pose: {msg.pose.pose}')



    def block_pose_callback(self, msg: PointStamped): ################# CHANGE THIS TO THE CORRECT TOPIC

        if self.robot_position is None:

            self.get_logger().warn('Robot position not yet received. Waiting...')

            return

        # self.get_logger().info(f'Block position received: {msg.point}')

        

        dx = msg.point.x - self.robot_position.x

        dy = msg.point.y - self.robot_position.y

        distance = math.sqrt(dx**2 + dy**2)

        ratio = (distance - self.arm_working_range) / distance



        target_pose = PoseStamped()

        target_pose.header.frame_id = "map"

        target_pose.header.stamp = self.get_clock().now().to_msg()

        target_pose.pose.position.x = self.robot_position.x + ratio * dx

        target_pose.pose.position.y = self.robot_position.y + ratio * dy

        target_pose.pose.position.z = 0.0

        

        yaw = math.atan2(dy, dx)

        quaternion = quaternion_from_euler(0, 0, yaw)

        target_pose.pose.orientation.x = quaternion[0]

        target_pose.pose.orientation.y = quaternion[1]

        target_pose.pose.orientation.z = quaternion[2]

        target_pose.pose.orientation.w = quaternion[3]

        

        # if (self._send_goal_future == None or (time.time() - self.start_time) * 1e-6 > 5):

        if (self._send_goal_future == None):

            self.send_goal(target_pose.pose, True)

            # self.start_time = time.time()



    #####################NEW CODE END############################################





    def send_goal(self, target_pose, control_base_angle_bool = True):

        self.get_logger().info('Sending goal...')

        goal_msg = MoveBase.Goal()



        goal_msg.target_pose = target_pose

        goal_msg.control_base_angle_bool = control_base_angle_bool



        self._action_client.wait_for_server()

        # result = self._action_client.send_goal(goal_msg)

        # self.get_logger().info(f'Result: {result}')

        # # self._action_client.wa_



        # # self._action_client._get_result()

        # # self._action_client._



        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

        self.get_logger().info('Goal sent to Move Base Action Server. Waiting for response...')

        self._send_goal_future.add_done_callback(self.goal_response_callback)



    def feedback_callback(self, feedback_msg):

        distance_to_goal = feedback_msg._feedback.distance

        self.get_logger().info('Feedback received: {0}'.format(distance_to_goal))



    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:

            self.get_logger().info('Goal rejected.')

            return



        self.get_logger().info('Goal accepted. Waiting for result...')

        result_future = goal_handle.get_result_async()



        result_future.add_done_callback(self.result_callback)



    def result_callback(self, future):

        result = future.result()._result

        if result.done:

            self.get_logger().info('Goal reached successfully.')

            # rclpy.shutdown()

        else:

            self.get_logger().info('Failed to reach the goal.')



def degrees_to_quaternion(degrees):

    """Convert an angle in degrees to a quaternion around the z-axis."""

    radians = math.radians(degrees)

    w = math.cos(radians / 2)

    z = math.sin(radians / 2)

    return (0, 0, z, w)  # (x, y, z, w)



def quaternion_from_euler(roll, pitch, yaw):

    """

    Calculate the quaternion from Euler angles (roll, pitch, yaw).



    Parameters:

        roll (float): Roll angle in radians.

        pitch (float): Pitch angle in radians.

        yaw (float): Yaw angle in radians.



    Returns:

        list: Quaternion [x, y, z, w].

    """

    cy = math.cos(yaw * 0.5)

    sy = math.sin(yaw * 0.5)

    cp = math.cos(pitch * 0.5)

    sp = math.sin(pitch * 0.5)

    cr = math.cos(roll * 0.5)

    sr = math.sin(roll * 0.5)



    w = cy * cp * cr + sy * sp * sr

    x = cy * cp * sr - sy * sp * cr

    y = sy * cp * sr + cy * sp * cr

    z = sy * cp * cr - cy * sp * sr



    return [x, y, z, w]







# def main(args=None):

#     rclpy.init(args=args)



#     try:

#         movebase_client = MoveBaseClient()



#         # Define the target pose for the goal

#         target_pose = Pose()

#         target_pose.position.x = 1.0  # Replace with the desired x-coordinate

#         target_pose.position.y = 0.0  # Replace with the desired y-coordinate



#         # convert the Euler angles to quaternion

#         orientation_degrees = 45  # Replace with the desired orientation in degrees

#         (x, y, z, w) = degrees_to_quaternion(orientation_degrees)

#         print(f'Quaternion: {(x, y, z, w)}')

#         target_pose.orientation.z = z

#         target_pose.orientation.w = w

        

#         # Define control_base_angle_bool

#         control_base_angle_bool = True



#         # Send the goal to the action server

#         movebase_client.send_goal(target_pose, control_base_angle_bool)



#         rclpy.spin(movebase_client)



#     except KeyboardInterrupt:

#         pass

#     finally:

#         # Shutdown the ROS 2 system

#         rclpy.shutdown()



# if __name__ == '__main__':

#     main()



#####################NEW CODE START##########################################

def main(args=None):

    rclpy.init(args=args)

    movebase_client_node = MoveBaseClient()

    rclpy.spin(movebase_client_node)

    movebase_client_node.destroy_node()

    rclpy.shutdown()



if __name__ == '__main__':

    main()

#####################NEW CODE END############################################

11:05

