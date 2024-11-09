import sys
sys.path.append('/home/coastz/.conda/envs/yolo/lib/python3.8/site-packages/') 
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from global_camera.realsense_function import realsense_init, read_realsense_frame
from global_camera.yolov8n_function import yolo_init, detect_objects
from interface.msg import TeamPosition    


class GlobalCameraNode(Node):
    def __init__(self):
        super().__init__('global_camera_node')

        # 初始化 YOLOv8 模型
        self.yolov8n = yolo_init()

        # 初始化 CvBridge，负责将ROS消息转换为OpenCV图像
        self.bridge = CvBridge()

        # 创建发布器，用于发布带有检测框的图像
        self.image_publisher = self.create_publisher(Image, 'global_camera_detection', 10)
        self.pos_poblisher = self.create_publisher(TeamPosition, 'team_positions', 10)
        self.camera_image_sub = self.create_subscription(
            Image,
            "/camera/camera/color/image_raw",
            self.image_callback,
            10
        )

    def image_callback(self, msg):
        # 读取RealSense图像（一帧）
        color_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # 将图像从BGR格式转换为RGB格式
        rgb_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # 使用 YOLO 模型检测图像中的物体
        length, detections, names, scores = detect_objects(self.yolov8n, rgb_frame)

        # 获取物体在战术板上的位置
        positions_on_tactical_board = self.get_tactical_board(color_image, detections, names, length)

        # for position in positions_on_tactical_board:
        #     if position['name'] == 'blue_defender':
        #         TeamPositions.blue_defense_dog_position = position['tactical_coords']
        #     elif position['name'] == 'blue_attacker':
        #         TeamPositions.blue_attack_dog_position = position['tactical_coords']
        #     elif position['name'] == 'red_defender':
        #         TeamPositions.red_defense_dog_position = position['tactical_coords']
        #     elif position['name'] == 'red_attacker':
        #         TeamPositions.red_attack_dog_position = position['tactical_coords']
        #     elif position['name'] == 'ball':
        #         TeamPositions.ball_position = position['tactical_coords']

        # self.pos_poblisher.publish(TeamPositions)
        
        # 将OpenCV图像转换为ROS消息并发布
        ros_image = self.bridge.cv2_to_imgmsg(color_image, encoding='bgr8')
        self.image_publisher.publish(ros_image)

    def get_tactical_board(self, color_image, detections, names, length):
        # 定义透视变换的四个源点和目的地坐标
        pts_src = np.array([[204, 143], [375, 136], [201, 305], [387, 298]])
        pts_dst = np.array([[0, 0], [1, 0], [0, 0.95], [1, 0.95]])

        # 获取透视变换矩阵
        M = cv2.getPerspectiveTransform(pts_src.astype(np.float32), pts_dst.astype(np.float32))

        positions_on_tactical_board = []
        for i in range(length):
            x1, y1, x2, y2 = map(int, detections[i])
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            name = names[i]

            # 将图像中的目标坐标转换为战术板坐标
            target_pixel_coords = np.array([[x, y]], dtype='float32')
            target_pixel_coords = np.array([target_pixel_coords])
            target_tactical_coords = cv2.perspectiveTransform(target_pixel_coords, M)

            target = {
                'name': name,
                'tactical_coords': target_tactical_coords[0][0]
            }
            positions_on_tactical_board.append(target)

            # 在图像上绘制检测框和中心点
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(color_image, f"{name} : ({target_tactical_coords[0][0][0]:.2f}, {target_tactical_coords[0][0][1]:.2f})",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return positions_on_tactical_board


def main(args=None):
    rclpy.init(args=args)
    node = GlobalCameraNode()
    rclpy.spin(node)
    node.pipeline.stop()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
