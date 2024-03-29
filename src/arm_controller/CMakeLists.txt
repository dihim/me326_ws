cmake_minimum_required(VERSION 3.5)
project(arm_controller)

if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(interbotix_moveit_interface_msgs REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(moveit_visual_tools REQUIRED)
find_package(gazebo_ros_link_attacher REQUIRED)
find_package(rclcpp REQUIRED)

set(
  MOVEIT_INTERFACE_DEPENDENCIES
    interbotix_moveit_interface_msgs
    moveit_msgs
    geometry_msgs
    moveit_ros_planning_interface
    moveit_visual_tools
    rclcpp
    gazebo_ros_link_attacher
)

###########
## Build ##
###########

include_directories(
  include
)

add_executable(arm_controller src/moveit_interface.cpp src/moveit_interface_obj.cpp)
ament_target_dependencies(arm_controller ${MOVEIT_INTERFACE_DEPENDENCIES})

#############
## Install ##
#############

install(
  TARGETS
    arm_controller
  DESTINATION
    lib/${PROJECT_NAME}
)

# Install Python executables
install(
  PROGRAMS
    scripts/moveit_interface_gui
    # scripts/moveit_python_interface
  DESTINATION
    lib/${PROJECT_NAME}
)

# Install launch files.
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install URDF files
install(DIRECTORY model
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
