#!/usr/bin/env python
#coding:utf-8

import os,sys

sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from Dependcy import *
from urllib2 import urlopen
from optparse import OptionParser

usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--ID", action="store",
                  dest="ID",

                  help="GBK_ID")
parser.add_option("-o", "--Output", action="store",
                  dest="output",

                  help="OutputPath")
if __name__ == '__main__':
	(options, args) = parser.parse_args()
	ID = options.ID
	OUTPUT = options.output
	Get_Path(OUTPUT)
	base_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide"
	fasta_url = base_url+"&id=%s&rettype=fasta&retmode=text"%(ID)
	gbk_url = base_url+ "&id=%s&rettype=gbwithparts&retmode=text"%(ID)
	
	if not os.path.exists(OUTPUT+'/'+ID+'.fasta'):
		fasta_record = urlopen(fasta_url).read()
		FASTA = open(OUTPUT+'/'+ID+'.fasta','w')
		FASTA.write(fasta_record)
		FASTA.close()
		
	if not os.path.exists(OUTPUT+'/'+ID+'.gbk'):
		GBK = open(OUTPUT+'/'+ID+'.gbk','w')
		gbk_record = urlopen(gbk_url).read()
		GBK.write(gbk_record)
	
		GBK.close()
