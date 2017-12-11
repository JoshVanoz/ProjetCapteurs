
import re
import serial
import http.client

PORT = '/dev/ttyACM0'

SERVER = "localhost:5000"

connection = http.client.HTTPConnection(SERVER)

ser = serial.Serial(port=PORT, baudrate=115200)

while True:
    a = ser.readline().decode('latin-1')
    reg_capt = re.search("Message de ([0-9]+) : Capteur : (.+)", a)
    reg_pos = re.search("Message de ([0-9]+) : Position : (.+)", a)
    if reg_capt or reg_pos:
        reg = reg_capt or reg_pos
        r_type = "measure" if reg_capt else "position"
        sender, msg = reg.groups()
        sender = "0" + sender[-9:]
        print(sender + " : " + msg)
        connection.request('GET', '/%s/%s/%s' % (r_type, sender, msg,))
        print(connection.getresponse().read().decode())
