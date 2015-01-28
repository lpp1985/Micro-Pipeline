#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/28
"""
import Image,sys,os
from PIL import ImageDraw,ImageFont,ImageColor
sys.path.append(os.path.abspath(os.path.abspath(os.path.split(__file__)[0]))+'/../Lib/')
from lpp import *

from Dependcy import *

OUTPUT = Image.new('RGBA',(1000,750))  
Font_location = config_hash["Utils"]["gapmap"] +'/fonts/'
def Paste_Graph(png,OUTPUT,top,right):
		
	RAW = Image.open(png)
	width =RAW.size[0]
	height = RAW.size[1]

	image1 = RAW.crop((20,20,width,height))

	out = image1.resize((480,360),Image.ANTIALIAS)
	OUTPUT.paste(out,(top,right))



if __name__ == '__main__':

	PATH =sys.argv[1]+'/results/'
	
	Paste_Graph(PATH+'/adapter_observed_insert_length_distribution.png', OUTPUT, 0, 0)	
	Paste_Graph(PATH+'/filtered_subread_report.png', OUTPUT, 500, 0)	
	Paste_Graph(PATH+'/post_filterread_score_histogram.png', OUTPUT, 0, 380)	
	Paste_Graph(PATH+'/post_filter_readlength_histogram.png', OUTPUT, 500, 380)	
	
	NEW = ImageDraw.Draw(OUTPUT)
	font = ImageFont.truetype(Font_location+'times.ttf',21)
	NEW.setfont(font)
	NEW.text((220,360),"(a)",fill="black")
	
	NEW.text((220,730),"(c)",fill="black")
	
	NEW.text((700,360),"(b)",fill="black")
	
	NEW.text((700,730),"(d)",fill="black")
	OUTPUT.save(sys.argv[2])