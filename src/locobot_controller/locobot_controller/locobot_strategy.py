import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_msgs.msg import Header

class StrategyNode(Node): 

    def __init__(self): 
        super().__init__('strategy_node')
        self.picked_up_green = False
        self.picked_up_red = False
        self.picked_up_blue = False 
        self.desired_color = 'green' 
        self.color_publisher = self.create_publisher(String, 'desired_color', 10)
        self.picked_up_block_sub = self.create_subscription(Boolean, 'picked_up_block', self.picked_up_block_callback, 10) 
        self.dropped_off_block_sub = self.create_subscription(Boolean, 'dropped_off_block', self.dropped_up_block_callback, 10) 
        self.block_pose_sub = self.create_subscription(PointStamped, 'block_location', self.block_location_callback, 10) 
        self.target_pose_pub = self.create_publisher(PointStamped, 'target_pose', 10) 
        self.drop_off_point = (-1.0, -1.0, 0) 
        self.header = Header(stamp = rospy.Time.now(), frame_id='odom') 
        self.drop_off_point_stamped = PointStamped(header = self.header, point = self.drop_off_point)
        self.target_color = 'green'
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.get_block) 

    def get_block(self):
        msg = String(data = self.target_color) 
        self.color_publisher.publish(msg) 

    def block_location_callback(self, msg): 
        if (self.target_color == 'green'):
            if self.picked_up_green:
                self.target_pose_pub.publish(self.drop_off_point_stamped) 
            else: 
                self.target_pose_pub.publish(msg) 

        if (self.target_color == 'red'):
            if self.picked_up_red:
                self.target_pose_pub.publish(self.drop_off_point_stamped) 
            else: 
                self.target_pose_pub.publish(msg) 
        

        if (self.target_color == 'blue'):
            if self.picked_up_blue:
                self.target_pose_pub.publish(self.drop_off_point_stamped) 
            else: 
                self.target_pose_pub.publish(msg) 

    def pick_up_block_callback(self, msg):
        if (msg.data = True): 
            if (self.target_color == 'green'): 
                self.picked_up_green = True 
            if (self.target_color == 'blue'):
                self.picked_up_blue = True
            if (self.target_color == 'red'):
                self.picked_up_red = True

    def dropped_off_block_callback(self, msg): 
        if (msg.data = True):
            if self.target_color == 'green': 
                self.target_color = 'red'
            elif self.target_color == 'red':
                self.target_color == 'blue'
       


def main(args=None):
    rclpy.init(args=args)
    strategy_node = StrategyNode()
    rclpy.spin(strategy_node)
    strategy_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
