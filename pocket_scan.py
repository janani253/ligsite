#! /usr/local/env python

# This program scans the X and Y axes and the diagonals to detect pockets

from numpy import *
from collections import *
import matplotlib.pyplot as plt
from operator import itemgetter
import os
import itertools

fi = open("india_filled.csv","r")
pxy = fi.readlines()
fi.close()
pxy = [temp.replace("\n","") for temp in pxy]
pxy = array([temp.split(",") for temp in pxy])

xy1 = []
for temp in pxy:
	x = float(temp[0])
	y = float(temp[1])
	if [x,y] not in xy1:
		xy1.append([x,y])

pxy = xy1[:]

psp_list = []

# y axis scan
for i in range(0,201):
	first = 0
	last = 0
	for j in range(0,201):
		temp = [i/2.0,j/2.0] 
		if temp in pxy:
			first = j
			break	
	if first == -1:
		continue	
	for j in range(200,first,-1):
		temp = [i/2.0,j/2.0] 
		if temp in pxy:
			last = j
			break	
	if last == -1:
		continue
	for j in range(first,last):
		if [i/2.0,j/2.0] not in pxy:
			psp_list.append([i/2.0,j/2.0])

# x axis scan
for j in range(0,201):
	first = -1
	last = -1
	for i in range(0,201):
		temp = [i/2.0,j/2.0]
		if temp in pxy:
			first = i
			break	
	if first == -1:
		continue
	for i in range(200,first,-1):
		temp = [i/2.0,j/2.0] 
		if temp in pxy:
			last = i
			break	
	if last == -1:
		continue
	for i in range(first,last):
		if [i/2.0,j/2.0] not in pxy:
			psp_list.append([i/2.0,j/2.0])

def diagonal_scans(i_inc,j_inc):
	global pxy
	global psp_list
# x-y diagonal scan (0,0 - 100,100) - Upper triangle
	for i in range(0,201):
		p = False
		ps = False
		ps_list = []
		psp = False
		for j,k in zip(range(i,201,j_inc),range(0,201-i,i_inc)):
			if not p:
				if [k/2.0,j/2.0] in pxy:
					p = True
			elif p:
				if [k/2.0,j/2.0] not in pxy:
					ps = True
					ps_list.append([k/2.0,j/2.0])
			if ps:
				if [k/2.0,j/2.0] in pxy:
					psp = True
					ps = False
					for psp1 in ps_list:
						psp_list.append(psp1) 
					ps_list = []
	
# x-y diagonal scan (0,0 - 100,100) - Lower triangle
	for i in range(0,201):
		p = False
		ps = False
		ps_list = []
		psp = False
		for j,k in zip(range(0,201-i,j_inc),range(i,201,i_inc)):
			if not p:
				if [k/2.0,j/2.0] in pxy:
					p = True
			elif p:
				if [k/2.0,j/2.0] not in pxy:
					ps = True
					ps_list.append([k/2.0,j/2.0])
			if ps:
				if [k/2.0,j/2.0] in pxy:
					psp = True
					ps = False
					for psp1 in ps_list:
						psp_list.append(psp1) 
					ps_list = []
	
# x-y diagonal scan (100,0 - 0,100) - Upper triangle
	for i in range(200,-1,-1):
		p = False
		ps = False
		ps_list = []
		psp = False
		for j,k in zip(range(200-i,200,j_inc),range(200,200-i,-i_inc)):
			if not p:
				if [k/2.0,j/2.0] in pxy:
					p = True
			elif p:
				if [k/2.0,j/2.0] not in pxy:
					ps = True
					ps_list.append([k/2.0,j/2.0])
			if ps:
				if [k/2.0,j/2.0] in pxy:
					psp = True
					ps = False
					for psp1 in ps_list:
						psp_list.append(psp1)
					ps_list = []
	
