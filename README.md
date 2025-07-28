# rgbd_camera_issue

This package provides a minimal, reproducible example to help investigate a suspected issue with the `rgbd_camera` plugin in Gazebo Harmonic. It demonstrates a potential misalignment between the `CameraInfo` and `PointCloud2` messages.

---

### Problem Description

When using the `rgbd_camera` plugin in Gazebo Harmonic, the `sensor_msgs/msg/CameraInfo` and `sensor_msgs/msg/PointCloud2` messages are published with the same frame ID (`rgbd_camera_link`), but they **do not align visually** in RViz:

see:
<img width="996" height="886" alt="Image" src="https://github.com/user-attachments/assets/3eebd632-e6c5-4283-a091-80908b48a865" />
<img width="1840" height="1027" alt="Image" src="https://github.com/user-attachments/assets/42c8e654-719d-48f5-98ea-2ac27ec0f5ea" />
<img width="892" height="567" alt="image" src="https://github.com/user-attachments/assets/aaebab58-0c5e-410b-b4ab-cb34ec175a8d" />

This misalignment suggests that the **camera intrinsic parameters** or the **depth projection matrix** used for generating the point cloud is not consistent with the `camera_info` message.

---

### Observations

* `frame_id` for both topics: `rgbd_camera_link`
* Intrinsics (focal lengths and principal point) in `camera_info` are valid and match the expected values
* The `rgb` field is populated in the point cloud
* All transforms seem valid and static between world → camera → sensor

---

### Expected Behavior

The point cloud should be generated using the same intrinsics as reported in `camera_info`, and both should appear spatially aligned in RViz.


---

> **Note:**  
> All of the above assumes correct usage of the plugin and RViz configuration. If there is a mistake in my setup or understanding, please let me know.

