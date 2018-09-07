# Reading csv data for charts
import os
import csv
import DateTime
import matplotlib.pyplot as plt
import numpy as np

def readData():

    from path_config import csv_file_path

    #readFileNameParam = sys.argv[1] #read CSV file	
    finalArr1 = []
    for readFileNameParam in os.listdir(csv_file_path): # Read All the files inside file folder
        if readFileNameParam.endswith(".csv") and readFileNameParam.startswith("bar"): #Read only CSV file & start with ok name
            filename = csv_file_path+readFileNameParam			
            csvRowCount	 = 0;	
            data = {}	
            axisValues = []
            axisNameValues = []
            finalArr = {}
            
            with open(filename,'rt') as file: # Read CSV file
                reader=csv.reader(file)
                data=list(reader)				
                for csvRow in data:
                    #Auto increament	
                    csvRowCount = csvRowCount + 1 		
                    axisNameValues.append(csvRow[4])
                    axisValues.append(csvRow[:4])
                
                finalArr['axisNameValues']=axisNameValues
                finalArr['axisValues']=axisValues
                #filename without extension
                #print(finalArr)           
                readFileNameParam=readFileNameParam.replace(".csv", "")
                readFileNameParam=readFileNameParam.replace("bar_", "")

                finalArr['fileName'] = readFileNameParam
                finalArr1.append(finalArr)
                #final return done
            
    return finalArr1 

## End of program
