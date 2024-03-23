### ME326_group3
To Run the perception and move_base nodes in terminals:
```
ros2 launch interbotix_xslocobot_sim xslocobot_gz_classic.launch.py robot_model:=locobot_wx250s use_lidar:=true hardware_type:=gz_classic
ros2 launch locobot_autonomy spawn_cube_launch.py
ros2 run locobot_autonomy move_locobot_base_action_server.py
ros2 run locobot_autonomy visual_block_perception_srv
ros2 run locobot_autonomy movebase_client_node.py
ros2 run locobot_autonomy locobot_perception.py
ros2 topic pub /desired_color std_msgs/msg/String "data: 'red'"
```

Milestone Demo:
see website: https://sites.google.com/stanford.edu/collaborative-robotics-group-3/home
