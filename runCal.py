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
	digiDicIP = {'ANMX' : '136.177.121.45',
		'AFMO' : '136.177.121.186',
		'C01A' : '217.15.7.140',
		'ENG1' : '136.177.121.31',
		'ENG2' : '136.177.121.32',
		'ENG3' : '136.177.121.33',
		'ENG4' : '136.177.121.34',
		'ENG5' : '136.177.121.35',
		'ENG6' : '136.177.121.51',
		'ENG7' : '136.177.121.52',
		'FBA1' : '136.177.121.162',
		'FBA2' : '136.177.121.187',
		'INF1' : '136.177.121.151',
		'INF2' : '136.177.121.12',
		'TST1' : '136.177.121.180',
		'TST2' : '136.177.121.182',
		'TST3' : '136.177.121.184',
		'TST4' : '136.177.121.181',
		'TST5' : '136.177.121.183',
		'TST6' : '136.177.121.185'}
		#These belong to a different base port
		#'GTO'  : '136.177.121.149',
		#'MSTG' : '136.177.121.47',
		#'CHGR' : '136.177.121.48',
		#'CBRA' : '136.177.121.49'}

	digiDicSerial = {'ANMX' : '010000124ECE4256',
		'AFMO' : '0100000DB142F699',
		'C01A' : '010000069A79D5A7',
		'ENG1' : '01000013D573E277',
		'ENG2' : '010000140E6467B4',
		'ENG3' : '010000140E58B309',
		'ENG4' : '0100001418BC4FF2',
		'ENG5' : '0100001418C92541',
		'ENG6' : '010000140E647581',
		'ENG7' : '010000140E5A4937',
		'FBA1' : '010000124ED088D8',
		'FBA2' : '010000123EBEE78C',
		'INF1' : '01000006406C2456',
		'INF2' : '01000008E91425FC',
		'TST1' : '100000B650221EF',
		'TST2' : '0100000B69AB6211',
		'TST3' : '0100000DAFA06C93',
		'TST4' : '01000014D96F80EF',
		'TST5' : '01000014AC047B2D',
		'TST6' : '01000014EB1BBD75'}
		#These belong to a different base port
		#'GTO'  : '033500C7D2697832',
		#'MSTG' : '0335009A9219C8D3',
		#'CHGR' : '03350025D121A821',
		#'CBRA' : '03350064157808B6'}
 	
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

	#why do some have 3, 6, 7 values?
	calval = {'CMG3-T': ['-42','-36','-24','-6','-42','-36'],
		'CMG3-TB': ['-42','-36','-24','-6','-42','-36'],
		'CMG3-TB-COLD': ['-42','-36','-24','-6','-42','-42'],
		'GS12': ['-6','-6','-6','-6','-6','-6'],
		'KS36000': ['-6','-6','-6','-6','-6','-6','-6'],
		'KS54000': ['-12','-6','-6','-6','-12','-6','-6'],
		'STS-1': ['-30','-18','-6','-6','-30','-24','-24'],
		'STS-1-E300': ['-30','-18','-6','-6','-30','-24','-24'],
		'STS-1-Z': ['-30','-18','-6','-6','-30','-24','-24'],
		'STS-1-Z-E300': ['-30','-18','-6','-6','-30','-24','-24'],
		'STS-2.5': ['-36','-36','-18','-6','-42','-30'],
		'STS-2-HG': ['-36','-36','-24','-6','-42','-36'],
		'STS-2-SG': ['-36','-36','-24','-6','-42','-30'],
		'TR-240': ['-42','-30','-18','-6','-42','-36']}

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




