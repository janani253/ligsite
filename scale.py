#!/usr/llocal/env python

from numpy import *
import re

fi = open("india.dat","r")

lines = fi.readlines()
fi.close()
lines = [re.sub("\n","",temp) for temp in lines]
lines = filter(None, lines)

x = [float(re.sub(" .*","",temp)) for temp in lines]
y = [float(re.sub(".* ","",temp)) for temp in lines]

# Converting range of coordinates into a 0-100 A scale

def convert_to_100(a):
	amax = max(a)
	amin = min(a)
	A = array([[amax,1],[amin,1]])
	b = array([100,0])
	(c,d) = linalg.solve(A,b)
	a = [(temp*c)+d for temp in a]	
	return a

x = convert_to_100(x)
y = convert_to_100(y)

lines=[]

fo = open('scaled_india.csv',"w")
for x1,y1 in zip(x,y):
	temp ="%f,%f\n" %(x1,y1)
	fo.write(temp)

fo.close()
print "X,Y coordinates of India map scaled to the 0-100A scale have been written to scaled_india.csv"

try:
	os.system("Rscript plot_scaled.r")	
	print "The X,Y coordinates of the scaled India map have also been plotted into scaled_india.pdf"
except:
	pass



