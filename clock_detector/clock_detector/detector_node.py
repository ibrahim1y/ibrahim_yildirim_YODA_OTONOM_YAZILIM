import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO

class ClockDetectorNode(Node):
    def __init__(self):
        super().__init__('clock_detector_node')
        self.publisher_ = self.create_publisher(Image, 'clock_detections', 10)
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO('yolov8n.pt') 
        self.bridge = CvBridge()
        timer_period = 0.033  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info('Canlı Duvar Saati Algılama Nodu Başlatıldı!')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error('Kameradan görüntü alınamadı!')
            return

        results = self.model(frame, classes=[74], verbose=False)
        annotated_frame = results[0].plot()
        msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding="bgr8")
        self.publisher_.publish(msg)

    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ClockDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()