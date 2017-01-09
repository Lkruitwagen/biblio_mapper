#Collects sample data and trains a nn to classify is ref y/n

from cStringIO import StringIO
import re
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import random
np.set_printoptions(threshold=np.nan)


class config:

	#MAX so far: str_len:50; h1: 55; h2: 14; epsilon: 0.000005; reg_const: 0.005; iter=6000 gives 91%
	str_len=50 #based on histogram
	nn_h1_dim=55
	nn_h2_dim=14 #2 or 4?	
	nn_output_dim=2
	epsilon=0.000005
	reg_const=0.005
	num_passes=6000

	por_train=0.65
	por_cv=1.0-por_train

def make_sampleset(sample_path):
	print 'making sample'
	#print sample_path
	files = [f for f in os.listdir(sample_path) if os.path.isfile(os.path.join(sample_path,f))]
	files = [f for f in files if f[-4:]=='.csv']
	#print files

	sample=[]

	paths = [os.path.join(sample_path,f) for f in files]
	#print paths[:]

	for path in paths:
		with open(path,'rb') as csvfile:
			samplereader = csv.reader(csvfile,dialect='excel')
			for row in samplereader:
				sample.append(row)
		csvfile.close()

	return sample


def sample_prep(sample):
	#return X and y

	print 'prepping sample ...'
	str_len=config.str_len
	#print str_len

	#print [el[1] for el in sample]
	y=np.array([int(el[1]) for el in sample])
	#print y
	strs=[el[0] for el in sample]
	#print strs
	vecs=[]
	for each in strs:
		line=[ord(c) for c in each]
		if len(line)< str_len:
			line=(str_len-len(line))*[0]+line
		else:
			line=line[-config.str_len:]
		vecs.append(line)
	#print vecs
	#print [len(el) for el in vecs]
	X=np.array(vecs)
	#print X

	return X,y

def sample2sets(X,y):

	#return X_train,y_train,X_cv,y_cv
	train_size=int(config.por_train*len(X))
	cv_size=len(X)-train_size
	rand_train=random.sample(xrange(len(X)),train_size)
	X_train=np.array([X[i] for i in sorted(rand_train)])
	y_train=np.array([y[i] for i in sorted(rand_train)])
	rand_cv=[i for i in xrange(len(X)) if i not in rand_train]
	X_cv=np.array([X[i] for i in sorted(rand_cv)])
	y_cv=np.array([y[i] for i in sorted(rand_cv)])
	#print sorted(rand_train)
	#print sorted(rand_cv)
	#print len(rand_train)
	#print len(rand_cv)

	return X_train,y_train,X_cv,y_cv
	#print X_train
	#print y_train


