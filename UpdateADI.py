

import sys
import os

def band_to_freq(b):
	switcher = {
		"80M": "3.500",
		"40M": "7.000",
		"20M": "14.000",
		"15M": "21.000",
	}
	return switcher.get(b)

argc = len(sys.argv)
args = sys.argv

if (argc == 2):
	adiName = args[1]
	adiRoot = (adiName.split("."))[0]
	adiNewName = adiRoot + "_NEW.adi"
	adiFile = open(adiName, "r")
	adiNew = open(adiNewName, "w")
	
	for line in adiFile:
		if (line[0:6] == "<Band:"): # <Band:3>20M
			bandLen = int(line[6])
			bandStart = 8
			bandEnd = 8 + bandLen # one past end
			bandString = line[bandStart:bandEnd]
			freqString = band_to_freq(bandString)

		if (line[0:5] == "<eor>"): # line includes CRLF
			adiNew.write("<Other2:8>Waterman\n") # CR automatic on Windows
			adiNew.write("<MY_QTH:8>Waterman\n")
			adiNew.write("<TX_PWR:1>5\n")
			adiNew.write("<Freq:" + str(len(freqString)) + ">" + freqString + "\n") # <Freq:6>14.000

		# write the original line
		adiNew.write(line)
	
	adiFile.close()
	adiNew.close()
	
	# rename files
	os.rename(adiName, adiRoot + "_OLD.adi")
	os.rename(adiNewName, adiName)
	

