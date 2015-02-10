import socket
import sys
import json


class UdpClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def send_request(self, cmd):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(cmd, (self.ip, self.port))
            data = sock.recvfrom(1024)

            print 'Command: ' + cmd
            print 'Answer: ' + data[0]

            return data[0]
        except:
            print 'UDP Connection Error: ', sys.exc_info()[0]
            raise

    def set_light(self, bright, red, green, blue, active_bulb):
        cmd = '{"cmd":"light_ctrl","bright":"' + str(bright) + '","g":"' + str(green) + '","b":"' + str(blue) + '","effect":"9","r":"' + str(red) + '","sn_list":[{"sn":"' + active_bulb + '"}],"matchValue":"0","iswitch":"1"}'

        data = self.send_request(cmd)

    def get_lights(self):
        cmd = '{"cmd":"light_list"}'

        data = self.send_request(cmd)

        try:
            json_data = json.loads(data)

            return json_data
        except:
            print 'JSON Parsing Error: ', sys.exc_info()[0]
            raise

    def set_title(self, sn, title):
        cmd = '{"cmd":"set_title","sn":"' + sn + '","title":"' + title + '"}'

        data = self.send_request(cmd)

        try:
            json_data = json.loads(data)

            return json_data
        except:
            print 'JSON Parsing Error: ', sys.exc_info()[0]
            raise