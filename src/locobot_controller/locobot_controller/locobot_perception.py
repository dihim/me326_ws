import rclpy
from rclpy.node import Node
from la_msgs.srv import Ptps
from std_msgs.msg import String
from geometry_msgs.msg import PointStamped


class PerceptionClient(Node): 

    def __init__(self): 
        super().__init__('perception_client')
        self.cli = self.create_client(Ptps, 'pix_to_point_cpp') 
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again')
        self.req = Ptps.Request()
        self.subscription = self.create_subscription(String, '/desired_color', self.listener_callback, 10)
        self.publisher = self.create_publisher(PointStamped, '/block_location', 10)

    def listener_callback(self, msg): 
        point = self.send_request('locobot/base_link', msg.data) 
        self.publisher.publish(point)

    def send_request(self, desired_frame, color): 
        self.req.desired_frame = desired_frame
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_client(self, self.future)
        result = self.future.result()
        if color == 'red':
            if result.red_present:
                return result.red_points[0]
        elif color == 'blue': 
            if result.blue_present: 
                return result.blue_points[0]
        elif color == 'yellow':
            if result.yellow_present:
                return result.yellow_points[0]
        elif color == 'green': 
            if result.green_present:
                return result.green_points[0]



def main(args=None):
    rclpy.init(args=args)
    perception_client = PerceptionClient()
    rclpy.spin(perception_client)
    perception_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
