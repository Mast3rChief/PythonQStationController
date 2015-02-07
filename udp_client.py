import socket
import json


class UdpClient:
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port

    def send_request(self, cmd):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(cmd, (self.__ip, self.__port))
            data = sock.recvfrom(1024)

            print 'Command: ' + cmd
            print 'Answer: ' + data[0]

            return data[0]
        except ValueError:
            pass

    def set_light(self, bright, red, green, blue, active_bulb):
        cmd = '{"cmd":"light_ctrl","bright":"' + str(bright) + '","g":"' + str(green) + '","model":"6","b":"' + str(blue) + '","effect":"9","r":"' + str(red) + '","sn_list":[{"sn":"' + active_bulb + '"}],"matchValue":"0","isSwitch":"1"}'

        data = self.send_request(cmd)

    def get_lights(self):
        cmd = '{"cmd":"light_list"}'

        data = self.send_request(cmd)
        json_data = json.loads(data)

        return json_data