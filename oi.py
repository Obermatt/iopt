# importing required files and libraries
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
import CsvRead as CsvData  # imported python file for CSV read
import legend_handler as CustomeLegend
import matplotlib.font_manager as font_manager


# below function is used to convert nan value to default interpolate value between of two numbers
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


# This is to ignore warnings
import warnings

warnings.filterwarnings("ignore")

# Change format option to svg or png
PRINT_FORMAT = "png"
COMPANY_PERFORMANCE_LINE = "s"  # straight line  // i #interpolated

# defining colorcodes
# defining color and styles for various lines in chart
lightskyblue_obermatt = '#ACE3E8'
darkskyblue_obermatt = '#91CCD1'
blue_obermatt = '#2A90AC'
orange_obermatt = '#ff7802'
brown_obermatt = "#472101"


# start of function

def operatingIndex(SaveFileType, LineType, FileFormat, TableShow=None):
    try:
        # validate parmas when run script from command line
        from path_config import img_file_path

        # ReadData = CsvData.readData() # read CSV data
        dataRead = CsvData.readData()  # read CSV data multiple file
        incr = 1
        for ReadData in dataRead:
            ##Start of font setting
            matplotlib.font_manager._rebuild()
            fontpath = 'AGaramondPro-Regular.otf'
            prop = font_manager.FontProperties(fname=fontpath)
            titlefont = {'fontname': prop.get_name()}
            legendfont = prop.get_name()
            plt.rcParams['font.family'] = 'Arial'
            ##End of font setting

            now = datetime.datetime.now()
            curTime = now.strftime("%Y_%m_%d")

            # Reading filename from arguments
            PRINT_FORMAT = SaveFileType

            # Reading printing mode (landscape[l] or portrait[p])
            saveFileSizeParam = FileFormat

            # Reading line format for company performance straight line or interpolated
            COMPANY_PERFORMANCE_LINE = LineType

            # Reading input data filename
            saveinputFile = ReadData['fileName']

            # save path from export_path.py
            saveFile = "_oi_" + saveinputFile + "_" + LineType + "_" + saveFileSizeParam

            # reading chart title (#titleName = 'Operating Index \nEBIT Margin' # Static Title Entry)
            titleName = ReadData['title'][0]
            titleName = titleName.replace('\\n', '\n')

            # table titleseq
            tabletitleName = ReadData['tabletitle'][-1]

            color = [darkskyblue_obermatt, blue_obermatt, lightskyblue_obermatt, orange_obermatt,
                     blue_obermatt]
					 
			# line type
            style = ['-', '-', '-', '-', '']

			# Marker type		
            marker = ['', '', '', 'o', '']  

            # legend names reading from csv data file
            legendLabel = ReadData['legendName']

            # company name (reading from CSV data file)
            compname = legendLabel[3]

            # Check if CSV file value is in percentage or not
            percentageExist = ReadData["perExist"]
            percentageFormat = '{:3.1f}'
            percentageFormatYLables = '{:3.0f}%'
            if percentageExist: percentageFormat = '{:3.1f}%'
            intFormat = '{:3.0f}'
			
            # Marker width size
            markerSize = 5

            # Line width value
            lineWidthArr = [2, 1, 2, 1, 1]

            # Orange and blue Line width
            lineWidth = 1.5  

			# company name row id
            dottedKey = 0  

			# marker color
            markerColor = '#ff6100'  

            # title font size
            titleSize = 16

            # number font size
            numberFontSize = 10.5

            plt.figure()
			
			#Disabling Autoscale for y axis
            plt.autoscale(enable=False, axis='y');
            ax = plt.subplot()

            # hide right and left line of chart
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            #ax.spines['bottom'].set_position(('axes', -0.005))
            #ax.spines['top'].set_position(('axes', 1.005))

            # X Axis Data points
            x = np.array(list(range(len(ReadData['xAxisName']))))

            # Static Y Axis Data points
            yAxisValue = np.array(ReadData['axisValue'])

            # added below to set Y axis value static & dynamic Start
            yMin = ReadData['yMin']
            yMax = ReadData['yMax']
            y = np.array(yAxisValue)
            plt.ylim(int(yMin), int(yMax))

            # x Axis Data points
            my_xticks = ReadData['xAxisName']

            # set X axis replace static number with original key value
            plt.xticks(x, my_xticks, fontsize=numberFontSize)
			
            # interpolation technique is used to convert the straight line with curve --  Importing base library
            from scipy import interpolate

            # 0- companydata
            # 1-75 Percentile
            # 2-Median
            # 3-25 Percentile
            # 4-Count
			
			# COLOR_CODE of line
            color = [orange_obermatt, 
					lightskyblue_obermatt, 
					blue_obermatt, 
					darkskyblue_obermatt,
                    blue_obermatt]  

            # Loop start count
            count = 0
            fillData = {}
            lastcolumncount = len(y) - 1
            
            for data in y:
                if count == 0 and COMPANY_PERFORMANCE_LINE == "s":
                    f = interpolate.interp1d(np.arange(len(data)), data, kind='linear')
                else:
                    # interpolate value if found Nan value in array
                    data = np.array(data)
                    nans, xdata = nan_helper(data)
                    data[nans] = np.interp(xdata(nans), xdata(~nans), data[~nans])
					
                    # Draw Curve Linenan
                    if count == 0:
                        f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic')  #
                    else:
                        f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic')
				
                xnew = np.arange(0, len(data) - 1, 0.01)
                ynew = f(xnew)

                fillData[count] = f(xnew)
                # Set plot final plot
                if count == 0:
                    plt.plot(xnew, ynew, color=color[count], linestyle=style[count], markersize=markerSize,
                             linewidth=lineWidthArr[count], label=legendLabel[count], zorder=102)
                else:
                    if count == 2:
                        plt.plot(xnew, ynew, color=color[count], linestyle=style[count], markersize=markerSize,
                                 linewidth=lineWidthArr[count], label=legendLabel[count], zorder=101)
                    else:
                        plt.plot(xnew, ynew, color=color[count], linestyle=style[count], markersize=markerSize,
                                 linewidth=lineWidthArr[count], label=legendLabel[count], zorder=99)
                count = count + 1

            # Fill color between two line start
            # from y0 to y1
            fill1 = [1, 2]
            # from y1 to y2
            fill2 = [2, 3]
            # COLOR_CODE
            colorFill = [lightskyblue_obermatt, darkskyblue_obermatt]
            count1 = 0
            for a, b in zip(fill1, fill2):
                plt.fill_between(xnew, fillData[a], fillData[b], color=colorFill[count1], alpha='1', interpolate=True,
                                 zorder=100)
                count1 = count1 + 1

            # first add orange marker without line
            plt.plot(y[dottedKey], color=markerColor, linestyle='', markersize=markerSize, linewidth=lineWidth,
                     marker='o', zorder=102);

            # added to display value on marker
            for i, j in zip(x, y[dottedKey]):
                # converted values into percentage value
                ax.annotate(percentageFormat.format(j), xy=(i, j), horizontalalignment='right',
                            verticalalignment='bottom', fontsize=numberFontSize, zorder=103)

            vals = ax.get_yticks()
            # converted values into percentage value
            ax.set_yticklabels([percentageFormatYLables.format(x) for x in vals], fontsize=numberFontSize)
            # Display table or not based on parameter passed by user, by default table will display on graph, 0 -> dont display table, 1 -> Display table
            try:
                TableShow  # Parameter which is entered by user
            except Exception as e:
                showTable = False  # default display Table
                # boxx=0.26
                # boxy=-0.15
                boxx = 1.35
                boxy = 0.58
            else:
                showTable = False
                # boxx=0.26
                # boxy=-0.15
                boxx = 1.35
                boxy = 0.58
                if TableShow == 't':  # if user enter 1 display table else dont display the table
                    showTable = True
                    boxx = 1.35
                    boxy = 0.58
                    saveFile += "_t"

            saveFile += "." + PRINT_FORMAT

            plt.xticks(x, my_xticks, fontsize=numberFontSize)

            # ---------------------------------------Code for Showing table started------------------------
            count4 = 0
            if showTable:
                # -------------- Data Table start-----------------------

                yx = y

                y_without_nan = y
                y_without_nan_formatted = [[intFormat.format(k) for k in l] for l in y_without_nan]

                y_without_nan_formatted[:-1] = y[:-1]
                y_without_nan_formatted = np.array(y_without_nan_formatted)

                the_table = plt.table(cellText=y_without_nan_formatted, colLabels=my_xticks, loc='bottom',
                                      cellLoc='right', colLoc='right', rowLoc='left')
                the_table.set_fontsize(numberFontSize)
                the_table.scale(1, 1.2)

                # Remove Border of table 1 cell
                for key, cell in the_table.get_celld().items():
                    cell.set_linewidth(0)
                # -------------------Data Table end--------------------------

                # ---------------right side table of company name start------------------------------
                my_xticks_1 = [tabletitleName]

                legendLabel_1 = np.reshape(legendLabel, (-1, 1))
                the_table1 = plt.table(cellText=legendLabel_1, colLabels=my_xticks_1, loc='bottom right',
                                       colLoc='bottom center', rowLoc='bottom left', animated=True)
                # the_table1.auto_set_column_width([-1,0,1]) # set column width
                the_table1.set_fontsize(numberFontSize)
                the_table1.scale(.5, 1.5)
                cells = the_table1.properties()["celld"]

                # row text left align
                cellLength = len(legendLabel)  # length of row
                for i in range(0, cellLength + 1):
                    cells[i, 0]._loc = 'left'

                # Remove Border of table 2 cell
                for key, cell in the_table1.get_celld().items():
                    cell.set_linewidth(0)

                # -------------------------right side table of company name end-------------------------------------

                # plt.xticks([]) # remove x Axis values, already put value using table
                my_xticks = ['', '', '', '', '', '', '', '', '', '']
                plt.tick_params(
                    axis='x',  # changes apply to the x-axis
                    which='both',  # both major and minor ticks are affected
                    bottom='off',  # ticks along the bottom edge are off
                    top='off',  # ticks along the top edge are off
                    labelbottom='off')  # labels along the bottom edge are off
                # set X axis replace static number with original key value
                plt.xticks(x, my_xticks, fontsize=numberFontSize, ha="right")
            # ---------------------------------------Code for Showing table Ended------------------------

            # Set Graph title

            plt.title(titleName, loc='left', fontsize=titleSize, fontweight="regular", color=brown_obermatt,
                      **titlefont)

            fig = plt.gcf()
            # defining portrait or landscape mode
            if saveFileSizeParam == 'p':
                fig.set_size_inches(10.3, 7.3)
                dpi = 500
            else:
                fig.set_size_inches(9.84, 5.9)
                dpi = 500

            # -------------------- Start of designing custome legends------------------------
            m2, = ax.plot([], [])
            m3, = ax.plot([], [])
            m3, = ax.plot([], [], color='#ffffff', marker='', markersize=2, fillstyle='bottom', linestyle='none',
                          linewidth=1)
            m4, = ax.plot([], [], color=orange_obermatt, marker='o', linestyle='none', solid_joinstyle='round',
                          linewidth=1)

            legendtext1 = ReadData['axisfigtext'][0]
            legendtext2 = ReadData['axisfigtext'][1]

            # setup the handler instance for the scattered data
            custom_handler = CustomeLegend.ImageHandler()
            custom_handler.set_image('./legend_images/legend1.png', image_stretch=(10, 1))

            custom_handler2 = CustomeLegend.ImageHandler()
            custom_handler2.set_image('./legend_images/legend2.png', image_stretch=(10, 1))

            if saveFileSizeParam == "l":
                plt.legend([m2, m3],
                           [legendtext1, legendtext2],
                           handler_map={m2: custom_handler, m3: custom_handler2},
                           labelspacing=1, loc='right', bbox_to_anchor=(boxx, boxy), frameon=False,
                           prop={'family': legendfont, 'size': 11})
            else:
                plt.legend([m2, m3],
                           [legendtext1, legendtext2],
                           handler_map={m2: custom_handler, m3: custom_handler2},
                           labelspacing=1, loc='right', bbox_to_anchor=(boxx, boxy), frameon=False,
                           prop={'family': legendfont, 'size': 11})

            # -------------------- End of designing custome legends------------------------

            if showTable:
                plt.subplots_adjust(bottom=0.35, right=0.74, top=0.89, hspace=0.5, wspace=0.5)
            # plt.subplots_adjust(bottom=0.35,right=0.8,hspace=0.5,wspace=0.5) #Margin size of plot
            else:
                plt.subplots_adjust(bottom=0.18, right=0.74)  # Margin size of plot

            plt.savefig(img_file_path + curTime + saveFile, dpi=dpi, format=PRINT_FORMAT)
            # plt.savefig(img_file_path+curTime+saveFile, dpi=dpi, bbox_inches='tight', format=PRINT_FORMAT)

            # plt.show()
            print(str(incr) + " : " + curTime + saveFile)
            incr = incr + 1

    except Exception as e:

        print("Something Went wrong at Oi chart! Unable to process your request.")
        print(e)
    ## End of program


# reading file arguments
from args_reader import *

print("\nOI graph file generation started:")
operatingIndex(SaveFileType, LineType, FileFormat, TableShow)
