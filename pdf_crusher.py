#crushed pdfs in current directory into textfiles at the path given in hard_path

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
    print 'match!'
    print match.group()
    print match.end()
    return match.end()
  else:
    print 'not found'
    return -1


def pdf2txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    hard_path=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\txt'


    [dummy,name]=os.path.split(path)
    print name
    name_txt=name[:-4]+'.txt'
    print name_txt
    path = os.path.join(os.path.normpath(hard_path),name_txt)
    print path
    text_file = open(os.path.normpath(path),'w')
    text_file.write(text)
    text_file.close()

    return text
    

def main():

    hard_path=r'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\txt'
    #get dir of filenames
    cwd = os.getcwd()
    files= [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd,f))]
    #print cwd
    #print files

    #sort for those that are .pdf
    files = [f for f in files if f[-4:]=='.pdf']
    #print files
    names = [f[:-4] for f in files]
    print names
    paths = [os.path.join(cwd,f) for f in files]
    print paths
    
    path = 'C:\Users\Lucas\Dropbox\DPhil\ToS_Lit_Review\Articles\Q1\Q1_Auer_2016_Do-socially-ir-responsible-investments-pay-New-evidence-from-international-ESG-data.pdf'


    for path in paths:
      pdf2txt(path)
    #sort for those only with .pdf
    #extract metadata



    
    
    #text = pdf2txt(path)

    #return text

if __name__ == '__main__':
    main()
