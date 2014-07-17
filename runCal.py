#!/usr/bin/env python

import argparse
import os
import sys

def getargs():
	parser = argparse.ArgumentParser(description="Program to run autocals")

	parser.add_argument('-action', type = str, action = "store", dest="action", \
		required = True, help = "Options are start or stop")

	parser.add_argument('-d', '--digitizer', type = str, action = "store", \
		dest = "digitizer", required = True, help = "Name of digitizer" + \
		" Example: TST1")

	parser.add_argument('-st', '--sensortype', type = str, action = "store", \
		dest = "sensor", required = True, help = "Sensor type possible " + \
		"sensors include: STS-1")

	parser.add_argument('-ch', '--channels', type = str, action = "store", \
		dest = "channel", required = True, help="A or B")

	parser.add_argument('-v', '--verbose', action = "store_true", dest = "debug", \
		default = False, help = "Run in debug mode") 

	parserval = parser.parse_args()
	return parserval

def writeqreg(digitizer):
	#This function writes the qregister file based on the digitizer
	digiDicIP = {'ENG1' : '136.177.121.31',
		'ENG3' : '136.177.121.33'}

	digiDicSerial = {'ENG1' : '01000013D573E277',
		'ENG3' : '010000140E58B309'}
 	
	f = open("qregister.config",'w')
	f.write("Q330.1.IP = " + digiDicIP[digitizer] + "\n")
	f.write("Q330.1.Serial = " + digiDicSerial[digitizer] + "\n")
	f.write("Q330.1.BasePort = 5330\n")
	f.write("Q330.1.AuthCode = 0\n")

	f.close()

	return

def writeautocal(sensor,channel):
	f = open("autocal.config",'w')
	if channel == "A":
		channel = "1-3"
		calmon = "4"
	else:
		channel = "4-6"
		calmon = "1"
	calval = {'TR-240': ['-42','-30','-18','-6','-42','-36','-36']}
	f.write("# Autocal Sequence for " + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][0].ljust(3) + \
		" 5m    40m   5m    0  sine   0.004        SENSOR:" + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][1].ljust(3) + \
		" 5m    40m   5m    0  sine   0.02         SENSOR:" + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][2].ljust(3) + \
		" 5m    40m   5m    0  sine   0.1          SENSOR:" + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][3].ljust(3) + \
		" 5m    40m   5m    0  sine   1.0          SENSOR:" + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][4].ljust(3) + \
		" 15m   15m   15m   0  step   positive     SENSOR:" + sensor + "\n")
	f.write("1 " + channel + " " + calmon +  " " + calval[sensor][5].ljust(3) + \
		" 10m   4h    10m   0  random 1.25    none SENSOR:" + sensor + "\n")

	f.close()

	return



parserval = getargs()

if parserval.debug:
	debug = True
else:
	debug = False

if debug:
	print "Sensor: " + parserval.sensor
	print "Digitizer: " + parserval.digitizer
	print "Channel: " + parserval.channel
	print "Action: " + parserval.action

if not parserval.channel in set(["A", "B"]):
	print 'Channel must be A or B'
	sys.exit()

if debug:
	print "Writing qregister file"
writeqreg(parserval.digitizer)

if debug:
	print "Writing autocal file"
writeautocal(parserval.sensor,parserval.channel)

if not parserval.action in set(["start","stop"]):
	print 'Action must be start or stop'
	sys.exit()

if debug:
	print 'Starting autocal sequence'
os.system('/opt/util/bin/autocal -d 1 ' + parserval.action)




os.remove("qregister.config")
os.remove("autocal.config")




