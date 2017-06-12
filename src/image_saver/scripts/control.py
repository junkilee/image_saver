#!/usr/bin/env python
import rospy
from kobuki_msgs.msg import BumperEvent
from geometry_msgs.msg import Twist
from random import randint

image_index = 0
bumper_status = 0

def callback(data):
    global bumper_status
    rospy.loginfo("received a bumper message")
    bumper = data.bumper
    state = data.state
    rospy.loginfo("bumper ({}) state ({})".format(bumper, state))
    if state == BumperEvent.PRESSED:
        bumper_status = 1
    else:
        bumper_status = 0

def chooseDir(control_turn):
    num = randint(0,10)
    if num < 5:
        print("left\n")
        print(control_turn)
        return control_turn
    else:
        print("right\n")
        print(control_turn *(-1))
        return control_turn *(-1)

def chooseAngle(turn_length):
    num = randint(-10, 10)
    return turn_length + num

    
def run():
    global bumper_status

    rospy.init_node('turtlebot_control', anonymous=True)
    rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, callback)
    #pub = rospy.Publisher('~cmd_vel', Twist, queue_size = 20)
    #cmd_vel_mux/input/teleop
    pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size = 20)

    rate = rospy.Rate(15) # 15 Hz 1/15 sec

    control_speed = .3
    control_turn = .7
    current_turn = control_turn
    forward_length = 70
    turn_length = 30
    turn_on = 0
    move_back = 0
    forward = forward_length
    while not rospy.is_shutdown():
        if bumper_status == 1:
            turn_on = chooseAngle(turn_length)
            if current_turn < 0:
                print("turning right\n")
            else:
                print("turning left\n")

            move_back = 15


        if move_back > 0:
            move_back = move_back - 1
            twist = Twist()
            twist.linear.x = control_speed * -1; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            pub.publish(twist)
            rospy.loginfo("backing up..." + str(bumper_status))

        elif turn_on > 0:
            turn_on = turn_on - 1
            forward = forward_length
            twist = Twist()
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = current_turn
            pub.publish(twist)
            rospy.loginfo("turning..." + str(bumper_status))

        elif forward > 0:
            forward = forward -1
            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            pub.publish(twist)
            rospy.loginfo("forward..." + str(bumper_status))
        
        else: 
            current_turn = chooseDir(control_turn)
            turn_on = chooseAngle(turn_length)

        rate.sleep()

if __name__ == '__main__':
    run()
