#!/usr/bin/python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/4/28
import os,sys
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import Get_result
RAW = open( sys.argv[1] )
END = open(Get_result(sys.argv[1])+'.top1','w')
def check( RAW,END    ):
	
	END.write( RAW.next() )
	top_5 = {}
	for line in RAW:
		line_l = line.split('\t')
		if line_l[0] not in top_5:
			top_5[ line_l[0] ] = 1
		elif top_5[ line_l[0] ] ==5:
			continue
		else:
			top_5[ line_l[0] ] +=1
		
already = {}
for line in RAW:
	line_l = line.split('\t')
	if line_l[2] in already:
		continue
	else:
		END.write( '\t'.join( line_l[:-1]  )+'\n' )
		already[ line_l[2] ] = ''
