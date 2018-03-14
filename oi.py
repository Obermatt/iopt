# Creating Operating Index Chart

#importing required files and libraries
import os
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np  
import sys
import datetime
import CsvRead as CsvData #imported python file for CSV read 
import matplotlib.patches as mpatches
from matplotlib.legend_handler import (HandlerLineCollection,
                                       HandlerTuple)
import matplotlib.collections as mcol
from matplotlib.lines import Line2D

# importing font manager
import matplotlib.font_manager as font_manager 

#This is to ignore warnings
import warnings
warnings.filterwarnings("ignore")

#Change format option to svg or png
PRINT_FORMAT = "svg"   


try:
	#validate parmas when run script from command line

	import ParamValidator as prmValid 
	ReadData = CsvData.readData() # read CSV data

	##Start of font setting
	matplotlib.font_manager._rebuild()
	fontpath = 'EBGaramond12-Regular.ttf'
	prop = font_manager.FontProperties(fname=fontpath)
	titlefont = {'fontname':prop.get_name()}
	legendfont = prop.get_name()
	plt.rcParams['font.family'] = 'Arial'
	##End of font setting

	now = datetime.datetime.now()
	curTime = now.strftime("%Y%m%d")

	#Reading filename from arguments
	saveFileNameParam = sys.argv[1] 
	saveFileNameParam=saveFileNameParam.replace("."+PRINT_FORMAT, "") 

	#Reading printing mode (landscape[l] or portrait[p])
	saveFileSizeParam = sys.argv[2] 

	#Reading input data filename
	saveinputFile = sys.argv[3] 
	saveinputFile=saveinputFile.replace(".csv", "")

	
	#savefilepath
	savePath = "export_img/" 
	saveFile = "_"+saveFileNameParam+"_"+saveinputFile+"_"+saveFileSizeParam+"."+PRINT_FORMAT
	
	#reading chart title (#titleName = 'Operating Index \nEBIT Margin' # Static Title Entry)
	titleName = ReadData['title'][0]
	titleName = titleName.replace('\\n', '\n') 

	#defining color and styles for various lines in chart
	#TOP COLOR: #afdce3  
	#ORANGE COLOR:#ff7800
	#middle Line Color:#2e91ad
	#Bottom COLOR: #91ccd1

	color = ['#afdce3','#2e91ad','#91ccd1','#ff7800','#2e91ad'] # COLOR_CODE of line
	style = ['-','-','-','-',''] # line type
	marker = ['','','','o',''] # Marker type

	#legend names reading from csv data file
	legendLabel = ReadData['legendName'] 

	#company name (reading from CSV data file)
	compname =legendLabel[3] 

	# Check if CSV file value is in percentage or not
	percentageExist = ReadData["perExist"]
	percentageFormat = '{:3.1f}'
	if percentageExist: percentageFormat = '{:3.1f}%'
	#Marker width size
	markerSize = 5 

	#Line width value
	lineWidthArr = [1,2,1,2,1] 

	#Orange and blue Line width
	lineWidth = 1.5  # Line width value
	
	dottedKey = 3 # company name row id
	markerColor = '#ff6100' #marker color
	
	#title font size
	titleSize = 14

	#number font size
	numberFontSize = 10.5 	

	plt.figure(1)
	ax = plt.subplot(111)
	
	# Plot size margin from Bottom
	plt.subplots_adjust(bottom=0.2) 

	#hide right and left line of chart
	ax.spines['right'].set_visible(False) 
	ax.spines['left'].set_visible(False) 

	# X Axis Data points
	x = np.array(list(range(len(ReadData['xAxisName']))))
	
	# Y Axis Data points
	yAxisValue = ReadData['axisValue'] 
	yAxisValue = [list(map(float, i)) for i in yAxisValue]
	y = np.array(yAxisValue)

	#x Axis Data points
	my_xticks = ReadData['xAxisName'] 

	#set X axis replace static number with original key value
	plt.xticks(x, my_xticks,fontsize=numberFontSize)  

	# interpolation technique is used to convert the straight line with curve
	from scipy import interpolate 
	
	# Loop start count
	count = 0 
	fillData = {}
	for data in y:
		
		if count == 3: 
			# Draw staright Line
			f = interpolate.interp1d(np.arange(len(data)), data, kind='linear') 
		
	
		else:   
			# Draw Curve Line
			f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic') #
                
		xnew = np.arange(0, len(data)-1, 0.01)
		ynew = f(xnew)

		fillData[count] = f(xnew)	
		#Set plot final plot	
		plt.plot(xnew, ynew, color=color[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidthArr[count],label=legendLabel[count])  
		count = count + 1

	# Fill color between two line start
	#from y0 to y1	
	fill1 = [0,1] 
	#from y1 to y2
	fill2 = [1,2] 
	# COLOR_CODE
	colorFill = ['#91ccd1','#afdce3'] 
	count1 = 0
	for a,b in zip(fill1,fill2):
		plt.fill_between(xnew, fillData[a],fillData[b], color=colorFill[count1], alpha='1',interpolate=True) 
		count1 = count1 +1
	

	# first add orange marker without line		
	plt.plot(y[dottedKey],color=markerColor,linestyle='',markersize=markerSize,linewidth=lineWidth,marker='o'); 
	
	# added to display value on marker	
	for i,j in zip(x,y[dottedKey]):	
		#converted values into percentage value
		ax.annotate(percentageFormat.format(j),xy=(i,j),horizontalalignment='right',verticalalignment='bottom',fontsize=numberFontSize)	

	vals = ax.get_yticks()
	#converted values into percentage value
	ax.set_yticklabels([percentageFormat.format(x) for x in vals],fontsize=numberFontSize) 
	# Set title
	csfont = {'fontname':'EB Garamond'}	
	plt.title(titleName,loc='left',fontsize=titleSize,fontweight="bold",**titlefont)

	fig = plt.gcf()

	# defining portrait or landscape mode
	if saveFileSizeParam == 'p': 
		fig.set_size_inches(8.3, 4.3)
		dpi = 150
	else:  
		#either landscape or if not defined
		fig.set_size_inches(9.84, 5.9)	
		dpi = 200


	# Start of designing custome legends

	m2, = ax.plot([], [],color='#ffffff' , 
              fillstyle='bottom', linestyle='none',linewidth=2)
	m3, = ax.plot([], [], color='#ffffff', marker='',markersize=2,  fillstyle='bottom',
               linestyle='none',linewidth=1)
	m4, = ax.plot([], [], color='#ff7800' , marker='o',
               linestyle='none',solid_joinstyle='round',linewidth=1)
	
	legendtext1 = ReadData['axisfigtext'][0]
	legendtext2 = ReadData['axisfigtext'][1]
	
	plt.figtext(0.12, 0.08, '----------------------------------------------------',
		    backgroundcolor='#afdce3', color='#afdce3', weight='ultralight',
		    size='3')
	plt.figtext(0.12, 0.068, '---------------------------------------------------- -------------------------- ------------------------  ------------------------- ------------------------- ',
		    backgroundcolor='#2e91ad', color='#2e91ad', weight='ultralight',
		    size='1')
	plt.figtext(0.12, 0.06, '----------------------------------------------------',
		    backgroundcolor='#91ccd1',
		    color='#91ccd1', weight='ultralight', size='3')
	plt.figtext(0.23, 0.06, legendtext1,
		    backgroundcolor='#ffffff',
		    color='black', weight='normal', size='11',family=legendfont)
	plt.figtext(0.12, 0.02, '-------------------------------O--------------------- -------------------------- ------------------------  ------------------------- ------------------------- ',
		    backgroundcolor='#ff7800', color='#ff7800', weight='normal',
		    size='1')
	
	plt.legend(((m2,m3),m4), ('', legendtext2), numpoints=1, labelspacing=2,
          loc='center', fontsize=11.0,bbox_to_anchor=(0.14, -0.199),handlelength=6,frameon=False,prop={'family':legendfont})

	# End of designing custome legends 
	
	## bbox_inches='tight'  for removing margin and paddding of graph 
	plt.savefig(savePath+curTime+saveFile, dpi=dpi, bbox_inches='tight', format=PRINT_FORMAT) 
	
	#plt.show()	
	print("Chart succesfully completed. \n You can find generated file at following location:\n " +savePath+curTime+saveFile)	

except Exception as e:	

	print("Something Went wrong! Unable to process your request.")
	print(e)

## End of program
