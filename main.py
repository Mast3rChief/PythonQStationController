from Tkinter import *
from tkMessageBox import *
from udp_client import *
import ttk as ttk


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Python Q Station Control")
        
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        self.ip = StringVar()
        
        self.bulb_treeview = ttk.Treeview(self.mainframe)
        self.bulb_treeview.grid(column=0, row=1, rowspan=5, sticky=(W, E))
        self.bulb_treeview.bind('<<TreeviewSelect>>', self.callback_bulb_treeview)
        
        self.ip_entry = Entry(self.mainframe, textvariable=self.ip)
        self.ip_entry.grid(column=2, row=1, sticky=(W, E))
        
        self.bright_scale = Scale(self.mainframe, from_=0, to=100, orient=HORIZONTAL)
        self.bright_scale.set(0)
        self.bright_scale.grid(column=2, row=2, sticky=(N, W, E, S))

        self.red_scale = Scale(self.mainframe, from_=0, to=255, orient=HORIZONTAL)
        self.red_scale.set(0)
        self.red_scale.grid(column=2, row=3, sticky=(N, W, E, S))

        self.green_scale = Scale(self.mainframe, from_=0, to=255, orient=HORIZONTAL)
        self.green_scale.set(0)
        self.green_scale.grid(column=2, row=4, sticky=(N, W, E, S))

        self.blue_scale = Scale(self.mainframe, from_=0, to=255, orient=HORIZONTAL)
        self.blue_scale.set(0)
        self.blue_scale.grid(column=2, row=5, sticky=(N, W, E, S))

        Button(self.mainframe, text='Set Values', command=self.callback_set_values).grid(column=2, row=6, sticky=(W,E))
        Button(self.mainframe, text='Get bulbs from Q Station', command=self.callback_get_bulbs).grid(column=0, row=6, sticky=(W,E))

        Label(self.mainframe, text='Q Station IP').grid(column=1, row=1, sticky=W)
        Label(self.mainframe, text='Brightness').grid(column=1, row=2, sticky=W)
        Label(self.mainframe, text='Red').grid(column=1, row=3, sticky=W)
        Label(self.mainframe, text='Green').grid(column=1, row=4, sticky=W)
        Label(self.mainframe, text='Blue').grid(column=1, row=5, sticky=W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=5)

        self.ip_entry.focus()

        self.root.mainloop()

    def callback_set_values(self):
        if self.bulb_treeview.selection() != '' and self.bulb_treeview.selection()[0] != 'bulbs':
            udp_client = UdpClient(self.ip.get(), 11600)
            udp_client.set_light(self.bright_scale.get(), self.red_scale.get(), self.green_scale.get(), self.blue_scale.get(), self.bulb_treeview.item(self.bulb_treeview.selection()[0], 'tag')[0])
        else:
            showinfo('Info', 'Please select the bulb you want to control.')
    
    def callback_get_bulbs(self):
        if self.ip.get() != '':
            udp_client = UdpClient(self.ip.get(), 11600)
            response = udp_client.get_lights()

            map(self.bulb_treeview.delete, self.bulb_treeview.get_children())
            self.bulb_treeview.insert('', 'end', 'bulbs', text='Q Station', open=True)

            for i in range(len(response['led'])):
                self.bulb_treeview.insert('bulbs', 'end', text=response['led'][i]['title'], tag=response['led'][i]['sn'])
        else:
            showerror('Error', 'Please fill in the Q Station IP first.')

    def callback_bulb_treeview(self, event):
        item = self.bulb_treeview.selection()[0]
    
        if item != 'bulbs':
            print(self.bulb_treeview.item(item, 'tag')[0])

if __name__ == '__main__':
    app = App()