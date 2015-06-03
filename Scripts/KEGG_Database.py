#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/3/16
"""

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
KEGG_ANNO_Detail = open(sys.argv[2],'rU')
KEGG_ANNO_Detail.next()
for line in KEGG_ANNO_Detail:
	line_l = line[:-1].split("\t")
	go_data = get_or_create(session, AnnotationTable,Name = line_l[0].split()[0])
	go_data.KEGG_Hit = line_l[1].split()[0]
	go_data.KEGG_Eval = line_l[10]

	session.commit()
PATHWAY_DETAIL = open(sys.argv[3],'rU')
PATHWAY_DETAIL.next()
for line in PATHWAY_DETAIL:
	line_l = line[:-1].split("\t")
	go_data = get_or_create(session, AnnotationTable,Name = line_l[0])
	go_data.KEGG_KO = line_l[1]
	go_data.KEGG_PATHWAY = line_l[2]
	session.commit()