def build_model(nn_h1_dim,nn_h2_dim):
	nn_input_dim=config.str_len
	nn_output_dim=config.nn_output_dim
	np.random.seed(0)
	w1=np.random.randn(nn_input_dim,nn_h1_dim)/np.sqrt(nn_input_dim)
	b1=np.zeros((1,nn_h1_dim))
	w2=np.random.randn(nn_h1_dim,nn_h2_dim)/np.sqrt(nn_h1_dim)
	b2=np.zeros((1,nn_h2_dim))
	w3=np.random.randn(nn_h2_dim,nn_output_dim)/np.sqrt(nn_h2_dim)
	b3=np.zeros((1,nn_output_dim))
	model={}
	model={'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2, 'w3':w3, 'b3': b3}
	#print 'w1=',w1
	#print 'b1=',b1
	#print 'w2=',w2
	#print 'b2=',b2
	#print 'w3=',w3
	#print 'b3=',b3
	return model

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

def cost_function(model,X,y,reg):
	m=len(X)
	w1,b1,w2,b2,w3,b3 = model['w1'],model['b1'],model['w2'],model['b2'],model['w3'],model['b3']
	z1=X.dot(w1)+b1
	a1=np.tanh(z1)
	z2=a1.dot(w2)+b2
	a2=np.tanh(z2)
	z3=a2.dot(w3)+b3
	exps=np.exp(z3)
	P=exps/np.sum(exps,axis=1,keepdims=True)
	probs = P[:,0]
	diff=abs(probs-y)
	correct=-np.log(diff)
	cost=np.sum(correct)
	cost+= reg/2*(np.sum(np.square(w1))+np.sum(np.square(w2))+np.sum(np.square(w3)))
	return 1./m*cost

def train_model(model,X_train,y_train,X_cv,y_cv,reg_lambda,epsilon,num_passes=config.num_passes,print_loss=False):

    m=len(X_train)
    w1,b1,w2,b2,w3,b3 = model['w1'],model['b1'],model['w2'],model['b2'],model['w3'],model['b3']
    print num_passes
    #print range(num_passes)
    for i in range(num_passes):
    #forward prop
    	z1=X_train.dot(w1)+b1
    	a1=np.tanh(z1)
    	z2=a1.dot(w2)+b2
    	a2=np.tanh(z2)
    	z3=a2.dot(w3)+b3
    	exps=np.exp(z3)
    	probs=exps/np.sum(exps,axis=1,keepdims=True)
    	#print i
    	#print probs

    	#backward prop
    	del4=probs
    	del4[range(m),y_train] -= 1
    	#print del3
    	dw3=(a2.T).dot(del4)
    	db3=np.sum(del4,axis=0,keepdims=True)
    	del3=del4.dot(w3.T)*(1-np.power(a2,2))
  		#print 'dw2=',dw2
  		#print 'db2=',db2
  		#print 'del2=',del2

    	dw2=(a1.T).dot(del3)
    	db2=np.sum(del3,axis=0,keepdims=True)
    	del2=del3.dot(w2.T)*(1-np.power(a1,2))


    	dw1=np.dot(X_train.T,del2)
    	db1=np.sum(del2,axis=0)


    	#regularise
    	dw3+=reg_lambda*w3
    	dw2+=reg_lambda*w2
    	dw1+=reg_lambda*w1  

    	w1+=-epsilon*dw1
    	b1+=-epsilon*db1
    	w2+=-epsilon*dw2
    	b2+=-epsilon*db2
    	w3+=-epsilon*dw3
    	b3+=-epsilon*db3

    	model={'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2, 'w3': w3, 'b3': b3}
    	#print model
    	P=predict(model,X_cv)
    	P_act=np.argmax(P,axis=1)
    
    	corr= 1.0-float(np.sum(abs(P_act-y_cv)))/len(X_cv)
    	#print i
    #print corr
    	if i % 100 ==0:
    		print 'cost, i, /% =', cost_function(model,X_cv,y_cv,reg_lambda),i,corr

    #back prop
    #print 'hello'
    return model

def write_model(model):
	#helloheloo
	w1,b1,w2,b2,w3,b3 = model['w1'],model['b1'],model['w2'],model['b2'],model['w3'],model['b3']
	csv_out(w1,'w1')
	csv_out(b1,'b1')
	csv_out(w2,'w2')
	csv_out(b2,'b2')
	csv_out(w3,'w3')
	csv_out(b3,'b3')

def csv_out(var,name):
	cwd=os.getcwd()
	path=os.path.join(cwd,(name+'.csv'))
	resultfile=open(path,'wb')
	wr=csv.writer(resultfile,dialect='excel')
	out=list(var)
	for row in out:
		wr.writerow(row)
	resultfile.close()

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

    
def main():
	print "hello"
	sample_path=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\sample'
	sample = make_sampleset(sample_path)
	#print sample
	trues = [el for el in sample if el[1]=='1']
	print 'trues=',sum([int(el[1]) for el in trues])
	falses = [el for el in sample if el[1]=='0']

	#see the length of all the true samples
	true_lens = [len(el[0]) for el in trues]
	#print true_lens
	#plt.hist(true_lens)
	#plt.show()

	#convert sample now into crushable feature vector X and thingy y

	X,y = sample_prep(sample)
	print 'y sum=', sum(y)
	X_train,y_train,X_cv,y_cv=sample2sets(X,y)
	model = build_model(config.nn_h1_dim,config.nn_h2_dim)
	#P= predict(model,X)
	#print P
	#C= cost_function(model,X_cv,y_cv,config.reg_const)
	#print C
	model = train_model(model,X_train,y_train,X_cv,y_cv,config.reg_const,config.epsilon)
	P = predict(model,X)
	#print P
	output=np.argmax(P,axis=1)
	#print output
	#print y
	diff= abs(output-y)
	fpos=sum([el for el in (output-y) if el>0])
	print 'fpos=',fpos
	fneg=sum([el for el in (output-y) if el<0])
	print 'fneg=',fneg
	print '% correct = ', 1.0-float(sum(diff))/len(X)
	print len(sample)
	write_model(model)
	
	for i in range(len(X)):
		txt=[chr(el) for el in X[i]]
		txt=''.join(txt)
		P=predict(model,X[i])
		out=np.argmax(P,axis=1)
		#print txt,y[i],out,P


	test_str='Jin, L., Myers, S.C., 2006.'
	P=predict(model,prep(test_str))
	print P

	# path= r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\ref\Q1_Bosco_2016_The-effect-of-cross-listing-on-the-environmental-social-and-governance-performance-of-firms.csv'

	# with open(path,'rb') as csvfile:
	# 		samplereader = csv.reader(csvfile,dialect='excel')
	# 		for row in samplereader:
	# 			vec=prep(row)
	# 			P=predict(model,vec)
	# 			output=np.argmax(P,axis=1)
	# 			print row, output
	# 				#wr.writerow(row,)
	# csvfile.close()





    

	



if __name__ == '__main__':
    main()
