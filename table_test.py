import matplotlib
import matplotlib.pyplot as plt 
data = [[  "",  174296,   75131,  577908,   32015],
        [  58230,  381139,   78045,   99308,  160454],               
        [ 139361,  331509,  343164,  781380,   52269]]
     
columns = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')        
the_table = plt.table(cellText=data,colLabels=columns,loc='bottom',cellLoc='right',colLoc='top',rowLoc='left')		
plt.subplots_adjust(left=0.2, bottom=0.2)
plt.show()

		
