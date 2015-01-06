#!/usr/bin/python
#coding:utf-8
# Author:  LPP --<lpp1985@hotmail.com>
# Purpose: 
# Created: 2011/5/19
import os,tempfile,sys
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import Get_result
data_f = sys.argv[1:]

for e_f in data_f:
	RAW = blast_parse(open(e_f),open(Get_result(e_f)+'.Bparse','w'))
	RAW.parse()
	
