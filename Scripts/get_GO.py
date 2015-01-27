#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/12/30
"""
import sys,shlex,os,subprocess

sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
GO_Location = config_hash["Database"]["go"]
go_compt = File_dict(open(GO_Location+'/GO_Component','rU')).read(1,2)
go_def = File_dict(open(GO_Location+'/NAME_DEF.list','rU')).read(1,2)
id_go = Ddict()
for line in open(sys.argv[1],'rU'):
	line_l = line.strip().split("\t")
	for  e_f in line_l[1:]:
		id_go[line_l[0]] [e_f] = ""
END = open(sys.argv[2],'w')
END.write('GeneID\t'+"GO-BiologicalProcess"+'\t'+"GO-MolecularFunction"+"\tGo-CellularComponent\n")
end_order = ["biological_process","molecular_function","cellular_component"]
for key in id_go:
	all_go = id_go[key]
	mapp_result = Ddict()
	for each_go in all_go:
		mapp_result[go_compt[each_go]  ] [ each_go ]=""

	result = "\t".join([ '; '.join([ each_go+'//%s'%(go_def[each_go])  for each_go in   mapp_result[x]  ] )     for x in end_order    ])
	END.write(key+"\t"+result+'\n')
	
