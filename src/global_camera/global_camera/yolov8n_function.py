from ultralytics import YOLO

#初始化yolo模型
def yolo_init():
    # 加载预训练的 YOLOv8 模型
    model = YOLO("/home/coastz/ros2_ws/src/global_camera/checkpoint/best.pt")
    return model

def detect_objects(model, frame):
    # 使用 YOLO 模型检测图像中的物体
    results = model(frame)
    
    # 获取检测结果
    length = len(results[0].boxes)
    detections = results[0].boxes.xyxy  # 获取边界框坐标
    labels = results[0].boxes.cls  # 获取类别标签
    names = [model.names[int(label)] for label in labels]  # 获取类别名称
    scores = results[0].boxes.conf  # 获取置信度分数    
    return length, detections, names, scores