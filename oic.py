import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import CsvRead as CsvData #imported python file for CSV read 
import matplotlib.font_manager as font_manager 

import warnings
warnings.filterwarnings("ignore")

#Change format option to svg or png
PRINT_FORMAT = "png"

#defining colorcodes
lightskyblue_obermatt = '#ACE3E8'
darkskyblue_obermatt = '#91CCD1'
blue_obermatt = '#2A90AC'
orange_obermatt = '#ff7802'
brown_obermatt="#472101"

#below function is used to convert nan value to default interpolate value between of two numbers
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


def salesGrowth(SaveFileType,LineType,FileFormat,TableShow = None):
	try:
		from path_config import img_file_path
		
		dataRead = CsvData.readData() # read CSV data multiple file		
		incr=1
		for ReadData in dataRead:				
			##Start of font setting
			matplotlib.font_manager._rebuild()
			fontpath = 'AGaramondPro-Regular.otf'
			prop = font_manager.FontProperties(fname=fontpath)
			titlefont = {'fontname':prop.get_name()}
			legendfont = prop.get_name()
			plt.rcParams['font.family'] = 'Arial'
			##End of font setting

			now = datetime.datetime.now()
			curTime = now.strftime("%Y_%m_%d")
			
			#Reading filename from arguments
			PRINT_FORMAT = SaveFileType
			
			#Reading printing mode (landscape[l] or portrait[p])
			saveFileSizeParam = FileFormat 
				
			saveFileNameParam = ReadData['fileName'] #Read first param
			
			#title font size
			titleSize = 16
			
			markerSize = 5 # Marker width size
			lineWidth = 2 # Line width valuesaveFileNameParam
			count = 0 # Loop start count
			dottedKey = 0 # define where we need a dotted key on which line
			titleName = 'Sales Growth'
			replaceCountWord = 'Count'
			
			#save path from export_path.py

			saveinputFile = ReadData['fileName']
			saveFile = "_oic_"+saveinputFile+"_"+LineType+"_"+saveFileSizeParam
					
			#color code of line
			color = [orange_obermatt,blue_obermatt,blue_obermatt,blue_obermatt,blue_obermatt] 
			style = ['-','--','-','--',''] # line type
			marker = ['o','','','',''] # Marker type legendLabel = ReadData['legendName'] # legend name
			legendLabel = ReadData['legendName'] # legend name
			legendLabel1 = ReadData['legendName'] # legend name

			# replace Count word with _nolegend_. not required to display Count in legend	
			legendLabel1 = [w.replace(replaceCountWord, '_nolegend_') for w in legendLabel1] 
			numberFontSize = 10.5			

			# Check if CSV file value is in percentage or not
			percentageExist = ReadData["perExist"]
			percentageFormat = '{:3.1f}'
			if percentageExist: percentageFormat = '{:3.1f}%'

			# -- Start Plot  --		
			plt.figure()			
			ax = plt.subplot()
			ax.spines['right'].set_visible(False) #hide right line of chart
			ax.spines['top'].set_visible(False) #hide top line of chart
			#ax.spines['bottom'].set_position(('axes',-0.02))
			#ax.spines['top'].set_position(('axes',1.02))

			x = np.array(list(range(len(ReadData['xAxisName'])))) # X values total count

			yAxisValue = ReadData['axisValue'] # Y values data from CSV		
			# added below to set Y axis value static & dynamic Start
			yMin = ReadData['yMin']
			yMax = ReadData['yMax']	
			y = np.array(yAxisValue)
			plt.ylim(int(yMin),int(yMax))			
			
			my_xticks = ReadData['xAxisName'] # X values data from CSV

			for i,j in zip(x,y[dottedKey]):	# added to display value on marker		
				ax.annotate(percentageFormat.format(j),xy=(i,j),horizontalalignment='right',verticalalignment='bottom',fontsize=numberFontSize)	#converted values into percentage value	
					
			from scipy import interpolate # interpolate is used to convert the streight line with curve
			legend_elements = []		
			for data in y:
				if LineType == "s":
					f = interpolate.interp1d(np.arange(len(data)), data, kind='linear')
					xnew = np.arange(0, len(data)-1, 0.01)
					ynew = f(xnew)	
					# to set a curve line iprint(nstead of streight line End
					plt.plot(xnew, ynew, color=color[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,label=legendLabel[count]) #Set plot final plot
					legend_elements.append(Line2D([0], [0],color=color[count],label=legendLabel1[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,marker=marker[count])) #to set the legend							
				else:
					#interpolate value if found Nan value in array
					data = np.array(data)
					nans, xdata= nan_helper(data)
					data[nans]= np.interp(xdata(nans), xdata(~nans), data[~nans])
					# to set a curve line instead of streight line Start
					f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic') # Interpolate Line
					xnew = np.arange(0, len(data)-1, 0.01)
					ynew = f(xnew)	
					# to set a curve line iprint(nstead of streight line End
					plt.plot(xnew, ynew, color=color[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,label=legendLabel[count]) #Set plot final plot
					legend_elements.append(Line2D([0], [0],color=color[count],label=legendLabel1[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,marker=marker[count])) #to set the legend						
				count = count+1 # Auto increament of loop
			# Add orange marker on line
			plt.plot(y[dottedKey],color='#ff6100',linestyle='',markersize=markerSize,linewidth=lineWidth,marker='o'); 
			
			# to set the legend
			plt.legend(handles=legend_elements,bbox_to_anchor=(1, 0.8),prop={'size': numberFontSize,'weight':'normal','family':legendfont},labelspacing=2,frameon=False)
			vals = ax.get_yticks()

			# Converted values into percentage value
			ax.set_yticklabels([percentageFormat.format(x) for x in vals],fontsize=numberFontSize) 
			
			# Display table or not based on parameter passed by user, by default table will display on graph, 0 -> dont display table, 1 -> Display table
			try:
				TableShow # Parameter which is entered by user
			except Exception as e:
				showTable = True # default display Table				
			else:
				showTable = False
				if TableShow == 't': # if user enter 1 display table else dont display the table
					showTable = True					
					saveFile += "_t"
								
			saveFile += "."+PRINT_FORMAT
			plt.xticks(x, my_xticks,fontsize=numberFontSize)
			
			if showTable: # True display Table
				# First Table start
				the_table = plt.table(cellText=y,colLabels=my_xticks,loc='bottom',colLoc='right',rowLoc='left')					
				the_table.set_fontsize(numberFontSize)
				the_table.scale(1,1.5)
				
				#Remove Border of table 1 cell
				for key, cell in the_table.get_celld().items():		
					cell.set_linewidth(0)
				# First Table end
				
				# right side table of company name start		
				my_xticks_1 = [titleName]
				legendLabel_1 = np.reshape(legendLabel, (-1, 1))	
				
				the_table1 = plt.table(cellText=legendLabel_1,colLabels=my_xticks_1,loc='bottom right',colLoc='bottom left',rowLoc='bottom left',animated=True)
				#the_table1.auto_set_column_width([-1,0,1]) # set column width	
				the_table1.set_fontsize(numberFontSize)
				the_table1.scale(.5,1.5)
				cells = the_table1.properties()["celld"]
				
				# row text left align
				cellLength = len(legendLabel) #lengtshowTableh of row
				for i in range(0,cellLength+1):
					cells[i, 0]._loc = 'left'		
				
				
				#Remove Border of table 2 cell
				for key, cell in the_table1.get_celld().items():
					cell.set_linewidth(0)
					
				# right side table of company name end
				
				plt.xticks([]) # remove x Axis values, already put value using table
										
			plt.title(titleName,loc='left',fontsize=titleSize,fontweight="regular",color=brown_obermatt,**titlefont)# Set title 
			
			fig = plt.gcf()
			# defining portrait or landscape mode
			if saveFileSizeParam == 'p': 
				fig.set_size_inches(10.3, 7.3)
				dpi = 500
			else:  
				#either landscape or if not defined
				fig.set_size_inches(9.84, 5.9)	
				dpi = 500

			#Margin size of plot					
			if showTable:
				#plt.subplots_adjust(bottom=0.35,right=0.74,top=0.92,hspace=0.25,wspace=0.35)
				plt.subplots_adjust(bottom=0.28,right=0.70,left=0.08,top=0.89,hspace=0.5,wspace=0.5)	
			else:
				plt.subplots_adjust(bottom=0.11,right=0.70,left=0.08) #Margin size of plot

			plt.savefig(img_file_path+curTime+saveFile, dpi=dpi, format=PRINT_FORMAT)
			print(str(incr)+" : " +curTime+saveFile)	
			incr=incr+1
			#plt.show()
	except Exception as e:	
		print("Something Went wrong at OIC chart! Unable to process your request.")
		print(e)




#reading file arguments
from args_reader import *
print("\nOIC graph file generation started:")
salesGrowth(SaveFileType,LineType,FileFormat,TableShow)
