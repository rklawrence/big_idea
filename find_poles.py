import odrive
from time import sleep

odrv0 = odrive.find_any()
try:
    odrv0.reboot()
except Exception:
    pass
sleep(2)


for pole_pair in range(1, 100):
    odrv0 = odrive.find_any()
    odrv0.axis0.motor.config.pole_pairs = pole_pair
    odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    sleep(10)
    error_message = odrv0.axis0.encoder.error
    if error_message == 0:
        print(f"Success: {pole_pair}")
        break
    try:
        odrv0.reboot()
    except Exception:
        pass
    print(f"Fail: {pole_pair}\nError message: {error_message}")
    sleep(2)


