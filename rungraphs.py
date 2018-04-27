import sys

import oi as Oi #imported python file for oi read 
import oic as Oic #imported python file for oic read



# svg or png
SaveFileType = sys.argv[1] 

#s=Streight, i=Interpolate
LineType = sys.argv[2] 

#p=portrait, l=Landscape
FileFormat = sys.argv[3] 

try:
	#t=table
	TableShow = sys.argv[4]
except Exception as e:
	TableShow = 0

# function to call generate oi.py file	
Oi.operatingIndex(SaveFileType,LineType,FileFormat,TableShow) 

# function to call oic.py file
Oic.salesGrowth(SaveFileType,LineType,FileFormat,TableShow) 
