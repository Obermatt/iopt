import sys

showSyntax = False
try:
	# svg or png
	SaveFileType = sys.argv[1] 

	#s=Streight, i=Interpolate
	LineType = sys.argv[2] 

	#p=portrait, l=Landscape
	FileFormat = sys.argv[3] 
except Exception as e:
	showSyntax=True

try:
	#t=table
	TableShow = sys.argv[4] 
except Exception as e:
	TableShow = 0

#validating param values

if showSyntax==False:
	if SaveFileType!="png" and SaveFileType!="svg":
		showSyntax=True

	if LineType!="s" and LineType!="i":
		showSyntax=True

	if FileFormat!="p" and FileFormat!="l":
		showSyntax=True

	if TableShow!="t" and TableShow!=0:
		showSyntax=True

if showSyntax==True:
	print("Invalid param values")
	print("Correct syntax is as follows:")
	print("\t For all graphs: rungraphs.py")
	print("\t For Ok graph: ok.py")
	print("\t For oi graph: oi.py")
	print("\t For oic graph: oic.py")
	print("\t Parameters: <outputformat> <linetype> <displaymode> <showtable>")
	print("\t\t output formats -- svg / png")
	print("\t\t linetype -- s (for straightline) / i (for interpolated lines) ")
	print("\t\t display mode -- l (landscape) | p (portraight)")
	print("\t\t show table -- t ")
	exit()

