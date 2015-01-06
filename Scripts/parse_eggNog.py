#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/6/20
"""
import os,sys
sys.path.append(
    os.path.abspath(os.path.split(__file__)[0]+'../Lib/' )
)	
from lpp import *
from Dependcy import *
from collections import namedtuple

from sqlobject import *
from optparse import OptionParser
class NOG_des(SQLObject):
    class sqlmeta:
        table="NOG_Description"
    Name = StringCol(length=50,unique=True)
    Description = StringCol()
    name_index= DatabaseIndex(Name)

class NOG_GENE( SQLObject  ):
    class sqlmeta:
        table="Gene_NOG"
    Gene = StringCol(length=100)
    NOG = StringCol(length=50,)
    gene_index = DatabaseIndex(Gene)
    nog_index = DatabaseIndex(NOG)
    
    
class NOG_CAT( SQLObject  ):
    class sqlmeta:
        table="NOG_Category"
    NOG =StringCol(length=50)
    Cat = StringCol(length=10)
    nog_index = DatabaseIndex(NOG)
    cat_index = DatabaseIndex(Cat)
    
class CAT_DES( SQLObject  ):
    class sqlmeta:
        table="CAT_des"
    Abb= StringCol(length=4)
    Description = StringCol()
    cat_index = DatabaseIndex(Abb)
    


def get_or_create(model, **kwargs):
    ''' use it to get or create object from a table '''

    instance = model.selectBy(**kwargs)
    
    if instance.count():
        return instance
    else:
        instance = model(**kwargs)

        return instance

user = "root"
password = "gass_1985"
mysql_connection = "mysql -u%s -p%s  --local-infile=1 eggNOG "%(user,password)
mysql_build = "mysql -u%s -p%s  --local-infile=1 "%(user,password)
connection_string = 'mysql://%s:%s@localhost/eggNOG'%(user,password)    
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection
if __name__ == '__main__':
    usage = '''usage: python2.7 %prog [options] 
         parse eggNOG data
   
         '''
    parser = OptionParser(usage =usage )    
    parser.add_option("-d", "--DES", action="store",
                      dest="description",
                      help="NOG descripton")
    parser.add_option("-r", "--Rela", action="store",
                      dest="rela",
                      help="NOG gene Rela")
    parser.add_option("-a", "--Anno", action="store",
                      dest="anno",
                      help="Cat annotation")    
    parser.add_option("-c", "--Cat", action="store",
                      dest="cate",
                      help="NOG gene Category")  
    parser.add_option("-s", "--Seq", action="store",
                          dest="sequence",
                          help="NOG gene Category")      
    
    (options, args) = parser.parse_args()
    os.system(mysql_build+"-e 'create database eggNOG;'")
    os.system(mysql_build+"-e 'drop database eggNOG;'")
    os.system(mysql_build+"-e 'create database eggNOG;'")
    

    NOG_des.createTable(ifNotExists=True)
    NOG_GENE.createTable(ifNotExists=True)
    CAT_DES.createTable(ifNotExists=True)
    NOG_CAT.createTable(ifNotExists=True)
   
    ANNO = open(options.anno,'rU')

    for (abb,description) in  re.findall( "\[(\w)\]\s+([^\n]+)",ANNO.read()  ):
        get_or_create(CAT_DES,Abb=abb,Description=description)
  
  
  
  
    Nog = namedtuple("Nog","Id Description")

    noglify = Nog._make
    Rela = namedtuple("RELA","NOG_ID,Protein,Start,End")
    
    
    
    
    
    relalify = Rela._make
    DES = open(options.description , 'rU')
    DES.next()
    TMP = open("tmp",'w')
    for line in DES:
        if line[-1]=='\n':
            line = line[:-1]        
        nog_data =  noglify(line.split("\t"))
        TMP.write(line+'\n')
    load_des_script = """-e 'load data local infile   "%s" into table NOG_Description (name, description);'"""%(TMP.name)
    os.system( mysql_connection+load_des_script   )

   
    
    CAT = open(options.cate,'rU')
    TMP = open("tmp",'w')
    for line in CAT:
        if line[-1]=='\n':
            line = line[:-1]
        nog_data =  noglify(line.split("\t"))
        nog_table = NOG_des.selectBy(  Name=nog_data.Id  )
        for data in nog_data.Description:
            TMP.write(nog_data.Id+'\t'+data+'\n')
    load_cate_script = """-e 'load data local infile   "%s" into table  NOG_Category (no_g,cat);'"""%(TMP.name)
    os.system( mysql_connection+load_cate_script   )
    

    TMP = open("tmp",'w')
    for each_f in  glob.glob("*"+options.rela):
        RELA = open(each_f , 'rU')
        RELA.next()

    
        for line in RELA: 
            try:
                rela_data = relalify(line[:-1].split("\t"))
                TMP.write(rela_data.Protein+'\t'+rela_data.NOG_ID+'\n')
            except:
                print(line)

    load_rela_script = """-e 'load data local infile   "%s" into table Gene_NOG (gene,no_g);'"""%(TMP.name)
    os.system( mysql_connection+load_rela_script   )
    
    SEQ = fasta_check(open(options.sequence,'rU'))
    END = open('total.validate.sequence.fasta','w')
    for t,s in SEQ:
        t_name = t.strip()[1:]
        if NOG_GENE.selectBy(Gene = t_name).count():
            END.write(">"+t_name+'\n'+s)
