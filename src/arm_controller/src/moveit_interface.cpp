#include "interbotix_moveit_interface/moveit_interface_obj.hpp"
#include <iostream>
#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <Eigen/Dense>
#include <Eigen/Geometry>
#include <cmath>
#include "geometry_msgs/msg/pose_stamped.h"
#include "geometry_msgs/msg/point.hpp"
#include "std_msgs/msg/bool.hpp"


class MyNode : public rclcpp::Node {
public:
    MyNode()
    : Node("interbotix_moveit_node") {
        rclcpp::NodeOptions node_options;
        node_options.automatically_declare_parameters_from_overrides(true);
        auto node = std::make_shared<rclcpp::Node>("interbotix_moveit_node", node_options);
        geometry_msgs::msg::PoseStamped target_pose;
        target_pose.pose.position.x = 0.451367;
        target_pose.pose.position.y = 0.09671;
        target_pose.pose.position.z = 0.02;
        Eigen::Vector3d v(0, 1, 0); // pitch about y-axis


        // Define the rotation angle
        double th = 90 * M_PI / 180.0; 
        Eigen::Quaterniond q;
        q = Eigen::AngleAxisd(th, Eigen::Vector3d::UnitY());
        target_pose.pose.orientation.x = v(0) * std::sin(th / 2);
        target_pose.pose.orientation.y = v(1) * std::sin(th / 2);
        target_pose.pose.orientation.z = v(2) * std::sin(th / 2);
        target_pose.pose.orientation.w = std::cos(th / 2);

        subscription_pick_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
            "pick_block", 10, std::bind(&MyNode::pick_callback, this, target_pose));

        subscription_drop_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
            "drop_block", 10, std::bind(&MyNode::drop_callback, this, target_pose));

        publisher_pick_ = this->create_publisher<std_msgs::msg::Bool>("pick_block_response", 10);

        publisher_drop_ = this->create_publisher<std_msgs::msg::Bool>("drop_block_response", 10);
        
    }

    void pick_callback(geometry_msgs::msg::PoseStamped target_pose) const {
        target_pose.pose.position.z = 0.02;
        Eigen::Vector3d v(0, 1, 0); // pitch about y-axis
        // Define the rotation angle
        double th = 90 * M_PI / 180.0; 
        Eigen::Quaterniond q;
        q = Eigen::AngleAxisd(th, Eigen::Vector3d::UnitY());
        target_pose.pose.orientation.x = v(0) * std::sin(th / 2);
        target_pose.pose.orientation.y = v(1) * std::sin(th / 2);
        target_pose.pose.orientation.z = v(2) * std::sin(th / 2);
        target_pose.pose.orientation.w = std::cos(th / 2);
        moveit_interface_->moveit_set_arm_target_values("Home");
        moveit_interface_->moveit_open_gripper();
        moveit_interface_->moveit_plan_ee_pose(target_pose.pose);
        moveit_interface_->moveit_execute_plan();
        moveit_interface_->moveit_close_gripper();
        moveit_interface_->moveit_set_arm_target_values("Home");
        auto message_pick = std_msgs::msg::Bool();
        message_pick.data = true;
        publisher_pick_->publish(message_pick);
    }

    void drop_callback(geometry_msgs::msg::PoseStamped target_pose) const {
        // This is a placeholder for the drop logic, which should be different from the pick logic.
        // Assuming the drop logic involves moving to a drop position and opening the gripper.
        // You may need to adjust this logic based on your specific requirements.

        // Example drop logic (you need to customize this):
        target_pose.pose.position.z = 0.02; // Adjust the drop height as necessary.
        // No need to adjust orientation for the drop; assuming it's the same as after picking.

        moveit_interface_->moveit_set_arm_target_values("Home"); // Assuming "DropPosition" is a predefined pose.
        moveit_interface_->moveit_plan_ee_pose(target_pose.pose);
        moveit_interface_->moveit_execute_plan();
        moveit_interface_->moveit_open_gripper(); // Release the object.
        moveit_interface_->moveit_set_arm_target_values("Home"); // Return to "Home" position.
        auto message_drop = std_msgs::msg::Bool();
        message_drop.data = true;
        publisher_drop_->publish(message_drop);
    }
    

private:
    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr subscription_pick_;
    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr subscription_drop_;
    std::shared_ptr<interbotix::InterbotixMoveItInterface> moveit_interface_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr publisher_pick_;
    rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr publisher_drop_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyNode>());
    rclcpp::shutdown();
    return 0;
}
