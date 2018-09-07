import sys
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import legend_handler as CustomeLegend
import CsvRead_cdax as CsvData  # imported python file for CSV read

import matplotlib.font_manager as font_manager
import warnings
import matplotlib.patheffects as pe

warnings.filterwarnings("ignore")



# below function is used to convert nan value to default interpolate value between of two numbers
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


def cdaxGraph():
    try:
        from path_config import img_file_path

        dataRead = CsvData.readData()  # read CSV data multiple file

        incr = 1
        
        for ReadData in dataRead:
            saveinputFile = ReadData['fileName']
            saveFile = "_CDAX_" + saveinputFile + "." + SaveFileType
            now = datetime.datetime.now()
            curTime = now.strftime("%Y_%m_%d")
            
            matplotlib.font_manager._rebuild()
            fontpath = 'AGaramondPro-Regular.otf'
            prop = font_manager.FontProperties(fname=fontpath)
            garamondFont = {'fontname': prop.get_name()}
            #plt.rcParams['font.family'] = 'Arial'
            plt.figure()
            plt.autoscale(enable=False, axis='y');
            ax = plt.subplot()

            ax.spines['right'].set_visible(False)  # hide right line of chart
            ax.spines['left'].set_visible(False)  # hide left line of chart
            ax.spines['top'].set_visible(False)  # hide top line of chart
            ax.spines['bottom'].set_visible(False)  # hide bottom line of chart
            
            barValues = []
            barYValue = 90
            decrementBy = 2 #bardecrement
            diffValue = 12
            diffSpace = 12
            incr2 = 0
            axisValues = ReadData['axisValues']
            axisNames = ReadData['axisNameValues']
            
            y = np.array(axisValues)
            
            for row in y:
                barValues.append(barYValue)
                rowStart = 10
                for m in row:
                    y1 = barYValue
                    x1 = rowStart
                    
                    y2 = barYValue
                    x2 = rowStart + diffValue 
                    
                    fix_y = np.array([y1, y2])
                    fix_x = np.array([x1, x2])

                    m1 = np.nan if m is '' else int(round(float (m)))
                    percvaluex = x1 + (m1 * diffValue / 100)

                    y_new = fix_y
                    x_new = np.array([x1,percvaluex])
                    
                    plt.plot(fix_x, fix_y, color="lightgray", linewidth=10.5)# Set plot final plot
                    plt.plot(fix_x, fix_y, color="white", linewidth=10)  # Set plot final plot
                    
                    if(m1<24):
                        colorValue = "#ec5958" #"red"
                    else:
                        if(m1<50):
                            colorValue = "#f8f17f" #"yellow"
                        else:
                            if(m1<75):
                                colorValue = "#b0d754" #"lightgreen"
                            else:
                                colorValue = "#79a240" #"green"
                            
                        
                    plt.plot(x_new, y_new, color=colorValue,linewidth=10)  # Set plot final plot
                    ax.annotate(m1,xy=(x1-2,y1-0.4),horizontalalignment='right',verticalalignment='bottom',fontsize=5, zorder=105,**garamondFont)	#converted values into percentage value	
                    rowStart = x2 + diffSpace
                    
                incr2 = incr2+1
                barYValue = barYValue - decrementBy
                
            plt.xticks([])
            ax.axis([0,102,barYValue-10,100])
            yax = ax.set_yticks(barValues)
            yax = ax.get_yticks()
            ax.set_yticklabels(axisNames, fontsize=5, horizontalalignment='right',**garamondFont)
            ax.yaxis.set_tick_params(length=0)
            plt.subplots_adjust(left=0.6, right=0.99, top=1, bottom=0.2)
            plt.tight_layout()
            plt.savefig(img_file_path + curTime + saveFile,dpi=1500, format=SaveFileType)
            plt.show()    
    except Exception as e:
        print("Something Went wrong at OK chart! Unable to process your request.")
        print(e)

        
SaveFileType = sys.argv[1] 

showSyntax = False
try:
	# svg or png
	SaveFileType = sys.argv[1] 

except Exception as e:
	showSyntax=True
    
if showSyntax==False:
	if SaveFileType!="png" and SaveFileType!="svg":
		showSyntax=True

if showSyntax==True:
	print("Invalid param values")
	print("Correct syntax is as follows:")
	print("\t Parameters: <outputformat>")
	print("\t\t output formats -- svg / png")
else:
    print("\nCDAX graph file generation started:")
    cdaxGraph()