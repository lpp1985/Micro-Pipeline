#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/3
"""
import os,sys

sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from optparse import OptionParser

usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Input", action="store",
                  dest="Input",

                  help="GBK_ID")
parser.add_option("-o", "--Output", action="store",
                  dest="output",

                  help="OutputPath")

parser.add_option("-t", "--Threshold", action="store",
                  dest="Threshold",
                  type="int",
                  help="Length Threshold!!!")

if __name__ == '__main__':
	(options, args) = parser.parse_args()
	Input = options.Input
	OUTPUT = options.output	
	Threshold = options.Threshold
	
	g=0
	p=0
	for t,s in fasta_check(open( options.Input,'rU') ):
		s2 = re.sub("\s+","",s)
		length = len(s2)
		status = re.search("(\w+)\n",t).group(1)
		if length>Threshold:
			g+=1
			Name="Genome%s"%(g)
		else:
			p+=1
			Name="Plasmid%s"%(p)
		OUT = open(OUTPUT+'/%s.fasta'%(Name),'w')
		OUT.write('>%s Length=%s %s\n%s'%(
	        Name,
	        length,
	        status,
	        s
	    )
	            )
		
			
