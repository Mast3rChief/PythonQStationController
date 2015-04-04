from udp_client import *
import socket
import sys
import json

try:
	IP = socket.gethostbyname('bellnet')
	PORT = 11600
except:
	print 'Error', 'Could not find QStation!'

class UdpClient:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = None

	def send_cmd(self, cmd):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.connect((self.ip, self.port))

			if sys.version_info < (3, 0):
				self.sock.sendall(cmd)
				data = self.sock.recvfrom(2048)
				self.sock.close()

				# print(cmd + ' : ' + data[0])

				return json.loads(data[0])
			else:
				self.sock.sendall(cmd.encode('UTF-8'))
				data = self.sock.recv(2048)
				self.sock.close()

				# print(cmd + ' : ' + str(data.decode('UTF-8')))

				return json.loads(data.decode('UTF-8'))
		except:
			print('UDP Connection Error: ', sys.exc_info()[0])
			raise

	def set_light(self, *arguments):
		cmd =	'{"cmd":"light_ctrl",' \
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
		return self.send_cmd(cmd)

	def set_title(self, sn, title):
		cmd = '{"cmd":"set_title","sn":"' + sn + '","title":"' + title + '"}'
		return self.send_cmd(cmd)

	def get_lights(self):
		cmd = '{"cmd":"light_list"}'
		return self.send_cmd(cmd)

	def get_groups(self):
		cmd = '{"cmd":"group_list"}'
		return self.send_cmd(cmd)

	def get_group_lights(self, group_id):
		cmd =	'{"cmd":"group_leds_list",' \
				'"group_id":"' + group_id + '"}'
		return self.send_cmd(cmd)

	def set_group(self, *arguments):
		cmd =	'{"cmd":"<cmdValue>",' \
				'"r":"<redValue>",' \
				'"g":"<greenValue>",' \
				'"b":"blueValue",' \
				'"bright": "<lightValue>",' \
				'"effect": "<effectValue>", ' \
				'"angle": "colorAngle", ' \
				'"sn_list": [ { "sn": "<xxx>" } ], ' \
				'"matchValue": "<value>", ' \
				'"iswitch": "<ledStatus>", ' \
				'"group1": "<group1Value>", ' \
				'"angle": "colorValue"}'
		return self.send_cmd(cmd)

	def create_group(self, group_title):
		cmd =	'{"cmd":" cmdValue",' \
				'"group_title":"' + group_title + '"}'
		return self.send_cmd(cmd)

	def delete_group(self, group_id):
		cmd =	'{"cmd":"del_group",' \
				'"group_id":"' + group_id + '"}'
		return self.send_cmd(cmd)

	def add_light2group(self, sn, group_id):
		cmd =	'{"cmd":"set_group",' \
				'"sn":"' + sn + '",' \
				'"group_id":"' + group_id + '"}'
		return self.send_cmd(cmd)

	def rmv_light(self, sn, group_id):
		cmd =	'{"cmd":" leave_group ",' \
				'"sn":"' + sn + '",' \
				'"group_id":"' + group_id + '"}'
		return self.send_cmd(cmd)

	def rename_group(self, sn, group_title):
		cmd =	'{"cmd":" set_group_title ",' \
				'"sn":"' + sn + '",' \
				'"group_title":"' + group_title + '"}'
		return self.send_cmd(cmd)



class QStation:
	def __init__(self):
		self.ip = '0'
		self.bulb = []
		self.group = []
		self.group_elements = []
		self.udp_client = UdpClient(IP, PORT)
		self.get_bulbs()
		self.get_groups()

	def get_bulbs(self):
		self.output = self.udp_client.get_lights()
		print self.output['led'][1]
		self.bulbs = [Bulb(self.output['led'][i]) for i in range(len(self.output['led']))]

	def get_groups(self):
		self.groups = self.udp_client.get_groups()
		self.group = [Group(self.groups['data'][i], self.udp_client.get_group_lights(self.groups['data'][i]['group_id'])['data']) for i in range(len(self.groups['data']))]

	def create_group(self, name):
		self.udp_client.create_group(name)
		self.get_groups()

	def delete_group(self, id):
		self.group[id].delete()

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
		self.udp_client = UdpClient(IP, PORT)

	def get_list(self):
		return self.elements

	def add_bulb2list(self, sn):
		self.udp_client.add_light2group(sn, self.settings['group_id'])

	def rmv_blub(self, sn):
		self.udp_client.rmv_light(sn, self.settings['group_id'])

	def switch(self, bright, angle):
		self.udp_client.set_group([bright, angle])

	def switch_status(self):
		return True

	def show(self):
		print self.settings['group_id'], self.settings['group_title']
		print self.elements

	def delete(self):
		self.udp_client.del_group(self.settings['group_id'])

class Bulb:
	def __init__(self, settings):
		self.settings = settings

	def switch(self, bright, angle):
		self.udp_client.set_light([bright, angle])

	def switch_status(self):
		return True

	def show(self):
		print self.settings['sn'], self.settings['title']