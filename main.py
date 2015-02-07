from Tkinter import *
from udp_client import *


def callback_bright():
    udp_client = UdpClient(ip.get(), 11600)
    udp_client.set_light(bright.get(), red.get(), green.get(), blue.get(), bulb.get())


def callback_ping():
    udp_client = UdpClient(ip.get(), 11600)
    response = udp_client.get_lights()

    for i in range(len(response['led'])):
        if i == 0:
            seperator = ''
        else:
            seperator = ', '

        bulb.set(bulb.get() + seperator + response['led'][i]['sn'])

root = Tk()
root.title("Python Q Station Control")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ip = StringVar()
bulb = StringVar()

ip.set('188.166.7.41')

ip_entry = Entry(mainframe, textvariable=ip)
ip_entry.grid(column=2, row=1, sticky=(W, E))

bulb_entry = Entry(mainframe, textvariable=bulb)
bulb_entry.grid(column=2, row=2, sticky=(W, E))

bright = Scale(mainframe, from_=0, to=100, orient=HORIZONTAL)
bright.set(0)
bright.grid(column=2, row=3, sticky=(N, W, E, S))

red = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
red.set(0)
red.grid(column=2, row=4, sticky=(N, W, E, S))

green = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
green.set(0)
green.grid(column=2, row=5, sticky=(N, W, E, S))

blue = Scale(mainframe, from_=0, to=255, orient=HORIZONTAL)
blue.set(0)
blue.grid(column=2, row=6, sticky=(N, W, E, S))

Button(mainframe, text="Set Brightness", command=callback_bright).grid(column=2, row=7, sticky=W)
Button(mainframe, text="Get Bulbs", command=callback_ping).grid(column=1, row=7, sticky=W)

Label(mainframe, text="Q Station IP").grid(column=1, row=1, sticky=W)
Label(mainframe, text="Bulb").grid(column=1, row=2, sticky=W)
Label(mainframe, text="Brightness").grid(column=1, row=3, sticky=W)
Label(mainframe, text="Green").grid(column=1, row=4, sticky=W)
Label(mainframe, text="Red").grid(column=1, row=5, sticky=W)
Label(mainframe, text="Blue").grid(column=1, row=6, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=5)

ip_entry.focus()

root.mainloop()