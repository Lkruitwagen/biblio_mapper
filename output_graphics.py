#! /usr/bin/env python
# -*- coding: utf-8 -*-
#use nn to eliminate garbage; build ALL list, build node network

from cStringIO import StringIO
import re
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import random
from ann_train import config
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from build_network import str2entry
from operator import add
np.set_printoptions(threshold=np.nan)


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

def isint(el):
	try:
		int(el)
		return int(el)
	except:
		return el


def build_table(final_path):
	print 'build_table'
	files = [f for f in os.listdir(final_path) if os.path.isfile(os.path.join(final_path,f))]
	files = [f for f in files if f[-4:]=='.csv']
	paths = [os.path.join(final_path,f) for f in files] #all ref csv files

	paths=paths[:]

	master=[['PRIMARY']]

	match_count=0

	for path in paths:
		[dummy, name]=os.path.split(path)
		master[0].append(name)
		prim=master[0]
		#print 'prim=',prim
		print path
		prim_len=len(prim)
		with open(path,'rb') as csvfile:
			samplereader = csv.reader(csvfile,dialect='excel')
			fix_len=len(master)
			for row in samplereader:
				#print 'row= ',row
				#print str2entry(row[0])
				
				flag=False
				for i in range(1,fix_len):
					each=master[i][0]
					#print each
					#print str2entry(each)
					if flag==False:
						if refcmp(str2entry(each),str2entry(row[0])):
							print 'match!', each
							#ind_arr=[el[0] for el in master]
							#ind=ind_arr.index(each)
							master[i].append(1)
							match_count+=1
							flag=True
					#else: master[i].append(0)
				if flag==False:
					app_form=row+[0]*(prim_len-2)+[1]
					#print 'app_form=',app_form
					master.append(app_form)
		for i in range(1,len(master)):
			if len(master[i])<len(prim):
				master[i].append(0)
		csvfile.close()

	links=[el[1:] for el in master[1:]]
	#print links[1]
	#print sum(links[1])
	link_sum=[sum(el)-1 for el in links]
	print 'match_count=', match_count
	#print link_sum


	cwd=os.getcwd()
	name='master.csv'
	resultfile=open(os.path.join(cwd,name),'wb')
	wr=csv.writer(resultfile,dialect='excel')
	for el in master:
		wr.writerow(el,)

	resultfile.close()


	threshold=2

	master_filt=[]
	for i in range(1,len(master)):
		if link_sum[i-1]>=threshold:
			master_filt.append([master[i][0],link_sum[i-1]])
	
	master_filt.sort(key=lambda x: x[1], reverse=True)
	for el in master_filt:
		print el


	return master

	#print prim
	#print len(prim)
	#for el in sorted(master):
		#print 'hai'
		#print el

	#insert preprocess?
	#open each final file
	#each ref check duplicate
	#if yes - add (1)
	#if no - add row and add (1)
	#{PRIM: Q1 skjdf; Q1 sflg; Q2 wkjfgsdf}
	#{ref 1: 1 0 0}
	#{ref 2: 1 0 1}
	#{ref 3: 0 0 1}
	#load each file


def filt_thresh(master):
	threshold=6

	master_filt=[]
	shorthand=[]

	links=[el[1:] for el in master[1:]]
	link_sum=[sum(el)-1 for el in links]

	for i in range(1,len(master)):
		if link_sum[i-1]>=threshold:
			master_filt.append(master[i])
			shorthand.append([master[i][0],link_sum[i-1]])
	
	shorthand.sort(key=lambda x: x[1], reverse=True)
	for el in shorthand:
		print el

	return master_filt

