import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import legend_handler as CustomeLegend
import CsvRead_Ok as CsvData  # imported python file for CSV read
import matplotlib
import matplotlib.font_manager as font_manager
import warnings

warnings.filterwarnings("ignore")


# Change format option to svg or png
PRINT_FORMAT = "png"


# defining colorcodes
orange_obermatt = '#ff7802'
red_obermatt = '#a53332'
yellow_obermatt = '#ffdc00'
green_obermatt = '#2eaa60'
violett_obermatt = '#593794'
lila_obermatt = '#9d2fa3'
brown_obermatt = "#472101"
lightskyblue_obermatt = '#ACE3E8'
darkskyblue_obermatt = '#91CCD1'
blue_obermatt = '#2A90AC'


# below function is used to convert nan value to default interpolate value between of two numbers
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]


# parameter: {filename}.py {savefilename} {filesize} {sourcecsvfile}.csv {table show[0,1]}

def okGraph(SaveFileType, LineType, FileFormat, TableShow=None):
    try:
        from path_config import img_file_path

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

            saveFileNameParam = ReadData['fileName']  # Read first param

            # title font size
            titleSize = 16

            markerSize = 5  # Marker width size
            lineWidth = 2  # Line width valuesaveFileNameParam
            count = 0  # Loop start count
            dottedKey = 0  # define where we need a dotted key on which line
            titleName = ReadData['title'][0]
            titleName = titleName.replace('\\n', '\n')
            tabletitleName = ReadData['tabletitle'][-1]

            replaceCountWord = 'Count'

            saveinputFile = ReadData['fileName']
            saveFile = "_ok_" + saveinputFile + "_" + LineType + "_" + saveFileSizeParam

            # color code of line
            color = [orange_obermatt, red_obermatt, yellow_obermatt, green_obermatt, violett_obermatt, lila_obermatt]
            style = ['-', '-', '-', '-', '-', '-']  # line type
            marker = ['o', 'o', 'o', 'o', 'o', 'o']  # Marker type				legendLabel = ReadData['legendName'] # legend name
            legendLabel = ReadData['legendName']  # legend name

            legendLabel1 = ReadData['legendName']  # legend name

            # replace Count word with _nolegend_. not required to display Count in legend
            legendLabel1 = [w.replace(replaceCountWord, '_nolegend_') for w in legendLabel1]
            numberFontSize = 10.5

            # Check if CSV file value is in percentage or not
            percentageExist = ReadData["perExist"]
            percentageFormat = '{:3.0f}'
            # if percentageExist: percentageFormat = '{:3.0f}%'
            intFormat = '{:3.0f}'
            # Plot size margin from Bottom
            # plt.subplots_adjust(bottom=0.2,left=2.5,right=3.5)

            # -- Start Plot  --
            plt.figure()
            plt.autoscale(enable=False, axis='y');
            ax = plt.subplot()

            ax.spines['right'].set_visible(False)  # hide right line of chart
            ax.spines['left'].set_visible(False)  # hide left line of chart
            ax.spines['bottom'].set_position(('axes', -0.005))
            ax.spines['bottom'].set_linewidth(0.5)
            ax.spines['top'].set_position(('axes', 1.005))
            ax.spines['top'].set_linewidth(0.5)
            x = np.array(list(range(len(ReadData['xAxisName']))))  # X values total count

            yAxisValue = ReadData['axisValue']  # Y values data from CSV
            # added below to set Y axis value static & dynamic Start
            yMin = ReadData['yMin']
            yMax = ReadData['yMax']
            y = np.array(yAxisValue)
            # plt.ylim(int(yMin),int(yMax))

            ax.set_yticks([0, 25, 50, 75, 100])
            vals = ax.get_yticks()

            # Converted values into percentage value
            ax.set_yticklabels([percentageFormat.format(x) for x in vals], fontsize=numberFontSize)

            my_xticks = ReadData['xAxisName']  # X values data from CSV

            from scipy import interpolate  # interpolate is used to convert the streight line with curve
            minY = 0
            maxY = 100
            legend_elements = []
            fillData = {}
            for data in y:
                if LineType == "s":
                    f = interpolate.interp1d(np.arange(len(data)), data, kind='linear')
                    xnew = np.arange(0, len(data) - 1, 0.01)
                    ynew = f(xnew)
                    # to set a curve line iprint(nstead of streight line End
                    plt.plot(xnew, ynew, color=color[count], linestyle=style[count], markersize=markerSize,
                             linewidth=lineWidth, label=legendLabel[count], zorder=101)  # Set plot final plot
                    legend_elements.append(
                        Line2D([0], [0], color=color[count], label=legendLabel1[count], linestyle=style[count],
                               markersize=markerSize, linewidth=lineWidth, marker=marker[count]))  # to set the legend
                    plt.plot(y[count], color=color[count], linestyle='', markersize=markerSize, linewidth=lineWidth,
                             marker='o', zorder=102);
                    # ax.annotate(percentageFormat.format(data[count]),xy=(i,y[count]),horizontalalignment='right',verticalalignment='bottom',fontsize=numberFontSize,zorder=103)	#converted values into percentage value
                    fillData[count] = f(xnew)
                else:
                    # interpolate value if found Nan value in array
                    data = np.array(data)
                    nans, xdata = nan_helper(data)
                    data[nans] = np.interp(xdata(nans), xdata(~nans), data[~nans])
                    # to set a curve line instead of streight line Start
                    f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic')  # Interpolate Line
                    xnew = np.arange(0, len(data) - 1, 0.01)
                    ynew = f(xnew)

                    for yn in ynew:
                        if yn > maxY:
                            maxY = yn
                        if yn < minY:
                            minY = yn

                    # to set a curve line iprintinstead of streight line End
                    plt.plot(xnew, ynew, color=color[count], linestyle=style[count], markersize=markerSize,
                             linewidth=lineWidth, label=legendLabel[count], zorder=101)  # Set plot final plot
                    legend_elements.append(
                        Line2D([0], [0], color=color[count], label=legendLabel1[count], linestyle=style[count],
                               markersize=markerSize, linewidth=lineWidth, marker=marker[count]))  # to set the legend
                    plt.plot(y[count], color=color[count], linestyle='', markersize=markerSize, linewidth=lineWidth,
                             marker='o', zorder=102);

                    fillData[count] = f(xnew)
                count = count + 1
            # End of loop
            '''
            #now setting ysticks again
            if yMax > 100:
                if yMin < 0:
                    ax.set_yticks([yMin-2, 0,25,50,75,100, yMax+2])
                else:
                    ax.set_yticks([0,25,50,75,100, yMax+5])
            else:
                if yMin < 0:
                    ax.set_yticks([yMin-2, 0,25,50,75,100])
                else:
                    ax.set_yticks([0,25,50,75,100])

            vals = ax.get_yticks()

            # hiding edge values
            #edgeValueFormat = '{:0.0}'
            edgeValueFormat = '{:0.0f}'
            newyVals =[]
            for vy in vals:
                if vy < 0:
                    vyx = " "
                else:
                    vyx = percentageFormat.format(vy)
                newyVals.append(vyx)

            ax.set_yticklabels(newyVals)
            #--end of setting ysticks again
            '''
            # from y0 to y1
            fill1 = [1, 2, 3]

            # from y1 to y2
            fill2 = [2, 3, 4]

            # COLOR_CODE
            colorFill = [darkskyblue_obermatt, blue_obermatt, lightskyblue_obermatt]
            count1 = 0
            fillArr = [25, 50, 50.5]
            fillArr1 = [50, 50.5, 75]
            for a, b in zip(fill1, fill2):
                plt.fill_between(x, fillArr[count1], fillArr1[count1], color=colorFill[count1], alpha='1',
                                 interpolate=False, zorder=100)
                count1 = count1 + 1

            # to set the legend

            # -------------------- Start of designing custom legends------------------------
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
            custom_handler.set_image('./legend_images/legend1.png', image_stretch=(3, .01))

            if saveFileSizeParam == 'p':
                legendx = 1
                legendy = 0.8
                boxx = 1.315
                if TableShow == "t":
                    boxy = 0.10
                else:
                    boxy = 0.25
            else:
                legendx = 1
                legendy = 0.95
                boxx = 1.330

                if TableShow == "t":
                    boxy = 0.10
                else:
                    boxy = 0.28

            legend1 = plt.legend([m2],
                                 [legendtext1],
                                 handler_map={m2: custom_handler},
                                 labelspacing=2, loc='right', bbox_to_anchor=(boxx, boxy), frameon=False,
                                 prop={'size': numberFontSize, 'weight': 'normal', 'family': legendfont})

            # -------------------- End of designing custome legends------------------------


            plt.legend(handles=legend_elements, bbox_to_anchor=(legendx, legendy),
                       prop={'size': numberFontSize, 'weight': 'normal', 'family': legendfont}, labelspacing=2,
                       frameon=False)
            plt.gca().add_artist(legend1)
            vals = ax.get_yticks()

            # Converted values into percentage value
            ax.set_yticklabels([percentageFormat.format(x) for x in vals], fontsize=numberFontSize)

            # Display table or not based on parameter passed by user, by default table will display on graph, 0 -> dont display table, 1 -> Display table
            try:
                TableShow  # Parameter which is entered by user
            except Exception as e:
                showTable = True  # default display Table
            else:
                showTable = False
                if TableShow == 't':  # if user enter 1 display table else dont display the table
                    showTable = True
                    saveFile += "_t"

            saveFile += "." + PRINT_FORMAT
            plt.xticks(x, my_xticks, fontsize=numberFontSize)

            if showTable:  # True display Table
                # First Table start
                # replacing y nan values with empty string
                y_without_nan = y;
                # y_without_nan[np.isnan(y_without_nan)]=0;
                tb = plt
                y_without_nan_formatted = [[intFormat.format(k) for k in l] for l in y_without_nan]
                the_table = tb.table(cellText=y_without_nan_formatted, colLabels=my_xticks, loc='bottom',
                                     colLoc='right', rowLoc='left')
                the_table.set_fontsize(numberFontSize)
                the_table.scale(1, 1.3)

                # Remove Border of table 1 cell
                for key, cell in the_table.get_celld().items():
                    cell.set_linewidth(0)
                # First Table end

                # right side table of company name start
                # my_xticks_1 = [titleName]
                my_xticks_1 = [tabletitleName]
                # print(my_xticks_1)
                legendLabel_1 = np.reshape(legendLabel, (-1, 1))

                the_table1 = tb.table(cellText=legendLabel_1, colLabels=my_xticks_1, loc='bottom right',
                                      colLoc='bottom left', rowLoc='bottom left', animated=True)
                # the_table1.auto_set_column_width([-1,0,1]) # set column width
                the_table1.set_fontsize(numberFontSize)
                the_table1.scale(.5, 1.3)
                cells = the_table1.properties()["celld"]

                # row text left align
                cellLength = len(legendLabel)  # lengtshowTableh of row
                for i in range(0, cellLength + 1):
                    cells[i, 0]._loc = 'left'

                # Remove Border of table 2 cell
                for key, cell in the_table1.get_celld().items():
                    cell.set_linewidth(0)

                # right side table of company name end

                plt.xticks([])  # remove x Axis values, already put value using table

            plt.title(titleName, loc='left', fontsize=titleSize, fontweight="regular", color=brown_obermatt,
                      **titlefont)  # Set title

            fig = plt.gcf()
            # defining portrait or landscape mode
            if saveFileSizeParam == 'p':
                fig.set_size_inches(10.3, 7.3)
                dpi = 500
            else:
                # either landscape or if not defined
                fig.set_size_inches(9.84, 5.9)
                dpi = 500

            # Margin size of plot
            if showTable:
                # plt.subplots_adjust(bottom=0.35,right=0.74,top=0.92,hspace=0.25,wspace=0.35)
                plt.subplots_adjust(bottom=0.35, right=0.74, top=0.89, hspace=0.5, wspace=0.5)
            else:
                plt.subplots_adjust(bottom=0.18, right=0.74)  # Margin size of plot

            plt.savefig(img_file_path + curTime + saveFile, dpi=dpi, format=PRINT_FORMAT)
            print(str(incr) + " : " + curTime + saveFile);
            incr = incr + 1
        # plt.show()
    except Exception as e:
        print("Something Went wrong at OK chart! Unable to process your request.")
        print(e)


from args_reader import *

print("\nOk graph file generation started:")
okGraph(SaveFileType, LineType, FileFormat, TableShow)
