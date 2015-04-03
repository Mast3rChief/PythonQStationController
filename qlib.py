from udp_client import *
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

                # print(cmd + ' : ' + data[0])

                return data[0]
            else:
                self.sock.sendall(cmd.encode('UTF-8'))
                data = self.sock.recv(2048)
                self.sock.close()

                # print(cmd + ' : ' + str(data.decode('UTF-8')))

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

    def get_groups(self):
        cmd = '{"cmd":"group_list"}'

        data = self.send_request(cmd)

        try:
            json_data = json.loads(data)

            return json_data
        except:
            print('JSON Parsing Error: ', sys.exc_info()[0])
            raise

    def get_group_lights(self, group_id):
        cmd = '{"cmd":"group_leds_list",' \
              '"group_id":"' + group_id + '"}'

        data = self.send_request(cmd)

        try:
            json_data = json.loads(data)

            return json_data
        except:
            print('JSON Parsing Error: ', sys.exc_info()[0])
            raise

class QStation:
	PORT = 11600
	def __init__(self):
		self.ip = '0'
		self.bulb = []
		self.group = []
		self.group_elements = []
		try:
			self.ip = socket.gethostbyname('bellnet')
		except:
			print 'Error', 'Could not find QStation!'

		self.get_bulbs(self.ip)
		self.get_groups(self.ip)

	def get_bulbs(self, ip):
		self.udp_client = UdpClient(self.ip, self.PORT)
		self.output = self.udp_client.get_lights()
		
		bulb_num = len(self.output['led'])
		self.bulbs = [Bulb(self.output['led'][i]) for i in range(bulb_num)]

	def get_groups(self, ip):
		self.udp_client = UdpClient(self.ip, self.PORT)
		self.groups = self.udp_client.get_groups()

		group_num = len(self.groups['data'])
		self.group = [Group(self.groups['data'][i], self.udp_client.get_group_lights(self.groups['data'][i]['group_id'])['data']) for i in range(group_num)]

	def show(self):
		for item in self.bulbs:
			item.show()

		for item in self.group:
			item.show()

class Group:
	def __init__(self, settings, elements):
		self.settings = settings
		self.elements = []
		for bulb in elements:
			if 'status' in bulb and bulb['status'] == '1':
				self.elements.append(bulb['sn'])

	def get_list(self):

	def add2list(self, sn):

	def rmv(self, sn):

	def switch(self, bright, angle):

	def switch_status(self):

	def show(self):
		print self.settings['group_id'], self. settings['group_title']
		print self.elements

class Bulb:
	def __init__(self, settings):
		self.settings = settings

	def switch(self, bright, angle):

	def switch_status(self):

	def show(self):
		print self.settings['sn'], self.settings['title']