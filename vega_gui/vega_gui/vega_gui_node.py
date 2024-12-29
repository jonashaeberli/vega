import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class VegaGuiNode(Node):
    def __init__(self):
        super().__init__('vega_gui_node')
        self.publisher = self.create_publisher(String, 'example_topic', 10)
        self.subscription = self.create_subscription(
            String,
            'example_response_topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.response_data = None

    def publish_message(self, message):
        msg = String()
        msg.data = message
        self.publisher.publish(msg)
        self.get_logger().info(f'Published message: {message}')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received message: {msg.data}')
        self.response_data = msg.data
