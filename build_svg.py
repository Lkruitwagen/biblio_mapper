from cStringIO import StringIO
import re
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import random
import math

np.set_printoptions(threshold=np.nan)

def isint(el):
	try:
		int(el)
		return int(el)
	except:
		return el

def csv_in(name):

	#hihi
	cwd=os.getcwd()
	var=[]
	path=os.path.join(cwd,name)
	resultfile=open(path,'r')
	wr=csv.reader(resultfile,dialect='excel')
	for row in wr:
		var.append([isint(el) for el in row])
	resultfile.close()
	return var

def rgb2hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def cost(centers_data,order,centers,big_centers):
	#sum of all link distances with log weightings

	links=[] 
	#R,G,B
	for el in centers_data:
		links.append([math.log10(float(el[5])+1),math.log10(float(el[6])+1),math.log10(float(el[7])+1)])
	
	print 'order',order
	for el in links: print el
	#G,B,R
	distances=[]
	for el in centers:
		distances.append([math.sqrt((el[0]-big_centers[0][0])**2+(el[1]-big_centers[0][1])**2),math.sqrt((el[0]-big_centers[1][0])**2+(el[1]-big_centers[1][1])**2),math.sqrt((el[0]-big_centers[2][0])**2+(el[1]-big_centers[2][1])**2)])

	print distances
	distances=np.array(distances)
	links = np.array(links)
	subcost=[]
	print distances
	wait = raw_input("PRESS ENTER TO CONTINUE.")
	#GBR
	for i in range(len(centers_data)):
		sublink=links[order[i]] #index for link
		#print sublink

		subcost.append([distances[i][0]*sublink[1],distances[i][1]*sublink[2],distances[i][2]*sublink[0]])
		print subcost
		#wait = raw_input("PRESS ENTER TO CONTINUE.")
	#print subcost
	print np.sum(subcost)
	return np.sum(subcost)


