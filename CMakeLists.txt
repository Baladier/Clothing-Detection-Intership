cmake_minimum_required(VERSION 3.0.2)
project(clothing_detection)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  sensor_msgs
  cv_bridge
  message_generation
)

add_message_files(
  FILES
  Box.msg
  BoxArray.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs sensor_msgs cv_bridge message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  src/camera_node.py
  src/clothing_detector_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
