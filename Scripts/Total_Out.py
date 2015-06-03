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
session.query(AnnotationTable).all()
END = open(sys.argv[2],'w')
END.write(
    "\t".join(
        [

            "Name",
	    "Function",
            "Nr_Hit",
            "Nr_Eval",
            "KEGG_Hit",
            "KEGG_Eval",
            "KEGG_KO",
            "KEGG_PATHWAY",
            "Swiss_Hit",
            "Swiss_Eval",
            "Eggnog_Hit",
            "Eggnog_Eval",
            "COG",
            "BiologicalProcess",
            "MolecularFunction",
            "CellularComponent"       
        ]
    )+"\n"
)

for i in session.query(AnnotationTable).all():
	data = [
	    i.Name,
	    i.Function,
	    i.Nr_Hit,
	    i.Nr_Eval,
	    i.KEGG_Hit,
	    i.KEGG_Eval,
	    i.KEGG_KO,
	    i.KEGG_PATHWAY,
	    i.Swiss_Hit,
	    i.Swiss_Eval,
	    i.Eggnog_Hit,
	    i.Eggnog_Eval,
	    i.COG ,
	    i.BiologicalProcess,
	    i.MolecularFunction,
	    i.CellularComponent,    
	]	
	out_data = []
	for e_data in data:
		if e_data:
			out_data.append(e_data)
		else:
			out_data.append("-")
	END.write(
	   "\t".join(
	      out_data
	      )
	+'\n'
	)
	
