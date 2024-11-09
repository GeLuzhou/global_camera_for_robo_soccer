import numpy as np
import pyrealsense2 as rs

# 初始化 RealSense 相机
def realsense_init():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    pipeline.start(config)
    return pipeline

# 读取 RealSense 图像帧
def read_realsense_frame(pipeline):
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    if not color_frame or not depth_frame:
        raise ValueError("Could not read frames from RealSense camera")

    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    return color_image, depth_image

def read_intrinsics(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        print(repr(line))

    # 找到内参数矩阵和畸变系数的起始行
    start_matrix_idx = None
    start_dist_idx = None
    
    for idx, line in enumerate(lines):
        if "内参数矩阵 (mtx):" in line:
            start_matrix_idx = idx + 1
        if "畸变系数 (dist):\n" in line:
            start_dist_idx = idx + 1
            break

    if start_matrix_idx is None:
        raise ValueError("未找到内参数矩阵 (mtx)")
    if start_dist_idx is None:
        raise ValueError("未找到畸变系数 (dist)")

    # 读取内参数矩阵和畸变系数的值
    K_matrics = []
    dist = []
    for i in range(3):
        K_matrics.append([float(x) for x in lines[start_matrix_idx + i].strip().split()])
    dist = [float(x) for x in lines[start_dist_idx].strip().split()]

    return np.array(K_matrics), np.array(dist)

