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
	finalArr	= {}
	perExist = False
	with open(filename,'rt') as file: # Read CSV file
		reader=csv.reader(file)
		data=list(reader)
		
		for csvRow in data:
			csvRowCount = csvRowCount + 1 #Auto increament			
			if csvRowCount == 1:
				arrFirst = csvRow[:-1] #X axis value escape last row
				continue
			arrTwo.append(csvRow[len(csvRow) - 1]) # Legend name						
			if any("%" in str for str in csvRow): #to check value is in percentage format or normal format
				perExist = True # if percentage value exist in CSV file
			csvRow = [w.replace('%', '') for w in csvRow] # replace % from the value
			arrThree.append(csvRow[:-1]) # Line multidimentional value
		
		finalArr['xAxisName'] = arrFirst
		finalArr['legendName'] = arrTwo
		finalArr['axisValue'] = arrThree 
		finalArr['perExist'] = perExist
		
	return finalArr #final return done