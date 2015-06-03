#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""
import os,sys
sys.path.append(os.path.split(__file__)[0]+'/../Lib/')
from lpp import *
from Dependcy import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


db_file = os.path.abspath(sys.argv[1])
Ddatabase_engine = create_engine(  'sqlite:///%s'%(db_file) )
Ddatabase_engine.connect()
Base.metadata.create_all( Ddatabase_engine  )
Session = sessionmaker( bind = Ddatabase_engine  )
session = Session()
FASTA = fasta_check(open(sys.argv[2],'rU'))
for t,s in FASTA:
	try:
		t = t[1:].strip()
		name,anno = t.split(" ",1)
	except:
		continue
	go_data = get_or_create(session, AnnotationTable,Name = name)
	go_data.Function = anno
	session.commit()
