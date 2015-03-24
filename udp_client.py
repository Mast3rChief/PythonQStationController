import socket
import sys
import json


class UdpClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None

    def send_request(self, cmd):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((self.ip, self.port))

            if sys.version_info < (3, 0):
                self.sock.sendall(cmd)
                data = self.sock.recvfrom(2048)
                self.sock.close()

                print(cmd + ' : ' + data[0])

                return data[0]
            else:
                self.sock.sendall(cmd.encode('UTF-8'))
                data = self.sock.recv(2048)
                self.sock.close()

                print(cmd + ' : ' + str(data.decode('UTF-8')))

                return str(data.decode('UTF-8'))
        except:
            print('UDP Connection Error: ', sys.exc_info()[0])
            raise

    def set_light(self, bright, red, green, blue, status, active_bulb):
        cmd = '{"cmd":"light_ctrl",' \
              '"r":"' + str(red) + '",' \
              '"g":"' + str(green) + '",' \
              '"b":"' + str(blue) + '",' \
              '"bright":"' + str(bright) + '",' \
              '"effect":"9",' \
              '"iswitch":"' + str(status) + '",' \
              '"matchValue":"0",' \
              '"sn_list":[' \
              '{"sn":"' + active_bulb + '"}' \
              ']}'

        data = self.send_request(cmd)

    def set_title(self, sn, title):
        cmd = '{"cmd":"set_title","sn":"' + sn + '","title":"' + title + '"}'

        data = self.send_request(cmd)

    def get_lights(self):
        cmd = '{"cmd":"light_list"}'

        data = self.send_request(cmd)

        try:
            json_data = json.loads(data)

            return json_data
        except:
            print('JSON Parsing Error: ', sys.exc_info()[0])
            raise
