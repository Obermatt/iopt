import sys
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import legend_handler as CustomeLegend
import CsvRead_bar as CsvData  # imported python file for CSV read

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
            saveFile = "_bar_" + saveinputFile + "_" + outputType + "." + SaveFileType
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
            #ax.spines['left'].set_position(('axes',5))
            ax.spines['bottom'].set_position(('axes',5))
            ax.spines['left'].set_visible(False)  # hide left line of chart
            
            ax.spines['top'].set_visible(False)  # hide top line of chart
            ax.spines['bottom'].set_visible(False)  # hide bottom line of chart
            
            barValues = []
            barYValue = 100
            decrementBy = 12 #bardecrement
            diffValue = 10
            diffSpace = 10
            incr2 = 0
            axisValues = ReadData['axisValues']
            axisNames = ReadData['axisNameValues']
            
            y = np.array(axisValues)
            
            for row in y:
                barValues.append(barYValue)
                rowStart = 30
                for m in row:
                    y1 = barYValue
                    x1 = rowStart
                    
                    y2 = barYValue
                    x2 = rowStart + diffValue 
                    
                    fix_y = np.array([y1, y2])
                    fix_x = np.array([x1, x2])

                    if(incr2==0):
                        #adding title to the columns
                        ax.annotate(m,xy=(x1-4,y1-3),color='#2e91ad', horizontalalignment='left',verticalalignment='bottom',fontsize=9, zorder=105,**garamondFont)	#converted values into percentage value	
                        rowStart = x2 + diffSpace
                    else:
                        m1 = np.nan if m is '' else int(round(float (m)))
                        percvaluex = x1 + (m1 * diffValue / 100)

                        y_new = fix_y
                        x_new = np.array([x1,percvaluex])
                        
                        plt.plot(fix_x, fix_y, color="lightgray", linewidth=10.5)# Set plot final plot
                        plt.plot(fix_x, fix_y, color="white", linewidth=10)  # Set plot final plot
                        
                        if(m1<24):
                            colorValue = "#E24C4C" #"red"
                        else:
                            if(m1<50):
                                colorValue = "#F2EA48" #"yellow"
                            else:
                                if(m1<75):
                                    colorValue = "#A4CB49" #"lightgreen"
                                else:
                                    colorValue = "#6C8E40" #"green"
                        
                        plt.plot(x_new, y_new, color=colorValue,linewidth=10)  # Set plot final plot
                        ax.annotate(m1,xy=(x1-2,y1-4),horizontalalignment='right',verticalalignment='bottom',fontsize=7, zorder=105,**garamondFont)	#converted values into percentage value	
                        rowStart = x2 + diffSpace
                    
                incr2 = incr2+1
                barYValue = barYValue - decrementBy

            plt.xticks([])
            ax.axis([0,102,barYValue-10,110])
            yax = ax.set_yticks(barValues)
            yax = ax.get_yticks()
            ax.set_yticklabels(axisNames, fontsize=9, horizontalalignment='left',**garamondFont)
            ax.get_yticklabels()[0].set_color("#2e91ad")
            ax.yaxis.set_tick_params(length=0)
            plt.tight_layout()
            if outputType == "blog":
                dpi = 385
            else:
                dpi = 591
                plt.subplots_adjust(left=0.10, right=0.90)
            
            finalFileName = curTime + saveFile
            
            # defining size for landscape mode 
            fig = plt.gcf()
            
            if(incr2<3):
                height = 0.6 *  (incr2/1.5)
            else:
                if(incr2<5):
                    height = 0.6 *  (incr2/1.8)
                else:
                    height = 0.6 *  (incr2/2.2)
            
            headerSpace = 0.3
            
            fig.set_size_inches(6.5, height+headerSpace)
            if outputType == "blog":
                dpi = 385
            else:
                dpi = 591
            
            
            plt.savefig(img_file_path + finalFileName,dpi=dpi, format=SaveFileType,  transparent=True)
            print(str(incr) + " : " + finalFileName);
            incr = incr + 1
    except Exception as e:
        print("Something Went wrong at OK chart! Unable to process your request.")
        print(e)

        
outputType = ""
showSyntax = False
try:
    # svg or png
    SaveFileType = sys.argv[1]

except Exception as e:
    showSyntax=True

try:    
    if sys.argv[0] == "bar.py":
        outputType = sys.argv[2] 

except Exception as e:
    outputType = "blog"

    
if showSyntax==False:
    if SaveFileType!="png" and SaveFileType!="svg":
        showSyntax=True
    if outputType!="video" and outputType!="blog":
        outputType = "blog"

if showSyntax==True:
    print("Invalid param values")
    print("Correct syntax is as follows:")
    print("\t Parameters: <outputformat>")
    print("\t\t output formats -- svg / png")
    print("\t\t output required for -- video / blog")
else:
    print("\nBar graph file generation started:")
    cdaxGraph()