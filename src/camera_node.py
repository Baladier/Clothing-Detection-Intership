#!/usr/bin/env python3
"""Publish frames from a USB/webcam device as sensor_msgs/Image messages."""

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def main():
    rospy.init_node('camera_node', anonymous=True)

    camera_index = rospy.get_param('~camera_index', 0)
    image_topic = rospy.get_param('~image_topic', '/image_output')
    fps = rospy.get_param('~fps', 10)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        rospy.logerr("Could not open camera at index %s", camera_index)
        return

    pub = rospy.Publisher(image_topic, Image, queue_size=15)
    bridge = CvBridge()
    rate = rospy.Rate(fps)

    rospy.loginfo("Publishing camera %s on %s at %s Hz", camera_index, image_topic, fps)

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            rospy.logwarn("Failed to read a frame from the camera")
            break

        try:
            # OpenCV delivers frames in BGR, so that is the correct encoding.
            # Labelling them "rgb8" swaps the red and blue channels downstream.
            ros_image = bridge.cv2_to_imgmsg(frame, "bgr8")
            ros_image.header.stamp = rospy.Time.now()
            ros_image.header.frame_id = "camera"
            pub.publish(ros_image)
        except CvBridgeError as e:
            rospy.logerr(e)

        rate.sleep()

    cap.release()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
