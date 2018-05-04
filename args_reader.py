import sys

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

