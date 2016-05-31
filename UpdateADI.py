# Update ADI file from contest log with fields for contact log.

import argparse
import re
import os
import time

# Convert Band to Freq.
def band_to_freq(band):
	freqTable = {
		"160M": "1.800",
		"80M":  "3.500",
		"40M":  "7.000",
		"20M": "14.000",
		"15M": "21.000",
		"10M": "28.000",
	}
	return freqTable.get(band)

# Input command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("adi_file", type=str, help="name of the ADI file, such as MOQP.adi or MOQP")
parser.add_argument("-f", "--freq_from_band", action="store_true", help="set Freq from Band")
parser.add_argument("--other2", type=str, help="data for Other2 field")
parser.add_argument("--my_qth", type=str, help="data for MY_QTH field")
parser.add_argument("--tx_pwr", type=str, help="data for TX_PWR field")
args = parser.parse_args()
	
# Validate and format file name: XYZ.adi or XYZ
dotAdi = re.compile(".*\.adi$")
anyDot = re.compile(".*\..*")
if dotAdi.match(args.adi_file): # XYZ.adi
	rootName = args.adi_file[:-4]
	origName = args.adi_file
elif not anyDot.match(args.adi_file): # XYZ
	rootName = args.adi_file
	origName = args.adi_file + ".adi"
else:
	print "Invalid ADI filename: " + args.adi_file
	print "Format: XYZ.adi or XYZ with no dot."
	exit(1)

# Get date/time of original ADI file.
fileTime = os.path.getmtime(origName) # float
fileTimeLocal = time.localtime(fileTime) # struct
timeTag = time.strftime("_%Y%m%d_%H%M%S", fileTimeLocal) # string
backName = rootName + timeTag + ".adi"
workName = rootName + "_UPDATE.adi"

# Note: CR automatic on Windows with Python LF
if args.other2: # Prepare Other2 line.
	other2_line = "<Other2:" + str(len(args.other2)) + ">" + args.other2 + "\n"
if args.my_qth: # Prepare MY_QTH line.
	my_qth_line = "<MY_QTH:" + str(len(args.my_qth)) + ">" + args.my_qth + "\n"
if args.tx_pwr: # Prepare TX_PWR line.
	tx_pwr_line = "<TX_PWR:" + str(len(args.tx_pwr)) + ">" + args.tx_pwr + "\n"

# Open original and work ADI files.
origFile = open(origName, "r")
workFile = open(workName, "w")

# Loop through each line in the ADI file.
for line in origFile:
	# Convert Band to Freq
	if line[1:5] == "Band" and args.freq_from_band: # <Band:3>20M
		band_len = int(line[6])
		band_start = 8
		band_end = 8 + band_len # one past end
		band_str = line[band_start:band_end]
		freq_str = band_to_freq(band_str)
		freq_line = "<Freq:" + str(len(freq_str)) + ">" + freq_str + "\n" # <Freq:6>14.000

	# Write new lines before end of record.
	if (line[1:4] == "eor"):
		if args.other2:
			workFile.write(other2_line)
		if args.my_qth:
			workFile.write(my_qth_line)
		if args.tx_pwr:
			workFile.write(tx_pwr_line)
		if args.freq_from_band:
			workFile.write(freq_line)

	# Write the original line.
	workFile.write(line)

# Close and rename files.
origFile.close()
workFile.close()
os.rename(origName, backName)
os.rename(workName, origName)
