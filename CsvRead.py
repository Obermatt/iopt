# Reading csv data for charts
import os
import csv
import sys
import DateTime
import matplotlib.pyplot as plt
import numpy as np

def readData():		
	readFileNameParam = sys.argv[3] #read CSV file
	filename = 'file/'+readFileNameParam
	csvRowCount	 = 0;	
	data = {}	
	arrFirst = []
	arrTwo = []
	arrThree = []
	arrFour = []
	arrFive = []
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
				arrFirst = csvRow[:-3] 
				continue
			# All Legend name
			arrTwo.append(csvRow[len(csvRow) - 3])
 			# cutomized Legend text
			arrFour.append(csvRow[len(csvRow) - 2]) 
			# chart title
			arrFive.append(csvRow[len(csvRow) - 1]) 
			#to check value is in percentage format or normal format			
			if any("%" in str for str in csvRow): 
				# if percentage value exist in CSV file
				perExist = True 
			# replace % from the value
			csvRow = [w.replace('%', '') for w in csvRow] 
			# Line multidimentional value
			arrThree.append(csvRow[:-3]) 
			
		
		finalArr['xAxisName'] = arrFirst
		finalArr['legendName'] = arrTwo
		finalArr['axisValue'] = arrThree
		finalArr['axisfigtext'] = arrFour
		finalArr['title'] = arrFive  
		finalArr['perExist'] = perExist
	#final return done	
	return finalArr 

## End of program