def autcmp(aut1,aut2):
	#compares formatted author [lname,fini]
	
	#if last names match
	if aut1[0]==aut2[0]:
		#print 'a thing'
		#print aut1,aut2
		if (len(aut1)==1)&(len(aut2)==1):
			#print 'match'
			return 1
		#if one has initials and one doesn't
		elif (len(aut1)>1)&(len(aut2)==1):
			return 0
		elif (len(aut2)>1)&(len(aut1)==1):
			return 0
		#if the initials match
		elif aut1[1]==aut2[1]:
			return 1
		#if one is only a first initial and the other is multiple and the first initials are the same
		elif (len(aut1[1])==1)&(len(aut2[1])>1)&(aut1[1][0]==aut2[1][0]):
			return 1
		elif (len(aut2[1])==1)&(len(aut1[1])>1)&(aut1[1][0]==aut2[1][0]):
			return 1
		#if one has two initials and the other more than two and the first and last match
		elif (len(aut1[1])==2)&(len(aut2[1])>2)&(aut1[1][0]==aut2[1][0])&(aut1[1][-1]==aut2[1][-1]):
			return 1
		elif (len(aut2[1])==2)&(len(aut1[1])>2)&(aut1[1][0]==aut2[1][0])&(aut1[1][-1]==aut2[1][-1]):
			return 1
		else:
			return 0
	else:
		return 0


def author_trans(master):
	print "author trans"
	#print master
	master_author=[]
	cits=[el[0] for el in master[1:]]
	#for el in cits: print str2entry(el)
	for each in cits:
		dats=master[cits.index(each)+1]
		try:
			temp=str2entry(each)
		except:
			print 'error:',each
			sys.exit()
		temp=temp[1:]
		for el in temp:
			master_author.append([el]+dats[1:])

	master_author.sort(key=lambda x: x[0][0])

	master_author=master_author

	#for el in master_author: print el

	remove_dups=[]
	dupcount=0

	for i in range(len(master_author)):
		#print 'i,ith el',i,master_author[i]
		flag=False
		for j in range(len(remove_dups)):
			if flag==False:
				if autcmp(master_author[i][0],remove_dups[j][0]):
					a= np.array(master_author[i][1:])
					b= np.array(remove_dups[j][1:])
					#print a, type(a), a.size
					#print b, type(b), b.size
					c=np.add(a,b)
					#print c
					d=c.tolist()
					#print d
					
					temp=[master_author[i][0]]+d
					#print temp
					remove_dups.pop(j)
					remove_dups.insert(j,temp)
					dupcount+=1
					flag=True
		if flag==False:
			remove_dups.append(master_author[i])
	print 'dupcount=',dupcount
	#for el in remove_dups: print el

	summary=[]

	for el in remove_dups:
		summary.append([el[0],sum(el[1:])])

	threshold=10

	summary_filt=[el for el in summary if el[1]>10]
	summary_filt.sort(key=lambda x: x[1])

	for el in summary_filt: print el

	cwd=os.getcwd()
	name='master_author.csv'
	resultfile=open(os.path.join(cwd,name),'wb')
	wr=csv.writer(resultfile,dialect='excel')
	for el in master_author:
		wr.writerow(el,)

	resultfile.close()

	return master_author

	#dupcount=0
	#for i in range(len(master_author)-1):
	#	print 'i, ith el, len(mast_auth)=',i, master_author[i][0], len(master_author)
	#	for j in range(i+1,len(master_author)-1):
	#		print 'i,j,len(master_auth)=',i,j,len(master_author)
	#		if autcmp(master_author[i][0],master_author[j][0]):
	#			#match i,j, add to i, pop j
	#			sumran=[sum(x) for x in zip(master_author[i][1:],master_author[j][1:])]
	#			temp=[master_author[i][0],sumran]
	#			print temp
	#			master_author.insert(i,temp)
	#			master_author.pop(i+1)
	#			master_author.pop(j)
	#			dupcount+=1
	#	print 'dupcount=',dupcount

	#print master_author
	#for el in master_author: print el
	#a= master_author[500][0]
	#b= master_author[501][0]
	#print autcmp(a,b)
	
