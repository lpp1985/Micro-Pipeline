#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/11
"""
from lpp import *
cog_mapping =Ddict() 
RAW = open(sys.argv[1] ,'rU')
RAW.next()
cog_detail = {}
for line in RAW:
	line_l = line.strip().split("\t")
	cog_cate_annotation = line_l[6]

	cog_annotation = re.sub("\s+\[\w+\]$","",cog_cate_annotation)
	cog_cate = re.search("\[(\w+)\]$",cog_cate_annotation).group(1)
	cog_detail[cog_cate] = cog_annotation
	cog_mapping[cog_cate][line_l[0]]

END = open(sys.argv[2],'w')
END.write("Category\tAnnotation\tGene Number\n")
for key ,val in cog_detail.items():
	#print(cog_mapping[key])
	END.write(key+'\t'+val +'\t%s\n'%(   len(cog_mapping[key])))
