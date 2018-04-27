import matplotlib
import matplotlib.pyplot as plt 

x=[0,1,2,3,4]
y=[[2.56422, 3.77284,3.52623,3.51468,3.02199],[4.56422, 1.77284,3.52623,3.51468,3.02199]]


fig, ax = plt.subplots()
#ax.scatter(z, y)
"""
for k in x:
	#print(k[1])
	for l in k:
		print(l)
		print(l[y])
exit()
"""
count = 1
for i,j in zip(x,y):
	print("-----------")
	print(i)	
	print(j[i])
	ax.annotate(j[i],xy=(i,j[i]),horizontalalignment='right',verticalalignment='bottom')	#converted values into percentage value	
	count = count+1
#exit()
#for i, txt in enumerate(n):
    #ax.annotate(txt, (z[i],y[i]))
#plt.show()
