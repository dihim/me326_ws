import rclpy
from rclpy.node import Node
from la_msgs.srv import Ptps
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped
from rclpy.action import ActionClient
import sys

class PerceptionClient(Node): 

    def __init__(self): 
        super().__init__('perception_client')
        self.get_logger().info("Starting Node")
        self.client = self.create_client(Ptps, 'pix_to_point_cpp')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...') 
        self.req = Ptps.Request()
        self.subscription = self.create_subscription(String, 'desired_color', self.listener_callback, 10) 
        self.publisher = self.create_publisher(PointStamped, 'block_location', 10) 
        self.get_logger().info("Service found, setting up")
        self.desired_frame = 'locobot/odom'
        self.client_futures = []
        self.point = None

    def listener_callback(self, msg):
        self.desired_color = msg.data
        print("Searching for color : " + msg.data)
        self.req.desired_frame = self.desired_frame
        self.client_futures.append(self.client.call_async(self.req))

    def spin(self):
        self.get_logger().info("Spinning is a fun trick")
        while rclpy.ok():
            rclpy.spin_once(self)
            incomplete_futures = []
            for f in self.client_futures:
                if f.done():
                    result = f.result()
                    self.get_logger().info('Found Block') 
                    if self.desired_color == 'red':
                        if result.red_present and (len(result.red_points) != 0):
                            self.point = result.red_points[0]
                    elif self.desired_color == 'blue' and (len(result.blue_points) != 0): 
                        if result.blue_present: 
                            self.point = result.blue_points[0]
                    elif self.desired_color == 'yellow' and (len(result.yellow_points) != 0):
                        if result.yellow_present:
                            self.point = result.yellow_points[0]
                    elif self.desired_color == 'green'and (len(result.green_points) != 0): 
                        if result.green_present:
                            self.point = result.green_points[0]
                    if self.point != None:
                        self.get_logger().info("Publishing block location") 
                        self.publisher.publish(self.point)
                        self.point = None
                else:
                    incomplete_futures.append(f) 
            self.client_futures = incomplete_futures 

def main(args=None):
    rclpy.init(args=args)
    perception_client = PerceptionClient()
    perception_client.spin()
    perception_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
