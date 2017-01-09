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
np.set_printoptions(threshold=np.nan)

def Find(pat, text):
  match = re.search(pat,text)
  if match:
    #print 'match!'
    #print match.group()
    #print match.end()
    #print text[0:match.end()]
    return match.start(), match.group(0)
  else:
    #print 'not found'
    #hi
    return -1

def collect_model():
	#hihi
	w1=csv_in('w1.csv')
	b1=csv_in('b1.csv')
	w2=csv_in('w2.csv')
	b2=csv_in('b2.csv')
	w3=csv_in('w3.csv')
	b3=csv_in('b3.csv')
	model={}
	model={'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2, 'w3':w3, 'b3': b3}
	return model

def csv_in(name):
	#hihi
	cwd=os.getcwd()
	var=[]
	path=os.path.join(cwd,name)
	resultfile=open(path,'r')
	wr=csv.reader(resultfile,dialect='excel')
	for row in wr:
		var.append([float(el) for el in row])
	resultfile.close()
	return np.array(var)

def predict(model,X):
	w1,b1,w2,b2,w3,b3 = model['w1'],model['b1'],model['w2'],model['b2'],model['w3'],model['b3']
	z1=X.dot(w1)+b1
	a1=np.tanh(z1)
	z2=a1.dot(w2)+b2
	a2=np.tanh(z2)
	z3=a2.dot(w3)+b3
	exps=np.exp(z3)
	P=exps/np.sum(exps,axis=1,keepdims=True)
	#np.argmax(P,axis=1)
	return P

def process_refs(ref_path,final_path,model):
	files = [f for f in os.listdir(ref_path) if os.path.isfile(os.path.join(ref_path,f))]
	files = [f for f in files if f[-4:]=='.csv']
	paths = [os.path.join(ref_path,f) for f in files] #all ref csv files
	
	lines=[]

	for path in paths:
		[dummy, name] = os.path.split(path)
		print name


		final_name=os.path.join(final_path,name)
		resultfile=open(final_name,'wb')
		wr=csv.writer(resultfile,dialect='excel')


		with open(path,'rb') as csvfile:
			samplereader = csv.reader(csvfile,dialect='excel')
			for row in samplereader:
				#lines.append(row)
				#print row
				vec=prep(row[0])
				P=predict(model,vec)
				output=np.argmax(P,axis=1)
				txt=[chr(el) for el in vec]
				txt=''.join(txt)
				#print txt,output[0],P
				#print output[0]
				if output[0]>0:
					#print 'writing'
					lines.append(row)
					wr.writerow(row,)
		csvfile.close()
		resultfile.close()

	return lines



		#print lines

    	#print results
    	#ref_name=os.path.join(ref_path,(name[:-4]+'.csv'))
    	#print ref_name
    	#resultFile=open(ref_name,'wb')
    	#wr=csv.writer(resultFile,dialect='excel')
    	#for row in results:
        #	wr.writerow([row,])
    	#resultFile.close()

		#rewrite files with sanitised refs
		#AND add to an ALL REFS file

def prep(row):
	#jksdf
	#print config.str_len
	
	vec=[ord(c) for c in str(row)]
	if len(vec)<config.str_len:
		vec=(config.str_len-len(vec))*[0]+vec
	else:
		vec=vec[-config.str_len:]

	#print vec
	return np.array(vec)

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
						try:
							if refcmp(str2entry(each),str2entry(row[0])):
								print 'match!', each
								#ind_arr=[el[0] for el in master]
								#ind=ind_arr.index(each)
								master[i].append(1)
								match_count+=1
								flag=True
						except:
							print 'error', each,row[0]
							pass
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

def refcmp(ref1,ref2):
	#print 'refcmp'
	threshold=80
	#print ref1[0]
	#print ref2[0]
	cond1= (int(ref1[0])==int(ref2[0]))
	#print 'cond1=',ref1[0],ref2[0]
	if cond1:
		ref1.pop(0)
		ref2.pop(0)

		cond2=(len(ref1)==len(ref2))
		#print len(ref1)
		#print len(ref2)
		#print 'cond2=', len(ref1), len(ref2), ref1,ref2
		if cond2:
			lname1=[el[0] for el in ref1]
			lname2=[el[0] for el in ref2]
			lthresh=[]
			#print lname1
			#print lname2
			for i in range(len(lname1)):
				lthresh.append(fuzz.ratio(lname1[i],lname2[i]))
				#print lname1[i].encode('utf16'), lname2[i].encode('utf16'), lthresh
			cond3=all(el>threshold for el in lthresh)
			#print 'cond3', lthresh, ref1,ref2
			if cond3:
				#need to accomodate no-initial refs
				ini1=[]
				ini2=[]
				for i in range(len(ref1)):
					try:
						ini1.append(ref1[i][1])
					except:
						ini1.append('')
					try:
						ini2.append(ref2[i][1])
					except:
						ini2.append('')
				ithresh=[]
				#print ini1
				#print ini2
				for i in range(len(ini1)):
					#if they match

					#print len(ini1[i])
					#print len(ini2[i])

					if ini1[i]==ini2[i]:
						ithresh.append(True)
					#if one has an initial and the other doesn't, False
					elif (len(ini1[i])>0)&(len(ini2[i])==0):
						ithresh.append(False)
					elif (len(ini2[i])>0)&(len(ini1[i])==0):
						ithresh.append(False)
					#if one is only a first initial and the other is multiple and the first initials are the same
					elif (len(ini1[i])==1)&(len(ini2[i])>1)&(ini1[i][0]==ini2[i][0]):
						ithresh.append(True)
					elif (len(ini2[i])==1)&(len(ini1[i])>1)&(ini1[i][0]==ini2[i][0]):
						ithresh.append(True)
					#if one has two initials and the other has more than two and the first and last match
					elif (len(ini1[i])==2)&(len(ini2[i])>2)&(ini1[i][0]==ini2[i][0])&(ini1[i][-1]==ini2[i][-1]):
						ithresh.append(True)
					elif (len(ini2[i])==2)&(len(ini1[i])>2)&(ini1[i][0]==ini2[i][0])&(ini1[i][-1]==ini2[i][-1]):
						ithresh.append(True)
					#else false
					else:
						ithresh.append(False)

				#print 'cond4=',ithresh, ref2
				cond4=all(el for el in ithresh)
				#print cond4
				if cond4:
					return 1
				else:
					#print 'no match'
					return 0
			else: 
				#print 'no match'
				return 0
		else:
			#print 'no match'
			return 0
	else:
		#print 'no match'
		return 0


def str2entry(row_str):
	form=r'\d\d\d\d.?.?.?'
	i_year,ret_str=Find(form,row_str)
	year=row_str[i_year:i_year+4]
	#print year
	#pop year+ up to 3 wild
	row_str=row_str.replace(ret_str,'')
	#pop open brackets
	row_str=row_str.replace('(','')
	#pop 'and', '&'
	#row_str=row_str.replace('and','')
	#row_str=row_str.replace('&','')
	#remove any leading/trailing spaces
	row_str=row_str.strip()
	#remove any trailing commas
	#print row_str[-1]
	if row_str.endswith(','): row_str=row_str[:-1]
	#split by commas
	row_list=re.split(' and | & |,|\.',row_str)
	row_list=[el.strip() for el in row_list]
	row_list=[el for el in row_list if el]
	entry =[]
	entry.append(year)
	cool=False
	#print row_list
	for i in range(len(row_list)):
		if len(row_list[i])>1:
			cool=False
			entry.append([row_list[i]])
		elif (cool==False):
			try:
				entry[-1].append(row_list[i])
				cool=True
			except:
				pass
		else:
			try:
				entry[-1][-1]=entry[-1][-1]+row_list[i]
			except:
				pass
	return entry



def main():
	print 'hello world'
	model = collect_model()

	ref_path=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\ref'
	final_path=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\final'
	all_sec_refs=process_refs(ref_path,final_path,model) #contains multiples (i.e. which is good)
	#print model
	sort_refs=sorted(all_sec_refs)
	#print sort_refs
	test_refs=sort_refs[0:5]
	#print 'test_refs',test_refs

	trace_mult=[[u'dummy, A 9999.',0]]

	for row in test_refs:
		#print 'row=',row
		fix_len=len(trace_mult)
		#print 'fix_len=',fix_len
		flag=False
		for i in range(fix_len):
			each=trace_mult[i]
			
			#print 'each=',each
			#each_ent=str2entry(each[0])
			#print str2entry(each[0])
			#print str2entry(row[0])
			#print row[0]
			#print 'refcmp=',refcmp(str2entry(each[0]),str2entry(row[0]))
			if flag==False:
				if (refcmp(str2entry(each[0]),str2entry(row[0]))):
					print each,'y'
					ind=trace_mult.index(each)
					#print trace_mult
					#print 'ind',ind
					[ref,count]=trace_mult[ind]
					count+=1
					trace_mult[ind]=[ref,count]
					flag=True
		if flag==False:
			#print each,'n'
			trace_mult.append([row[0],0])
		#print 'trace_mult:'

	demo=[el for el in trace_mult if el[1]>0]
	for row in demo:
		print row

	master = build_table(final_path)

	#print all_sec_refs[:]

	cwd=os.getcwd()
	name='all_refs.csv'
	path=os.path.join(cwd,name)
	resultfile=open(path,'wb')
	wr=csv.writer(resultfile,dialect='excel')
	for row in all_sec_refs:
		wr.writerow(row)
	resultfile.close()

	

	for row in all_sec_refs:
		row_str=row[0]
		#print row_str
		#print str2entry(row_str)
		#find year form
		


		#r'\(\d\d\d\d.?.?\)'
	test_str='Jin, L., Myers, S.C., 2006.'
	P=predict(model,prep(test_str))
	#print P


	#str1=u'Bilbao-Terol,  A.,  Arenas-Parra,  M.,   CaËœnal-FernÃ¡ndez,  V.,  Bilbao-Terol,  C.,  2013.'

	test_set=[
	[u'Bilbao-Terol,  A.,  Arenas-Parra,  M.,   CaËœnal-FernÃ¡ndez,  V.,  Bilbao-Terol,  C.,  2013.',u'Bilbao-Terol, A., Arenas-Parra, M., CaÃ±al-FernÃ¡ndez, V., & Bilbao-Terol, C. (2013)'],
	[u'Borgers, A., Derwall, J., Koedijk, K., Ter Horst, J., 2013.',u'Borgers, A., Derwall, J., Koedijk, K., Ter Horst, J.R., 2013.'],
	[u'Bouslah, K., Kryzanowski, L., Bouchra, M., 2013.',u'Bouslah, K., Kryzanowski, L., M"Zali, B., 2013.'],
	[u'Bowen, H.R., 1953.',u'Bowen, H. 1953.']
	]

	#print test_set[0][0].encode('utf8')
	#print str2entry(test_set[0][0])
	#print test_set[0][1].encode('utf8')
	#print str2entry(test_set[0][0])
	#print refcmp(str2entry(test_set[0][0]),str2entry(test_set[0][1]))
	#print refcmp(str2entry(test_set[1][0]),str2entry(test_set[1][1]))
	#print refcmp(str2entry(test_set[2][0]),str2entry(test_set[2][1]))
	#print refcmp(str2entry(test_set[3][0]),str2entry(test_set[3][1]))




if __name__ == '__main__':
    main()