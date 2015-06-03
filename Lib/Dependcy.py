#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2014/12/31
"""
import sys,os
from termcolor import colored
from pyflow import WorkflowRunner
from ConfigParser import ConfigParser
from lpp import *
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
def Get_Path( path ):
	if not os.path.exists(path):

		os.makedirs( path )
def Get_result(name):
	new_name = name.rsplit('.',1)[0]
	return new_name

# set sys.path

lib_path =  os.path.split(__file__)[0]
scripts_path = os.path.join(lib_path,"../Scripts/")

sys.path.extend([lib_path, scripts_path] )
#set Path Env
os.environ["PATH"] = os.getenv("PATH")+','+scripts_path

#parse config
config_path = os.path.join(lib_path,"../Config/")
general_config = ConfigParser()

general_config.read(
    os.path.join( config_path,"general.ini")
)
class AnnotationTable(  Base  ):
	__tablename__='Annotation'
	Id = Column(   Integer,primary_key=True )
	Name = Column(  String(20) ,index = True,nullable = False)
	Function = Column(  Text)
	Nr_Hit=Column(  Text,nullable = True)
	Nr_Eval = Column(  Text,nullable = True)
	KEGG_Hit = Column(  Text,nullable = True)
	KEGG_KO = Column(  Text,nullable = True)
	KEGG_PATHWAY = Column(  Text,nullable = True)
	KEGG_Eval = Column(  Text,nullable = True)
	Swiss_Hit = Column(  Text,nullable = True)
	Swiss_Eval = Column(  Text,nullable = True)
	Eggnog_Hit = Column(  Text,nullable = True)
	COG = Column(  Text,nullable = True)
	Eggnog_Eval = Column(  Text,nullable = True)
	BiologicalProcess = Column(  Text,nullable = True)
	MolecularFunction = Column(  Text,nullable = True)
	CellularComponent = Column(  Text,nullable = True)
	__table_args__=(
		UniqueConstraint(  "Name" ,

		                   ),
	)
	def __init__(  self,Name ):
		self.Name = Name
	def __repr__( self ):
		return self.Name



class AnnotationTable_RPKM(  Base  ):
	__tablename__='Annotation_RPKM'
	Id = Column(   Integer,primary_key=True )
	Name = Column(  String(20) ,index = True,nullable = False)
	Sequence = Column(  Text )
	RPKM = Column(  Text,nullable = True)
	Function = Column(  Text)
	Nr_Hit=Column(  Text,nullable = True)
	Nr_Eval = Column(  Text,nullable = True)
	KEGG_Hit = Column(  Text,nullable = True)
	KEGG_KO = Column(  Text,nullable = True)
	KEGG_PATHWAY = Column(  Text,nullable = True)
	KEGG_Eval = Column(  Text,nullable = True)
	Swiss_Hit = Column(  Text,nullable = True)
	Swiss_Eval = Column(  Text,nullable = True)
	Eggnog_Hit = Column(  Text,nullable = True)
	COG = Column(  Text,nullable = True)
	Eggnog_Eval = Column(  Text,nullable = True)
	BiologicalProcess = Column(  Text,nullable = True)
	MolecularFunction = Column(  Text,nullable = True)
	CellularComponent = Column(  Text,nullable = True)
	__table_args__=(
		UniqueConstraint(  "Name" ,

		                   ),
	)
	def __init__(  self,Name ):
		self.Name = Name
	def __repr__( self ):
		return self.Name




def get_or_create(session, model, **kwargs):
	''' use it to get or create object from a table '''

	try:
		instance = session.query(model).filter_by(**kwargs).first()
	except  Exception,err:
		print( err )
		print( kwargs )
	if instance:
		return instance
	else:
		instance = model(**kwargs)
		session.add( instance  )
		session.commit()
		return instance



def Check_file(file_name_list):
	for key,file_name in file_name_list:
		if not os.popen("which %s"%(file_name) ).read() and not os.path.isfile(file_name):
			raise Exception(file_name +"is not exist!!!")

def Make_path(path):
	if not os.path.isdir(path):
		os.makedirs(path)


def Check_path( name,file_path):
	if not os.path.isdir(file_path):
		raise Exception(name+"'s setting--"+file_path +" is not exist!!!")
config_hash = Ddict()
def Config_Parse(general_config):
	global config_hash
	tools_section =general_config.items("Tools")
	report_section = general_config.items("Report")
	database_section = general_config.items("Database")
	util_section = general_config.items("Utils")
	#for name,each_db in database_section:
		#Check_path(name,each_db)
	#Check_file(tools_section)
	#for key,path in util_section:
		#Check_path(key,path)
	#Check_path(general_config.get("Report","Template"))
	for section in general_config.sections():
		for key in general_config.options(section):

			config_hash[section][key] = general_config.get(section,key)




def Get_Addtional_Config(Addtional_File):
	global config_hash
	addtional_config = ConfigParser()
	addtional_config.read(
		os.path.abspath(Addtional_File)
	)	
	for section in addtional_config.sections():
		for key in addtional_config.options(section):

			config_hash[section][key] = addtional_config.get(section,key)	



def Prokka_Commandline( Contig,Genius,Spieces,Strain,Center,Prefix,OutPut,Plasmid,Evalue ):
	raw_commandline = config_hash["Tools"]["prokka"]+ '  --rfam  --prefix %(Prefix)s --outdir %(output)s --evalue %(e_value)s  --genus %(Genius)s --strain %(Strain)s  --cpus 64 --compliant --force --quiet --centre %(Centre)s  --prefix %(Prefix)s  --locustag %(Prefix)s'%(
		{
	        "Centre":Center,
			"Prefix":Prefix,
			"output":OutPut,
			"e_value":Evalue,
			"Genius":Genius,
			"Strain":Strain,
		}
	)

	if Plasmid:
		raw_commandline += " --plasmid %s"%(Plasmid)
	commandLine = raw_commandline +" %s"%(Contig) 
	commandLine += """&& sed -i  "s/ACCESSION/ACCESSION   123/g" %(Path)s && sed -i "s/VERSION/VERSION    1/g" %(Path)s"""%(
	    {
	        "Path":OutPut+"/"+Prefix+'.gbk'
	    }
	)
	Get_Path( re.sub("[^/+]\/$","",os.path.split(OutPut)[0])  )
	return commandLine

Config_Parse(general_config)