def write_svg(subset_out,subset_stats):
	print 'writing svg'
	path_out=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Pipeline'
	name='output.html'
	path=os.path.join(path_out,name)
	#print path
	f=open(path,'w')
	f.write('<svg width="1500" height="1000" version=1.0" xmlns="http://www.w3.org/2000/svg">\n')
	#f.write('<rect width="200" height="100" fill="#BBC42A" />\n')

	C=[750,500]
	big_centers=[]
	rad1=100
	angles=[-90,30,150]
	cols=['#00FF00','#0000FF','#FF0000']
	rad2=200
	for i in range(3):
		big_centers.append([C[0]+rad1*math.cos(math.radians(angles[i])),C[1]+rad1*math.sin(math.radians(angles[i])),cols[i]])

	theta1=math.radians(math.degrees(math.asin(float(rad1)/rad2*math.sin(math.radians(60))))+30)

	int1=[big_centers[1][0]+rad2*math.cos(theta1),big_centers[1][1]-rad2*math.sin(theta1)]
	D=math.sqrt((int1[0]-C[0])**2+(int1[1]-C[1])**2)
	print 'int1',int1
	print D
	int2=[C[0],C[1]+D]
	int3=[C[0]-(int1[0]-C[0]),int1[1]]


	print big_centers[1]
	print int1
	diff=[int1[0]-big_centers[1][0],int1[1]-big_centers[1][1]]
	print diff
	x_diff=int1[0]-big_centers[1][0]
	y_diff=int1[1]-big_centers[1][1]
	print math.degrees(math.acos(x_diff/rad2))
	print math.degrees(math.asin(y_diff/rad2))

	angle1=math.degrees(math.atan((float(diff[1])/diff[0])))
	angle2=math.degrees(math.acos((int2[0]-big_centers[1][0])/rad2))
	print 'angle',angle1, angle2
	point=[big_centers[1][0]+rad2*math.cos(math.radians(angle1)),big_centers[1][1]+rad2*math.sin(math.radians(angle1))]
	point2=[big_centers[1][0]+rad2*math.cos(math.radians(angle2)),big_centers[1][1]+rad2*math.sin(math.radians(angle2))]
	rads_arc=math.radians(angle2)-math.radians(angle1)
	print rads_arc

	x_diff=(int2[0]-big_centers[2][0])
	print x_diff
	print math.degrees(math.acos(x_diff/rad2))
	angle3= math.degrees(math.acos(x_diff/rad2))
	point3=[big_centers[2][0]+rad2*math.cos(math.radians(angle3)),big_centers[2][1]+rad2*math.sin(math.radians(angle3))]
	#arc=rads_arc*rad2/15
	#print arc
	print 'int3',int3
	print big_centers[0]
	print int3[1]-big_centers[0][1]
	angle4=-1*math.degrees(math.acos((int3[0]-big_centers[0][0])/(rad2)))
	point4=[big_centers[0][0]+rad2*math.cos(math.radians(angle4)),big_centers[0][1]+rad2*math.sin(math.radians(angle4))]
	print angle4

	#angle1, angle3, angle4

	rads_diff=rads_arc/15

	centers=[]
	for i in range(15):
		angle=math.radians(angle1)+rads_diff*i
		centers.append([big_centers[1][0]+rad2*math.cos(angle),big_centers[1][1]+rad2*math.sin(angle)])
	for i in range(15):
		angle=math.radians(angle3)+rads_diff*i
		centers.append([big_centers[2][0]+rad2*math.cos(angle),big_centers[2][1]+rad2*math.sin(angle)])
	for i in range(15):
		angle=math.radians(angle4)+rads_diff*i
		centers.append([big_centers[0][0]+rad2*math.cos(angle),big_centers[0][1]+rad2*math.sin(angle)])

	#for el in subset_stats: print el

	centers_data=subset_stats[1:]
	#order= range(len(subset_stats)-1)
	#cost_old=0.0
	#cost_new = cost(centers_data,order,centers,big_centers)
	#print cost_new
	#print type(cost_new)
	#print cost_new-cost_old
	#now adjust centers_data[-1]

	#bubble cost - i.e. if it makes things better, swap
	
	links=[] 
	#R,G,B
	for el in centers_data:
		#links.append([math.log10(float(el[5])+1),math.log10(float(el[6])+1),math.log10(float(el[7])+1)])
		links.append([round(math.log((float(el[7])+1),2)),round(math.log((float(el[5])+1),2)),round(math.log((float(el[6])+1),2))])

	print links
	#links: RGB/567->BRG

	#order,circles: BRG

	#large ones: GBR
	print big_centers

	for i in range(len(links)):
		f.write('<line x1="'+str(big_centers[0][0])+'" y1="'+str(big_centers[0][1])+'" x2="'+str(centers[i][0])+'" y2="'+str(centers[i][1])+'" stroke="#DDDDDD" stroke-width="'+str(int(links[i][2]))+'"/>\n')
		f.write('<line x1="'+str(big_centers[1][0])+'" y1="'+str(big_centers[1][1])+'" x2="'+str(centers[i][0])+'" y2="'+str(centers[i][1])+'" stroke="#DDDDDD" stroke-width="'+str(int(links[i][0]))+'"/>\n')
		f.write('<line x1="'+str(big_centers[2][0])+'" y1="'+str(big_centers[2][1])+'" x2="'+str(centers[i][0])+'" y2="'+str(centers[i][1])+'" stroke="#DDDDDD" stroke-width="'+str(int(links[i][1]))+'"/>\n')










	cols=[]

	for i in range(len(centers)):
		R=links[i][1]
		G=links[i][2]
		B=links[i][0]
		col_max=max([R,G,B])
		R=int(R/col_max*255)
		G=int(G/col_max*255)
		B=int(B/col_max*255)
		cols.append(rgb2hex(R,G,B))

	print cols




	print big_centers
	#for el in big_centers:
		#f.write('<circle cx="'+str(el[0])+'" cy="'+str(el[1])+'" r="200" stroke="#DDDDDD" stroke-width="4" fill="#FFFFFF" />\n')

	for el in big_centers:
		f.write('<circle cx="'+str(el[0])+'" cy="'+str(el[1])+'" r="75" stroke="#DDDDDD" stroke-width="4" fill='+el[2]+' />\n')
	f.write('<circle cx="'+str(int1[0])+'" cy="'+str(int1[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#FFFFFF" />\n')
	f.write('<circle cx="'+str(int2[0])+'" cy="'+str(int2[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#FFFFFF" />\n')
	f.write('<circle cx="'+str(int3[0])+'" cy="'+str(int3[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#FFFFFF" />\n')
	f.write('<circle cx="'+str(point[0])+'" cy="'+str(point[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#00FFFF" />\n')
	f.write('<circle cx="'+str(point2[0])+'" cy="'+str(point2[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#00FFFF" />\n')
	f.write('<circle cx="'+str(point3[0])+'" cy="'+str(point3[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#FF0000" />\n')
	f.write('<circle cx="'+str(point4[0])+'" cy="'+str(point4[1])+'" r="4" stroke="#DDDDDD" stroke-width="4" fill="#00FF00" />\n')

	for i in range(len(centers)):
		f.write('<circle cx="'+str(centers[i][0])+'" cy="'+str(centers[i][1])+'" r="10" stroke="#DDDDDD" stroke-width="2" fill="'+cols[i]+'" />\n')
		if i==12:
			f.write('<text x="'+str(centers[i][0]+15)+'" y="'+str(centers[i][1]+15)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==13:
			f.write('<text x="'+str(centers[i][0]+5)+'" y="'+str(centers[i][1]+30)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==14:
			f.write('<text x="'+str(centers[i][0]-60)+'" y="'+str(centers[i][1]+30)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==15:
			f.write('<text x="'+str(centers[i][0])+'" y="'+str(centers[i][1]+65)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==16:
			f.write('<text x="'+str(centers[i][0]-5)+'" y="'+str(centers[i][1]+35)+'" font-family="sans-serif" font-size="14px" fill="#333333" text-anchor="end" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==17:
			f.write('<text x="'+str(centers[i][0]-5)+'" y="'+str(centers[i][1]+45)+'" font-family="sans-serif" font-size="14px" fill="#333333" text-anchor="end" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==18:
			f.write('<text x="'+str(centers[i][0]-15)+'" y="'+str(centers[i][1]+15)+'" font-family="sans-serif" font-size="14px" fill="#333333" text-anchor="end" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==37:
			f.write('<text x="'+str(centers[i][0]-15)+'" y="'+str(centers[i][1]-10)+'" font-family="sans-serif" font-size="14px" text-anchor="end" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==38:
			f.write('<text x="'+str(centers[i][0])+'" y="'+str(centers[i][1]-10)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i==39:
			f.write('<text x="'+str(centers[i][0]+15)+'" y="'+str(centers[i][1])+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i<16:
			f.write('<text x="'+str(centers[i][0]+15)+'" y="'+str(centers[i][1]+5)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		elif i<37:
			f.write('<text x="'+str(centers[i][0]-15)+'" y="'+str(centers[i][1]+5)+'" font-family="sans-serif" font-size="14px" fill="#333333" text-anchor="end" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
		else:
			f.write('<text x="'+str(centers[i][0]+15)+'" y="'+str(centers[i][1]+5)+'" font-family="sans-serif" font-size="14px" fill="#333333" transform="rotate(0,500,500)">'+centers_data[i][0]+'</text>\n')
	f.write('</svg>\n')

	f.close()


def main():
	print 'build svg'
	subset_out = csv_in('out_dat.csv')
	subset_stats = csv_in('out_stats.csv')
	#for el in subset_out: print el
	#for el in subset_stats: print el
	write_svg(subset_out,subset_stats)


if __name__ == '__main__':
    main()