# x-y diagonal scan (100,0 - 0,100) - Lower triangle
	for i in range(200,-1,-1):
		p = False
		ps = False
		ps_list = []
		psp = False
		for j,k in zip(range(0,201-i,j_inc),range(200-i,-1,-i_inc)):
			if not p:
				if [k/2.0,j/2.0] in pxy:
					p = True
			elif p:
				if [k/2.0,j/2.0] not in pxy:
					ps = True
					ps_list.append([k/2.0,j/2.0])
			if ps:
				if [k/2.0,j/2.0] in pxy:
					psp = True
					ps = False
					for psp1 in ps_list:
						psp_list.append(psp1)
					ps_list = []

diagonal_scans(1,1)
#diagonal_scans(2,1)
#diagonal_scans(1,2)

xy1 = []

# Filtering by MIN_PSP event occurence

for temp in psp_list:
	if psp_list.count(temp)<2:
		continue
	x1 = float(temp[0])
	y1 = float(temp[1])
	if [x1,y1] not in xy1:
		xy1.append([x1,y1])

psp_list = xy1[:] 

# Clustering pockets
cluster = {}
psp_list.sort(key=itemgetter(0,1))
for temp in psp_list:
	x1 = float(temp[0])
	y1 = float(temp[1])
	cl = len(cluster)
	added2cl = False
	for k in range(0,cl):
		for i,j in itertools.product(range(-1,2),range(-1,2)):
			if [x1+i,y1+j] in cluster[k]:
				if [x1,y1] not in cluster[k]:
					cluster[k].append([x1,y1])
				added2cl = True
		if added2cl:
			break
	if not added2cl:
		cluster[cl] = [[x1,y1]]

psp_list.sort(key=itemgetter(1,0))
for temp in psp_list:
	x1 = float(temp[0])
	y1 = float(temp[1])
	cl = len(cluster)
	added2cl = False
	for k in range(0,cl):
		for i,j in itertools.product(range(-1,2),range(-1,2)):
			if [x1+i,y1+j] in cluster[k]:
				if [x1,y1] not in cluster[k]:
					cluster[k].append([x1,y1])
				added2cl = True
		if added2cl:
			break
	if not added2cl:
		cluster[cl] = [[x1,y1]]

# Merging clusters
change = 1
while change!=0:
	change = 0
	for i in range(0,len(cluster)):
		for temp1 in cluster[k]:
			for j in range(0,len(cluster)):
				if i == j:
					continue
				if temp1 in cluster[j]:
					for temp2 in cluster[j]:
						if temp2 not in cluster[i]:
							cluster[i].append(temp2)
							change = change + 1
					cluster[j] = []

# Filtering based on size of pocket
psp_list = []
for k in range(0,len(cluster)):
	if len(cluster[k])>=10:
		for temp in cluster[k]:
			if temp not in psp_list:
				psp_list.append(temp)


# Writing the pocket grid xy coordintates to file
sx = []
sy = []
fo = open("pockets.csv","w")
for temp in psp_list:
	x1 = float(temp[0])
	y1 = float(temp[1])
	sx.append(x1)
	sy.append(y1)
	fo.write("%f,%f,2\n" %(x1,y1))

# Writing the protein grid xy coordintates to file
px = []
py = []
for temp in pxy:
	x1 = float(temp[0])
	y1 = float(temp[1])
	px.append(x1)
	py.append(y1)
	fo.write("%f,%f,1\n" %(x1,y1))
fo.close()

print "The filled protein grid/coordinates along with its pockets has been written into pockets.csv"

# Plotting using R
try:
	os.system("Rscript plot_pockets.r")	
	print "The X,Y coordinates of the filled India map/protein along with its pocket have also been plotted into pockets.pdf"
except:
	pass

# Plotting using matplotlib
try:
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(sx,sy,color="red")
	ax.scatter(px,py,color="grey")
	ax.set_title('Pockets - India')
	plt.show()
except:
	pass
