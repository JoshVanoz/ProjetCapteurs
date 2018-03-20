import re
import serial
import http.client
from ../Web/Apply/app import app, db
import datetime

PORT = ''

ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p[1]:
        PORT = p[0]
        break

SERVER = "localhost:5000"

ser = serial.Serial(port=PORT, baudrate=115200)

while True:
    a = ser.readline().decode('latin-1')
    reg_capt = re.search("([0-9]+) @ (.+)", a)
    reg_pos = re.search("([0-9]+) % (.+)", a)
    if reg_capt or reg_pos:
        if reg_capt:
            sender, msg = reg_capt.groups()
            sender = "0" + sender[-9:]
            capteur = get_capteur_phone(sender)
            if capteur != None:
                d = Donnee(value   = msg[2:],
                            date    = datetime.strptime(datetime.datetime.now(), '%b %d %Y %I:%M%p'),
                            capteur = capteur.get_id(),
                            parterre = capteur.get_parterre())
                capteur.add_data(d)
                db.session.commit()

        else:
            sender, msg = reg_pos.groups()
            sender = "0" + sender[-9:]
            capteur = get_capteur_phone(sender)
            if capteur != None:
                msg=msg[2:]
                msg.split(";")
                capteur.set_X(float(msg[0]))
                capteur.set_Y(float(msg[1]))
                db.session.commit()
        print(sender + " : " + msg)
