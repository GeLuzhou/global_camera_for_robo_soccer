# global_camera_for_robo_soccer

## global_camera

- 全局相机功能包
- yolo

## image_saver_pkg

- 采数据功能包

## interface

- 自定义话题/服务功能包
- TeamPosition.msg
```
# 球的位置
geometry_msgs/Point ball_position

# 红队防守狗的位置
geometry_msgs/Point red_defense_dog_position

# 红队进攻狗的位置
geometry_msgs/Point red_attack_dog_position

# 蓝队防守狗的位置
geometry_msgs/Point blue_defense_dog_position

# 蓝队进攻狗的位置
geometry_msgs/Point blue_attack_dog_position
```