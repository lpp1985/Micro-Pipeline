#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/2
"""
import os,sys
python_env = os.getenv('PYTHONPATH')
if not python_env:
	python_env = ""
os.environ['PYTHONPATH']=python_env+','+os.path.split(__file__)[0]+'/../Lib/'
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from Dependcy import *
from optparse import OptionParser
from lpp import *
def Adjust_Seqeunce(head_name,title,sequence):
	"sequence Adjust"
	status = re.search("(\w+)\n",title).group(1)
	CACHE = open("cache",'w')
	title = title.split()[0]
	CACHE.write(title+"\n"+sequence)
	CACHE.close()
	if status =="Circle":
		command_line = """ %s --maxmatch %s %s 1>/dev/null 2>/dev/null && show-tiling -a  out.delta    """%( nucmer,CACHE.name,head_name  )
		stdout = os.popen( command_line  ).read()
		print(command_line)
		if not stdout:
			seq_new = sequence
			return seq_new
		coords_list = [int(x) for x in stdout.split()[:4]]
		if coords_list[-1]< coords_list[-2]:
			strain = '-'
			start = coords_list[1]
		else:
			strain='+'
			start = coords_list[0]
		sequence = re.sub("\s+","",s).upper()
		if strain =='-':
			seq_new = sequence[start:]+sequence[:start]
		else:
			seq_new = sequence[start-1:]+sequence[:start-1]
		if strain=="-":
			seq_new = complement(seq_new)
			
		
	else:
		seq_new = sequence
	seq_new = re.sub("(\w{60})","\\1\n",seq_new)+'\n'
	os.remove(CACHE.name)
	return seq_new
	


if __name__ == '__main__':
	usage = "python2.7 %prog [options]"
	parser = OptionParser(usage =usage )
	
	parser.add_option("-s", "--Sequence", action="store",
		              dest="Sequence",
		              help="Sequence")
	
	parser.add_option("-r", "--Ref", action="store",
		              dest="Ref",
	
		              help="reference sequence")
	
	parser.add_option("-o", "--Out", action="store",
		                  dest="Output",
		
		                  help="output")
	(options, args) = parser.parse_args()
	SEQUENCE = fasta_check(    open( options.Sequence ,'rU'  )     )
	REF = fasta_check(    open( options.Ref ,'rU'  )     )
	OUTPUT =  open( options.Output ,'w'  )     
	#                                                          #
	#  Prepare head sequence for Sequence Adjustment!!!!       #
	#                                                          #
	HEAD = open("head.fasta",'w')
	for t,s in REF:
		s = re.sub("\s+","",s)
		HEAD.write(t.split()[0]+'\n'+s[:2000]+'\n')
	HEAD.close()
	nucmer = config_hash["Tools"]["Nucmer"]
	nucmer ="nucmer"
	for t,s in SEQUENCE:
		s = re.sub("\s+","",s)
		seq_adjusted = Adjust_Seqeunce(HEAD.name, t, s)
		OUTPUT.write(t+seq_adjusted)
