import obd, time
import serial.tools.list_ports


def get_Current_Speed():
    connection = obd.OBD()  # auto-connects to USB or RF port

    cmd = obd.commands.THROTTLE_POS  # select an OBD command (sensor)
    response = connection.query(cmd)  # send the command, and parse the response

    #current_speed = response. value.to("mph")
    print(response.value)

    return response


def get_Radar_Speed():
    radar_speed = "50"
    return radar_speed

def get_Target_Speed():
    target_speed = int(get_Radar_Speed()) + int(get_Current_Speed())
    print()
    return target_speed
