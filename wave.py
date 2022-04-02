import odrive
from time import sleep, time
from pynput.keyboard import Listener, Key

SLEEP_TIME = 1
SPEED = 1.2
moving = True

def startup(controller):
    print("calibrating")
    controller.axis0.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    sleep(15)

def wave(controller):
    input("Press Enter to Start\n")
    controller.axis0.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
    controller.axis0.controller.config.input_filter_bandwidth = 2.0
    controller.axis0.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL

    speed = -SPEED
    controller.axis0.controller.input_vel = speed
    sleep(SLEEP_TIME)
    state = "right"
    global moving
    moving = True
    while moving:
        if state == "left":
            speed = -SPEED * 1.1
            state = "right"
        elif state == "right":
            speed = SPEED
            state = "left"
        else:
            speed = 0
            moving = False
        controller.axis0.controller.input_vel = speed
        sleep(2 * SLEEP_TIME)
    controller.axis0.controller.config.control_mode = odrive.enums.CONTROL_MODE_POSITION_CONTROL
    controller.axis0.controller.input_pos = 0
    sleep(.25)
    controller.axis0.requested_state = odrive.enums.AXIS_STATE_IDLE


def trajectory_wave(controller):
    input("Press Enter to Start\n")
    controller.axis0.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
    controller.axis0.controller.config.input_filter_bandwidth = 2.0
    controller.axis0.controller.config.input_mode = odrive.enums.INPUT_MODE_TRAP_TRAJ
    distance = 1
    global moving
    moving = True
    target_position = 0
    state = "right"
    while moving:
        if state == "left":
            target_position = -distance
            state = "right"
        elif state == "right":
            target_position = distance

            state = "left"
        else:
            moving = False
            target_position = 0
        controller.axis0.controller.input_pos = target_position
        sleep(SLEEP_TIME)

    controller.axis0.controller.config.control_mode = odrive.enums.CONTROL_MODE_POSITION_CONTROL
    controller.axis0.controller.input_pos = 0
    sleep(.25)
    controller.axis0.requested_state = odrive.enums.AXIS_STATE_IDLE

def on_release(key):
    if key == Key.esc:
        global moving
        moving = False

def on_press(key):
    pass

if __name__ == "__main__":
    print("Starting")
    with Listener(on_release=on_release, on_press=on_press) as listener:
        controller = odrive.find_any()
        print(controller)
        startup(controller) 
    
        while True:
            trajectory_wave(controller)
