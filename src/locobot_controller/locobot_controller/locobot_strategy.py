import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from std_msgs.msg import Header
from std_msgs.msg import Bool 

class StrategyNode(Node): 

    def __init__(self): 
        super().__init__('strategy_node')
        self.color_publisher = self.create_publisher(String, 'desired_color', 10)
        self.picked_up_block_sub = self.create_subscription(Bool, 'pick_block_response', self.picked_up_block_callback, 10) 
        self.dropped_off_block_sub = self.create_subscription(Bool, 'drop_block_response', self.dropped_off_block_callback, 10) 
        self.block_pose_sub = self.create_subscription(PointStamped, 'block_location', self.block_location_callback, 10) 
        self.target_pose_pub = self.create_publisher(PointStamped, 'target_pose', 10)
        self.block_arm_pose_pub = self.create_publisher(PoseStamped, 'pick_block', 10) 
        self.drop_block_pub = self.create_publisher(PoseStamped, 'drop_block', 10) 
        self.reach_block_sub = self.create_subscription(PoseStamped, 'reached_position', self.reached_position_callback, 10) 
        self.drop_off_point = Point()
        self.drop_off_point.x = -1.0
        self.drop_off_point.y = -1.0
        header = Header()
        self.drop_off_point_stamped = PointStamped(header = header, point = self.drop_off_point)
        self.target_color = 'green'
        self.reached_block = False
        self.has_block = False
        self.robot_pose = None

    def get_block(self, color):
        msg = String(data = color)
        self.target_color = color
        self.color_publisher.publish(msg)

    def reached_position_callback(self, msg):
        if (msg.data): 
            if has_block:
                self.drop_block_pub.publish(msg) 
            else: 
                self.reached_block = True 
                self.get_block(self.target_color) 
        

    def block_location_callback(self, msg):
        if self.reached_block == False: 
            self.target_pose_pub.publish(msg) 
        elif self.reached_block == True: 
            block_pose = PoseStamped()
            block_pose.Pose.Point = msg.Point
            block_pose.Pose.Orientation = self.robot_pose.Orientation
            self.block_arm_pose_pub.publish(msg) 
            self.reached_block = False

    def picked_up_block_callback(self, msg):
        if (msg.data): 
            self.has_block = True
            self.target_pose_pub.publish(self.drop_off_point_stamped) 

    def dropped_off_block_callback(self, msg): 
        if (msg.data):
            if self.target_color == 'green': 
                self.target_color = 'red'
                self.get_block('red') 
            elif self.target_color == 'red':
                self.target_color == 'blue'
                self.get_block('blue') 
        self.has_block = False
       


def main(args=None):
    rclpy.init(args=args)
    strategy_node = StrategyNode()
    strategy_node.get_block('green')
    rclpy.spin(strategy_node)
    strategy_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
