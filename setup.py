#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/1
"""
from distutils.core import setup,find_packages
if __name__ == '__main__':	
	setup (# Distribution meta-data
		   name = "McRun",
		   version = "1.0",
		   description = "Microbe genome automate analysis tools",
	# Description of modules and packages in the distribution
		   py_modules = ['McRun'],
	       pacakges = find_packages()
		  )