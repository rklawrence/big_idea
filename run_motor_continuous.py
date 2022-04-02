import odrive
from time import sleep

odrv0 = odrive.find_any()
try:
    odrv0.reboot()
except Exception:
    pass
sleep(2)
odrv0 = odrive.find_any()
odrv0.axis1.motor.config.pole_pairs = 20
odrv0.axis1.motor.config.motor_type = odrive.enums.MOTOR_TYPE_HIGH_CURRENT
odrv0.axis1.config.enable_watchdog = False
odrv0.axis1.controller.config.vel_limit = 20
odrv0.axis1.controller.config.vel_gain = 0.32
odrv0.axis1.controller.config.vel_integrator_gain = 0.0
odrv0.axis1.clear_errors()
odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
sleep(15)
# odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_ENCODER_INDEX_SEARCH
# sleep(5)
print("Updating state")
odrv0.axis1.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL
sleep(5)
print("moving")
moving = True
odrv0.axis1.controller.config.input_filter_bandwidth = 2.0
odrv0.axis1.controller.config.control_mode = odrive.enums.CONTROL_MODE_VELOCITY_CONTROL
speed = 1
while moving:
    input_val = input("f = forward\nb = backward\notherwise stop\n")
    if input_val == "f":
        odrv0.axis1.controller.input_vel = speed
    elif input_val == "b":
        odrv0.axis1.controller.input_vel = -speed
    else:
        odrv0.axis1.controller.input_vel = 0
        moving = False
