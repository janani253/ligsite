#! /usr/local/env python

# This program fills the grid for the body of the protein, given the protein outline 

from numpy import *
from collections import *

fi = open("scaled_india.csv","r")
xy = fi.readlines()

xy = [temp.replace("\n","") for temp in xy]
xy = array([temp.split(",") for temp in xy])

xy1 = []
for temp in xy:
	x = float(temp[0])
	y = float(temp[1])
	t = x - floor(x)
	if t<=0.25:
		x = floor(x)
	elif t<=0.75:
		x = floor(x) + 0.5
	else:
		x = ceil(x)
	t = y - floor(y)
	if t<=0.25:
		y = floor(y)
	elif t<=0.75:
		y = floor(y) + 0.5
	else:
		y = ceil(y)
	if [x,y] not in xy1:
		xy1.append([x,y])

xy = xy1[:]	

gridx = defaultdict(dict)
gridy = defaultdict(dict)
grid = defaultdict(dict)

# y-axis scan
for i in range(0,201):
	first = 0
	last = 0
	for j in range(0,201):
		temp = [i/2.0,j/2.0] 
		gridx[i/2.0][j/2.0] = 0
		if temp in xy:
			first = j
			break
		
	for j in range(201,0,-1):
		temp = [i/2.0,j/2.0] 
		gridx[i/2.0][j/2.0] = 0
		if temp in xy:
			last = j
			break	
	for j in range(first,last):
		gridx[i/2.0][j/2.0] = -1

# x-axis scan
for j in range(0,201):
	first = 0
	last = 0
	for i in range(0,201):
		temp = [i/2.0,j/2.0] 
		gridy[i/2.0][j/2.0] = 0
		if temp in xy:
			first = i
			break
	
	for i in range(201,0,-1):
		temp = [i/2.0,j/2.0] 
		gridy[i/2.0][j/2.0] = 0
		if temp in xy:
			last = i
			break	
	for i in range(first,last):
		gridy[i/2.0][j/2.0] = -1
		
x = []
y = []
fo = open("india_filled.csv","w")
# Combining x and y axes scans
for i in range(0,201):
	for j in range(0,201):
		grid[i/2.0][j/2.0] = gridx[i/2.0][j/2.0] * gridy[i/2.0][j/2.0]
		if grid[i/2.0][j/2.0]!=0:
			x.append(i/2.0)
			y.append(j/2.0)
			fo.write("%f,%f\n" %(i/2.0,j/2.0))
		
fo.close()

print "The filled protein grid/coordinates have been written into india_filled.csv"

try:
	os.system("Rscript plot_filled.r")	
	print "The X,Y coordinates of the filled India map/protein have also been plotted into india_filled.pdf"
except:
	pass