def rgb2hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def output(subset_out,subset_stats,queries):
	path_out=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Pipeline'
	name='graph.json'
	path=os.path.join(path_out,name)
	#print path
	f=open(path,'w')
	#f.write(r'this is a test\n') do not use literal string r
	#f.write('this is another test\n')
	#f.write('i predict a riot')

	#temp=10
	prim=subset_out[0]
	#prim_out=['_'.join(el.split('_')[0:3]) for el in prim]
	prim_out=prim[1:] #temp primout cap

	cols=[]
	#print queries
	for el in prim_out:
		ind=[i[0] for i in queries].index(el)
		r=int(float(queries[ind][1])*255)
		g=int(float(queries[ind][2])*255)
		b=int(float(queries[ind][3])*255)
		cols.append(rgb2hex(r,g,b))

	#print cols

	sec=[el[0] for el in subset_out]
	sec_out=sec[1:]
	#test=prim[3]
	
	for el in sec_out:
		ind=[i[0] for i in subset_out].index(el)
		print el, subset_out[ind][0]



	links=[el[1:] for el in subset_out[1:]]
	#for el in prim_out: print el
	#for el in sec_out: print el
	print 'prim out'
	print prim_out
	print 'sec out'
	print sec_out

	print 'links'
	print links

	all_nodes=prim_out+sec_out
	#for el in all_nodes: print el


	f.write('{\n')
	f.write('  "nodes":[\n')
	#ALL DA NODES
	for i in range(len(all_nodes)-1):
		if i<len(prim_out):
			f.write('\t\t{"name":"'+all_nodes[i]+'","group":2,"color":'+'"'+cols[i]+'"'+'},\n')
		else:
			f.write('\t\t{"name":"'+all_nodes[i]+'","group":1,"color":'+'"#FF00FF"'+'},\n')

	f.write('\t\t{"name":"'+all_nodes[(len(all_nodes)-1)]+'","group":1,"color":'+'"#FF00FF"'+'}\n')
	#f.write('\t\t{"name":"node1","group":1},\n')
	#f.write('\t\t{"name":"node2","group":2},\n')
	#f.write('\t\t{"name":"node3","group":2},\n')
	#f.write('\t\t{"name":"node3","group":4},\n')
	#f.write('\t\t{"name":"node4","group":3}\n')

	f.write('\t],\n')


	f.write('\t"links":[\n')
	#all da links

	#for each primary, draw links to secondary
	for i in range(len(prim_out)):
		link_prim=[el[i] for el in links]
		#print link_prim
		for j in range(len(link_prim)):
			if link_prim[j]>0:
				f.write('\t\t{"source":'+str(i)+',"target":'+str((j+len(prim_out)))+',"weight":'+str(link_prim[j])+'},\n')

	f.write('\t\t{"source":0,"target":0,"weight":0}\n')

	f.write('\t]\n')
	f.write('}')


	f.close()


def q_filter(master,queries):
	print 'q_filter'
	print master[0]
	labels=[el.split('_')[0] for el in master[0][1:]]
	print labels
	label_set=sorted(list(set(labels)))
	print label_set
	labels=['PRIMARY']+labels
	print labels

	

	master_compact=[['PRIMARY']+label_set]
	for each in master[1:]:
		new_row=[each[0]]
		#print each
		for el in label_set:
			#print el
			#print [each[i] for i in range(1,len(each)) if (labels[i]==el)]
			#print sum([each[i] for i in range(1,len(each)) if (labels[i]==el)])
			#print len([each[i] for i in range(1,len(each)) if (labels[i]==el)])
			new_row.append(sum([each[i] for i in range(1,len(each)) if (labels[i]==el)]))
			#wait = raw_input("PRESS ENTER TO CONTINUE.")
		#print new_row
		master_compact.append(new_row)
		#print master_compact
		#wait = raw_input("PRESS ENTER TO CONTINUE.")
	wait = raw_input("PRESS ENTER TO CONTINUE.")
	#for el in master_compact: print el
	N_Q=[]
	for i in range(len(label_set)):
		N_Q.append(sum([el[i+1] for el in master_compact[1:]]))
	N_tot=sum(N_Q)
	#print 'N_tot',N_tot
	N_Q_per=[]
	for N in N_Q:
		#print float(N)/N_tot
		N_Q_per.append(float(N)/N_tot)

	r=0.0
	g=0.0
	b=0.0
	#print [q[0] for q in queries]
	for i in range(len(label_set)):
		ind = [q[0] for q in queries].index(label_set[i])

		r+=float(queries[ind][1])*N_Q_per[i]
		g+=float(queries[ind][2])*N_Q_per[i]
		b+=float(queries[ind][3])*N_Q_per[i]

	#print 'r,g,b=', r,g,b
	H_RGB_per=[r,g,b]

	#print 'N_Q=',N_Q
	#print 'N_Per=',N_Q_per
	#print master_compact[500]
	#print stats(master_compact[500],queries,label_set,N_Q_per,H_RGB_per)
	full_stats=[]
	for each in master_compact[1:]:
		full_stats.append(stats(each,queries,label_set,N_Q_per,H_RGB_per))

	for el in full_stats:
		if el[1]>10:
			print el


	subset=[]
	#for top 15 for each R,G,B
	print 'top 15'
	
	selection=full_stats
	selection.sort(key=lambda x: x[5], reverse=True)
	for j in selection[0:17]:
		subset.append(j)
	selection.sort(key=lambda x: x[6], reverse=True)
	for j in selection[0:17]:
		subset.append(j)
	selection.sort(key=lambda x: x[7], reverse=True)
	for j in selection[0:17]:
		subset.append(j)
	subset_out=[master_compact[i] for i in range(1,len(master_compact)) if master_compact[i][0] in [el[0] for el in subset]]
	for el in subset_out: print el
	subset_out.insert(0,master_compact[0])

	subset.insert(0,['stat','sum','max','Qx','H_Q','R','G','B','H_RGB'])

	return subset_out, subset


