#!/usr/bin/env python
import serial
import time
import sqlite3
import datetime
import subprocess as sp

tmp = sp.call('clear',shell=True) #start with clear term
conn = sqlite3.connect("dylos.db")
cursor = conn.cursor()

#creat a table
cursor.execute('create table if not exists dylos (id INTEGER PRIMARY KEY AUTOINCREMENT, daystamp test, timestamp text, smallp text, bigp text)')

#enter your device file
arddev = '/dev/ttyUSB0'
baud = 9600

#setup - if a Serial object cant be created, a serialexception will be raised.
while True:
    try:
        ser = serial.Serial(arddev, baud)
        #break out of while loop when connection is made
        break
    except serial.SerialException:
        print 'waiting for device ' + arddev + ' to be available'
        time.sleep(3)

#read lines from serial device for ever
val = 0
while val == 0 :

    element = ser.readline().strip('\n')
    pieces = element.split(",") # split the data by the tab
    unix = time.time() #time
    datedaynow = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d')) #date
    datetimenow = str(datetime.datetime.fromtimestamp(unix).strftime('%H:%M:%S')) #time
    print "day: %s" % datedaynow
    print "time: %s" % datetimenow
    print "small parts : %s" % pieces[0]
    print "big parts   : %s" % pieces[1]
    print ""
	#insert data into database
    cursor.execute("insert into dylos (daystamp, timestamp, smallp, bigp) values (?, ?, ?, ?)", (datedaynow, datetimenow, pieces[0], pieces[1]))
    conn.commit()

cursor.close()
conn.close()