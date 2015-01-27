#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/23
"""
import sys
RAW = open(sys.argv[1],'rU')
END = open(sys.argv[2],'w')
RAW.next()
END.write("Gene\tFunction\n")
for line in RAW:
	line_l = line.split("\t")
	if line.startswith("GO:"):
		function =line_l[1]
	else:
		gene = line_l[3]
		END.write(gene+"\t"+function+'\n')
		
