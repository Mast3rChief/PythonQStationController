from Tkinter import *
import socket			
import Tkinter as tk
import json

def set_light(*args):
	try:
		UDP_IP = ip.get()
		print UDP_IP
		UDP_PORT = 11600
		MESSAGE = '{"cmd":"light_ctrl","bright":"' + bright.get() + '","g":"'+ str(green.get()) +'","model":"6","b":"'+ str(blue.get()) +'","effect":"9","r":"'+ str(red.get()) +'","sn_list":[{"sn":"'+ active_bulb.get() +'"}],"matchValue":"0","iswitch":"1"}'
		temp = bright.get()
		print 'Brightness', temp
		print MESSAGE
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
		text.set(data)
		print "received message:", data
	except ValueError:
		pass

def ping(*args):
	try:
		UDP_IP = ip.get()
		UDP_PORT = 11600
		MESSAGE = '{"cmd":"light_list"}'

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
		json_data = json.loads(data)
		print json_data
		for i in range(num.get()):
			Radiobutton(mainframe,text=json_data['led'][i]['title'], variable=active_bulb,value=json_data['led'][i]['sn']).grid(column=4, row=i+1, sticky=W)
		text.set('Light changed!')
	except ValueError:
		pass
def close_windows(*args):
	root.destroy()
def callback(*args):
    print "variable changed!", text.get()

root = Tk()
root.title("Python Q Station Control")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

sn = StringVar()
name = StringVar()
bright = StringVar()
ip = StringVar()
text = StringVar()
num = IntVar()
active_bulb = StringVar()

ip.set('192.168.178.66')
bright.set('100')
num.set(6)

ip_entry = Entry(mainframe, textvariable=ip)
ip_entry.grid(column=2, row=1, sticky=(W, E))

b_entry = Entry(mainframe, width=7, textvariable=num)
b_entry.grid(column=2, row=2, sticky=(W, E))

b_entry = Entry(mainframe, width=7, textvariable=bright)
b_entry.grid(column=2, row=3, sticky=(W, E))

red = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
red.set(0)
red.grid(column=2, row=4, sticky=(N, W, E, S))
green = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
green.set(0)
green.grid(column=2, row=5, sticky=(N, W, E, S))
blue = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
blue.set(0)
blue.grid(column=2, row=6, sticky=(N, W, E, S))

Label(mainframe, textvariable=text).grid(column=3, row=6, sticky=(W, E))

Button(mainframe, text="Set Light Brightness", command=set_light).grid(column=3, row=3, sticky=W)
Button(mainframe, text="Ping Q Station", command=ping).grid(column=3, row=2, sticky=W)
Button(root, text="Quit", command=close_windows).grid(column=0, row=5, sticky=W)


Label(mainframe, text="Q Station IP").grid(column=1, row=1, sticky=W)
Label(mainframe, text="(default: 192.168.178.66)").grid(column=3, row=1, sticky=W)
Label(mainframe, text="Brightness").grid(column=1, row=3, sticky=W)
Label(mainframe, text="Number of Bulbs").grid(column=1, row=2, sticky=W)
Label(mainframe, text="Green").grid(column=1, row=4, sticky=W)
Label(mainframe, text="Red").grid(column=1, row=4, sticky=W)
Label(mainframe, text="Blue").grid(column=1, row=4, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=5)

ip_entry.focus()
b_entry.focus()

root.mainloop()