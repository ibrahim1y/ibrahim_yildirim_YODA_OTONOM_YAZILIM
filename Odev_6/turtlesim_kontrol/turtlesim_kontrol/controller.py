import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 2.0  # İleri doğru hız
        msg.angular.z = 1.0 # Kendi ekseninde dönüş hızı
        self.publisher_.publish(msg)
        self.get_logger().info(f'Hız gönderiliyor: Linear={msg.linear.x}, Angular={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
