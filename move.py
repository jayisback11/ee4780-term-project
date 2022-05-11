from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import serial

vehicle = connect("/dev/ttyACM1", wait_ready=True)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=10)

# THIS FUNCTION IS RESPONSIBLE OF MOVING THE DRONE WHEN CALLED
def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

f = open("commands.txt", "w")
f.write("ready")
f.close()

x = 0
isAutoOn = False

while True:
    print(vehicle.location.global_relative_frame.alt)
    data = arduino.readline().decode("utf-8", "ignore")
    if "Auto" in data:
        isAutoOn = True
        break

while True:
    print(vehicle.location.global_relative_frame.alt)

    if isAutoOn:
        if x == 0:
            vehicle.mode = VehicleMode("GUIDED")
            x = x+1

        f = open("commands.txt", "r")
        command = f.read()
        f.close()

        # read the command from commands.txt and move the drone
        if "command" in command:
            f = open("commands.txt", "w")

            if "RIGHT" in command:
                send_body_ned_velocity(0, 0.2, 0, 1)
                print("RIGHT")
            elif "LEFT" in command:
                print("LEFT")
                send_body_ned_velocity(0, -0.2, 0, 1)
            elif "FORWARD" in command:
                print("FORWARD")
                send_body_ned_velocity(0.2, 0, 0, 1)
            elif "BACKWARD" in command:
                print("BACKWARD")
                send_body_ned_velocity(-0.2, 0, 0, 1)
            elif "LAND" in command:
                # if the altitude is less than 4 then release the payload
                if vehicle.location.global_relative_frame.alt < 4:
                    print("BRAKE MODE...")
                    vehicle.mode = VehicleMode("BRAKE")
                    time.sleep(1)
                    arduino.write(bytes('YES\n').encode('utf-8'))
                    print("OPENING PAYLOAD MECHANISM...")
                    time.sleep(2)
                    print("LOITER MODE...")
                    vehicle.mode = VehicleMode("LOITER")
                    break
                else:
                    send_body_ned_velocity(0, 0, 0.2, 1)
                    print("DESCEND")

            time.sleep(1)
            f.write("ready")
            f.close()
        else:
            print("WAITING FOR COMMAND...")
            time.sleep(1)