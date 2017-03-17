#scrapes text files for reference schapes of the forms given

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import csv
import os

def Find(pat, text):
  match = re.search(pat,text)
  if match:
    #print 'match!'
    #print match.group()
    #print match.end()
    #print text[0:match.end()]
    return match.end()
  else:
    #print 'not found'
    #hi
    return -1

def scrape_refs(path):
    results=[]

    #generate results


        
    form_MLA_APA_chic = r'\(\d\d\d\d.?.?\)'
    form_van_harv = r'\d\d\d\d\.'

    forms = [form_MLA_APA_chic,form_van_harv]
        
    f = open(path,'r')
    text=f.read()
    #print text
    lines=text.split('\n')

    result_vec=[path]

    for form in forms:
        res_count=0
        for line in lines:
            linf= Find(form,line)
                #define better shapes - choose best
            if linf>0:
                res_count+=1
                results.append(line[0:linf])
                #print line[0:linf]
                #print results
                # adds results from all forms

        result_vec.append(res_count)
        #print form
        #print len(results)
        #print results

        #exception: Manuscript accepted
        #clean up results
        #split up: [str, date, Author 1, Author 2, ..., Author N];
        #author format: 'lastname, I.I.'
    
    f.close()
    return results, result_vec

    #ipsum

def ref2csv(path,results,ref_path):
    #iiipyyy
    [dummy, name] = os.path.split(path)
    #print results
    ref_name=os.path.join(ref_path,(name[:-4]+'.csv'))
    #print ref_name
    resultFile=open(ref_name,'wb')
    wr=csv.writer(resultFile,dialect='excel')
    for row in results:
        wr.writerow([row,])
    resultFile.close()


   

def main():

    #pipeline:
    #get all txt files
    #one at a time, get refs using ref formats
    #clean ref formats - supervised learning 
    #match refs

    #get all txt files
    cwd = os.getcwd()
    txt_path=cwd
    ref_path=cwd
    files = [f for f in os.listdir(txt_path) if os.path.isfile(os.path.join(txt_path,f))]
    files = [f for f in files if f[-4:]=='.txt']
    
    paths = [os.path.join(txt_path,f) for f in files]

    results_all=[]
 
    print paths


    #set one demo path
    #path = paths[0]
    #for path in paths:
    #print 'path =',path

    #path = paths[0]

    for path in paths:

        #scrape refs
        results, result_vec = scrape_refs(path)
        #print results
        #write CSV
        ref2csv(path,results,ref_path)
        results_all.append(result_vec)

    for elem in results_all:
        print elem


    
    
    
    

if __name__ == '__main__':
    main()
