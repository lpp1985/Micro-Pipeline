#!/usr/bin/env python
#coding:utf-8
"""
Author:  LPP --<Lpp1985@hotmail.com>
Purpose: 123
Created: 2015/1/2
"""

import sys,shlex
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from dependcy import *
import subprocess
def Prokka_Run( Contig,Genius,Spieces,Strain,Center,Prefix,OutPut,Plasmid ):
	Prokka_Commandline = config_hash["Tools"]["Tools"]+' --prefix %(prefix)s --outdir %(output)s --evalue %(e_value)s  --genus %(Genius)s --strain %(Strain)s  --cpus 64 --compliant --quiet --prefix %(Prefix)s  --locustag %(Prefix)s'
	if Plasmid:
		Prokka_Commandline += "--plasmid %s"%(Plasmid)
	commandLine = shlex.split(Prokka_Commandline +" %s"%(Contig) )
	prokka_process = subprocess.Popen(commandLine,stder= subprocess.PIPE,stdout= subprocess.PIPE)
	stder,stdout = prokka_process.communicate()
	if stder:
		raise Exception(
		    "%s's Prokka Annotation is error! Msg is %s"%(
		        Prefix, 
		        stder
		    )
		)