def less_flr(a,b):
	#returns less of flr(a/b) or a/b
	if ((a/b)>1):
		return 1
	else:
		return a/b

def stats(row,queries,label_set,N_Q_per,H_RGB_per):
	#print 'stats'
	#return sum, max, 'QX', H_Q, R, G, B, H_RGB
	stat=[row[0]]
	#sum
	stat.append(sum(row[1:]))
	stat.append(max(row[1:]))
	stat.append(label_set[row.index(max(row[1:]))-1])

	H_per=[float(el)/sum(row[1:]) for el in row[1:]]
	
	H_Q=sum([(less_flr(H_per[i],N_Q_per[i])) for i in range(len(H_per))])/len(H_per)
	#print H_Q
	stat.append(H_Q)

	R=0.0
	G=0.0
	B=0.0
	#print [q[0] for q in queries]
	for i in range(len(label_set)):
		ind = [q[0] for q in queries].index(label_set[i])

		R+=float(queries[ind][1])*row[i+1]
		G+=float(queries[ind][2])*row[i+1]
		B+=float(queries[ind][3])*row[i+1]

	#print R,G,B
	stat.append(R)
	stat.append(G)
	stat.append(B)

	RGB=[R,G,B]
	RGB_per=[el/sum(RGB) for el in RGB]
	#print RGB_per
	#print H_RGB_per
	#print [(less_flr(RGB_per[i],H_RGB_per[i])) for i in range(3)]


	H_RGB=sum([(less_flr(RGB_per[i],H_RGB_per[i])) for i in range(3)])/3
	stat.append(H_RGB)

	return stat

def csv_out(var,fname):
	print 'writing csv', fname
	cwd=os.getcwd()
	name=fname
	resultfile=open(os.path.join(cwd,name),'wb')
	wr=csv.writer(resultfile,dialect='excel')
	for el in var:
		wr.writerow(el,)

	resultfile.close()

def main():
	print 'output graphics'
	master= csv_in('master_author_working.csv')

	queries=csv_in('queries.csv')

	subset_out, subset_stats=q_filter(master,queries)
	print subset_out
	print subset_stats

	csv_out(subset_out,'out_dat.csv')
	csv_out(subset_stats,'out_stats.csv')
	
	wait = raw_input("PRESS ENTER TO CONTINUE.")
	
	output(subset_out,subset_stats,queries)

	wait = raw_input("PRESS ENTER TO CONTINUE.")

	master_filt=filt_thresh(master)
	print 'master filt'
	for el in master_filt:
		print el

	master_filt.insert(0,master[0])

	#master_author=author_trans(master)
	master_author=csv_in('master_author_working.csv')
	#for el in master_author: print el
	master_author.insert(0,master[0])

	
	print queries
	
	#output(master_filt)

	#print link_sum
	#print link_sum


if __name__ == '__main__':
    main()