from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Path to RViz config file (customize if you want a specific view/layout)
    pkg_kinisi_gazebo = get_package_share_directory("kinisi_gazebo")

    rviz_config_path = os.path.join(pkg_kinisi_gazebo, "config", "rgbd_camera.rviz")

    # Print the path to help with debugging
    print(f"Looking for RViz config at: {rviz_config_path}")

    world_file = os.path.join(pkg_kinisi_gazebo, "worlds", "camera.world")

    gz_args = f"-r {world_file}"
    bridge_params = PathJoinSubstitution(
        [
            FindPackageShare("kinisi_gazebo"),
            "config",
            "gz_bridge_rgbd.yaml",
        ]
    )
    return LaunchDescription(
        [
            # Static transform from world to rgbd_camera
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="static_tf_rgbd_camera",
                arguments=[
                    "--x",
                    "0",
                    "--y",
                    "0",
                    "--z",
                    "0.5",
                    "--roll",
                    "0",
                    "--pitch",
                    "0",
                    "--yaw",
                    "0",
                    "--frame-id",
                    "world",
                    "--child-frame-id",
                    "rgbd_camera_link",
                ],
                parameters=[{"use_sim_time": True}],
            ),
            # Launch RViz with RGBD camera config
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", rviz_config_path],
                parameters=[{"use_sim_time": True}],
                output="screen",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
                    )
                ),
                launch_arguments=[
                    ("gz_args", gz_args),
                    ("use_sim_time", "true"),
                ],
            ),
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="gz_ros2_bridge",
                output="screen",
                arguments=[
                    "--ros-args",
                    "-p",
                    ["config_file:=", bridge_params],
                ],
            ),
        ]
    )
