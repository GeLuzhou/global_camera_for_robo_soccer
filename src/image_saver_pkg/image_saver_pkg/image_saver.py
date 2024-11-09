import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageSaver(Node):
    def __init__(self):
        super().__init__('image_saver')

        # 获取保存路径参数，默认为当前目录
        self.declare_parameter('save_directory', '/home/coastz/ros2_ws/src/image_saver_pkg/data/')
        self.save_directory = self.get_parameter('save_directory').get_parameter_value().string_value

        # 如果目录不存在，创建该目录
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',  # 订阅 RealSense 的 RGB 图像话题
            self.listener_callback,
            10)
        self.subscription  # 避免未被使用的警告
        self.bridge = CvBridge()
        self.latest_image = None
        self.image_counter = 0

    def listener_callback(self, msg):
        # 使用 CvBridge 将ROS的Image消息转换为OpenCV格式
        self.latest_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.get_logger().info('Image received, waiting for input to save...')

        # 等待输入 'y' 来保存图片
        user_input = input("Input 'y' to save the image: ")
        if user_input.lower() == 'y':
            self.save_image()

    def save_image(self):
        if self.latest_image is not None:
            # 保存图片到指定目录，文件名为 image_x.jpg
            filename = os.path.join(self.save_directory, f'image_{self.image_counter}.jpg')
            cv2.imwrite(filename, self.latest_image)
            self.get_logger().info(f'Saved image as {filename}')
            self.image_counter += 1
        else:
            self.get_logger().info('No image to save')

def main(args=None):
    rclpy.init(args=args)
    image_saver = ImageSaver()
    rclpy.spin(image_saver)
    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
