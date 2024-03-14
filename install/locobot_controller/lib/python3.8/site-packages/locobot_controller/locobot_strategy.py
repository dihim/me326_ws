import rclpy
from rclpy.node import Node


class StrategyNode(Node): 

    def __init__(self): 
        super().__init__('strategy_node')



def main(args=None):
    rclpy.init(args=args)
    strategy_node = StrategyNode()
    rclpy.spin(strategy_node)
    strategy_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
