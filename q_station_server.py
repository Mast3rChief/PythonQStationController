import socket
import sys
 
HOST = ''
PORT = 11600

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

while 1:
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    if not data: 
        break

    if data == '{"cmd":"light_list"}':
        reply = '{ "msync_switch": "1", "led": [ { "online": "1", "sn": "MD1AC44200001188", "title": "Light One", "iswitch": "0", "r": "0", "g": "11", "b": "106", "bright": "89", "effect": "9", "angle": "233.41176", "music_sync": "0" }, { "online": "1", "sn": "MD1AC44200001866", "title": "Light Two", "iswitch": "0", "r": "140", "g": "30", "b": "0", "bright": "66", "effect": "9", "angle": "0.0", "music_sync": "0" } ]}'
    else:
        reply = 'OK...' + data

    s.sendto(reply, addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()
