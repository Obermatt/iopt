# Reading csv data for charts
import os
import csv
import DateTime
import matplotlib.pyplot as plt
import numpy as np

def readData():
	#readFileNameParam = sys.argv[1] #read CSV file	
	finalArr1 = []
	for readFileNameParam in os.listdir("file/"): # Read All the files inside file folder
		if readFileNameParam.endswith(".csv") and readFileNameParam.startswith("ok"): #Read only CSV file & start with ok name
			filename = 'file/'+readFileNameParam			
			csvRowCount	 = 0;	
			data = {}	
			arrFirst = []
			arrTwo = []
			arrThree = []
			arrFour = []
			arrFive = []
			arrSix = []
			arrSeven = []
			arrEight = []
			finalArr	= {}
			perExist = False	
			with open(filename,'rt') as file: # Read CSV file
				reader=csv.reader(file)
				data=list(reader)				
				for csvRow in data:
					#Auto increament	
					csvRowCount = csvRowCount + 1 		
					if csvRowCount == 1:
						#X axis value escape last 3 row
						arrFirst = csvRow[:-5]
						arrSix = csvRow[:-4] 
						continue
					# All Legend name
					arrTwo.append(csvRow[len(csvRow) - 5])
					if any("%" in str for str in csvRow): #to check value is in percentage format or normal format
						perExist = True; # if percentage value exist in CSV file
					# cutomized Legend text
					arrFour.append(csvRow[len(csvRow) - 4]) 
					# chart title
					arrFive.append(csvRow[len(csvRow) - 3])
					
					#arrSeven.append(csvRow[len(csvRow[:1]) - 2])
					if csvRowCount == 2:
						# Y mincsvRow
						arrSeven = csvRow[len(csvRow) - 2]
						# Y max
						arrEight = csvRow[len(csvRow) - 1]
			 
					#to check value is in percentage format or normal format			
					if any("%" in str for str in csvRow): 
						# if percentage value exist in CSV file
						csvRowerarrSevenExist = True 
					# replace % from the value
					csvRow = [w.replace('%', '') for w in csvRow]
					# Line multidimentional value			
					arrThree.append([np.nan if v is '' else round(float (v)) for v in csvRow[:-5]]) # replace blank value with none
				
				# Start - to get Y min & max value if user not set Y min or max value then find min max from array
				arrThree = [list(map(float, i)) for i in arrThree[:6]] # All the data
								
				arrSeven = 0
				arrEight = 100
				finalArr['xAxisName'] = arrFirst
				finalArr['legendName'] = arrTwo
				finalArr['axisValue'] = arrThree
				finalArr['axisfigtext'] = arrFour
				finalArr['title'] = arrFive  
				finalArr['perExist'] = perExist
				finalArr['tabletitle'] = arrSix
				finalArr['yMin'] = arrSeven
				finalArr['yMax'] = arrEight
				#filename without extension
								
				readFileNameParam=readFileNameParam.replace(".csv", "")
				finalArr['fileName'] = readFileNameParam
				
				finalArr1.append(finalArr)
				#final return done
	return finalArr1 

## End of program
