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

END.write("GO\tAnnotation\tGene Number\n")
for line in RAW:
	if '->' in line:
		continue
	END.write(line)
	