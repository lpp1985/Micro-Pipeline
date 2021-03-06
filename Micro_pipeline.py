#!/usr/bin/env python
#coding:utf-8
"""
  Author:  LPP --<Lpp1985@hotmail.com>
  Purpose: 
  Created: 2015/1/2
"""
from Lib.Dependcy import *
from termcolor import colored
import time
import os
from optparse import OptionParser
from pyflow import WorkflowRunner

usage = "python2.7 %prog [options]"
parser = OptionParser(usage =usage )
parser.add_option("-i", "--Sequence", action="store",
                  dest="Sequence",

                  help="Contig")
parser.add_option("-o", "--Output", action="store",
                  dest="Output",

                  help="OutputPath")
parser.add_option("-c", "--Config", action="store",
                  dest="Config",

                  help="Config File")

class Download_Ref(WorkflowRunner):
    def __init__(self,Id_All,Path):
        self.Path = Path
        self.Id_all = Id_All
        self.gbk_list  = []
        Make_path(self.Path  )
        self.fasta = "%s/total_ref.fa"%(self.Path)
        for each_reference in self.Id_all.split('; '):
            self.gbk_list.append(self.Path+'/'+each_reference+'.gbk')
    def workflow(self):

        print(
            colored(
                "Step 1 Download Reference into %s And Combine them"%(self.Path),
                "green"
            )
        )		

        i=0
        dependcy = []
        for each_reference in self.Id_all.split('; '):

            i+=1

            self.addTask(
                "Download_ref%s"%(i),
                "nohup "+scripts_path+"/Download_reference.py -i %s -o %s"%(each_reference,self.Path ),

            )

            dependcy.append( "Download_ref%s"%(i) )

        self.addTask(
            "Combine",
            "nohup cat %s >%s/total_ref.fa"%(
                self.Path+'/*.fasta',
                self.Path 		
                ) ,
            dependencies = dependcy
        )





class Circle_Contig(WorkflowRunner):
    def __init__(self,Contig,Output,Ver= False):
        self.Path = os.path.abspath(os.path.split(Output)[0])
        self.Output = Output
        Make_path(self.Path)
        self.Contig = Contig
        self.Ver = Ver

    def workflow(self):
        print(
            colored(
                "Step 2 Check Contig's Termpology result %s"%(self.Ver),
                "green"
            )
        )			
        commandline = "nohup " +scripts_path+"Circula.py -i %s  -o %s "%(self.Contig,self.Output)
        if self.Ver:
            commandline +="-v"
        self.addTask(
            "Check_Result",
            commandline
        )




class Split_Sequence(WorkflowRunner):
    """Split Chromosomes"""
    def __init__(self,Input,Path,Threshold):
        if not Path.endswith("/"):
            Path+='/'
        self.Path = Path
        Make_path(Path)
        self.Threshold = int(Threshold)
        self.Input = Input
        self.totalfna =Path+'/total.fna'

    def workflow(self):

        print( 
            colored("Sequence Split into Chromosome or Plasmid","green"  )
        )	
        self.addTask("Split","nohup " +scripts_path+'/Fasta_split.py -i %s -o %s -t %s'%(
            self.Input,
            self.Path,
            self.Threshold
        )
                     )	
        self.addTask(
            "Cat_all",  
            "cat %(path)s/*.fasta >%(path)s/total.fna"%(
                {"path":self.Path}
                ),
            dependencies="Split"
        )

class RepeatMasker(WorkflowRunner):
    """Split Chromosomes"""
    def __init__(self,Input,Path):
        if not Path.endswith("/"):
            Path+='/'        
        self.Path = Path
        Make_path(Path)
        self.Input = Input


    def workflow(self):

        print( 
            colored("RepeatMakser Sequence","green"  )
        )	
        self.addTask("Split",config_hash["Tools"]["repeatmasker"]+" -pa 64 -norna -dir %s  -gff  -html %s  "%(
            self.Path,
            self.Input
        )
                     )	


class Order_Adjust(WorkflowRunner):
    "Adjust Order"
    def __init__(self,Contig,Ref,Output):
        Path = os.path.split(Output)[0]
        Make_path(Path)
        self.Contig = Contig
        self.Ref = Ref
        self.Output = Output
    def workflow(self):
        print(colored("Step3 Order Adjust","green") )
        self.addTask("Adjust","nohup "+scripts_path+'/Sequence_order_adjust.py -s %s -r %s -o %s'%(
            self.Contig,
            self.Ref,
            self.Output
        )
                     )			
class Draw_Graph(WorkflowRunner):
    def __init__(self,Gbk):
        self.Gbk = Gbk
        self.Output = os.path.split(Gbk)[0]+'/out.png'
    def workflow(self):
        print(colored("%s Is Drawing"%(self.Gbk),"green"  ))
        self.addTask("Draw", 
                     command="nohup "+ scripts_path+"/Circular_Graph_Draw.py -g %s -o %s"%(self.Gbk,self.Output), 
                     cwd=os.path.split(self.Gbk)[0]
                     )	
class Gene_Prediction(WorkflowRunner):
    def __init__(self,Contig,Genius,Spieces,Strain,Center,Prefix,OutPut,Plasmid, Evalue):
        self.Contig = Contig
        self.Commandline = Prokka_Commandline(Contig, Genius, Spieces, Strain, Center, Prefix, OutPut,  Plasmid, Evalue)

        self.gbk = OutPut+'/'+Prefix+'.gbk'
        self.Protein =OutPut+'/'+Prefix+'.faa'
        self.graph = OutPut+'/out.png'
        self.ffn = OutPut+'/'+Prefix+'.ffn'
        self.TotalDatabase = OutPut+"../../total.db"
    def workflow(self):
        if os.path.isfile(self.graph):
            return ""
        print(colored("%s is annotating"%(self.Contig),'blue') )
        self.addTask("Annotation",self.Commandline)
        draw_flow = Draw_Graph(self.gbk)
        self.addWorkflowTask("Drawing",draw_flow,dependencies=["Annotation"])
        self.addTask("Database",
                     scripts_path+"/create_database.py "+self.TotalDatabase+" "+self.ffn,
                     dependencies=["Annotation"]
                     )
        #self.addTask("Annotation",scripts_path+" "+self.TotalDatabase+" "+  )
        self.TotalDatabase


class Blast(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
    def workflow(self):
        print("%s is start to blast to %s"%(self.Input,self.Database))
        blast_out = self.Output+'.xml'
        self.addTask("Blast","nohup "+scripts_path +"blast_continue.py -i %s -o %s -e %s -d %s "%(
            self.Input,
            blast_out,
            self.E_value,
            self.Database,

        )
                     )




class Nr_Mapping(Blast):
    def __init__(self,Input,Output):
        self.Input = Input
        self.Output = Output
        self.Database = config_hash["Database"]["nr"]
        self.E_value = config_hash["Threshold"]["e_value"]
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db" 
    def workflow(self):
        print(
            colored(
                "%s's Nr Result is Running"%(self.Input),
                "red"
            )
        )       

        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)
        self.addTask("Database",
                     "nohup "+scripts_path+'/Nr_Database.py %s %s.top1 '%(
                         self.Total_Database,
                         self.Output
                         ),
                     dependencies="Blast"

                     )        
class COG_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db"

    def workflow(self):
        print(
            colored(
                "%s's Cog Result is Running"%(self.Input),
                "red"
            )
        )	
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )		
        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)

        self.addTask("COG",
                     "nohup "+scripts_path+'/COG_mapping.py -i %(result)s.top1 -o %(result)s.cog'%(
                         {"result":self.Output}
                         ),
                     dependencies="Blast"

                     )

        self.addTask(
            "Database",
            "nohup "+scripts_path+'/COG_Database.py %s  %s.cog '%(
                self.Total_Database,
                self.Output
                ),
            dependencies=["Blast","COG"]
        )         
        self.addTask(
            "Stat",
            "nohup "+scripts_path+'/cog_stat.py  %(result)s.cog %(result)s.stat'%(
                {"result":self.Output}
                ),
            dependencies=["Blast","COG"]
        )          


        self.addTask(
            "Draw",
            "nohup "+scripts_path+'/Cog_draw.py  %(result)s.cog %(path)s/stats.png %(path)s/Draw.R'%(
                {"result":self.Output,
                 "path":os.path.dirname(self.Output)
                 }
                ),
            dependencies=["Blast","COG"]
        )           


class GO_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db"


    def workflow(self):
        print(
            colored(
                "%s's GO Result is Running"%(self.Input),
                "red"
            )
        )		
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )	


        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)	
        self.addTask("GO",
                     "nohup "+scripts_path+'/GO_Mapping.py  %(result)s.top1  %(result)s'%(
                         {"result":self.Output}
                         ),
                     dependencies="Blast"

                     )


        self.addTask(
            "Fetch",
            "nohup "+scripts_path+'/get_GO.py  %(result)s.GO-mapping.detail  %(result)s.annotaion_detail'%(
                {"result":self.Output}
                ), 
            dependencies=["Blast","GO"]

        )     

        self.addTask(
            "Database",
            "nohup "+scripts_path+'/GO_Database.py  %s  %s.annotaion_detail'%(
                self.Total_Database,
                self.Output
                ), 
            dependencies=["Blast","GO","Fetch"]

        )     
        self.addTask(
                    "Swissprot",
                    "nohup "+scripts_path+'/Swiss_Database.py  %s  %s.top1'%(
                        self.Total_Database,
                        self.Output
                        ), 
                    dependencies=["Blast","GO","Fetch"]
        
                )          

        self.addTask(
            "Detail",
            "nohup "+scripts_path+'/Go_list.py  %(result)s.GO-mapping.list  %(result)s.class'%(
                {"result":self.Output}
                ), 
            dependencies=["Blast","GO"]

        ) 



        self.addTask(
            "Stats",
            "nohup " +scripts_path+"/GO_stat.py  %(result)s.GO-mapping.list %(result)s.stat"%(
                {
                    "result":self.Output
                }
            )
            ,dependencies=["Blast","GO"]

        )

        self.addTask(
            "Draw",
            "nohup "+scripts_path+'/GO_draw.py  %(result)s.class %(path)s/stats.png %(path)s/Draw.R'%(
                {"result":self.Output,
                 "path":os.path.dirname(self.Output)
                 }
                ),
            dependencies=["Blast","GO","Detail"]
        )           

class Pathway_Mapping(WorkflowRunner):
    def __init__(self,Input,Output,Database,E_value):
        self.Input = Input
        self.Output = Output
        self.Database = Database
        self.E_value = E_value
        self.Total_Database = os.path.split( self.Input)[0]+"/../../total.db"

    def workflow(self):
        print(
            colored(
                "%s's KEGG Pathway Result is Running"%(self.Input),
                "red"
            )
        )
        if not os.path.isfile(self.Input):
            raise Exception(
                colored("%s is not exist!!"%(self.Input),"green")
            )		
        name = os.path.split(self.Input)[-1].rsplit('.',1)[0]
        blast_flow = Blast(self.Input, self.Output, self.Database, self.E_value)
        self.addWorkflowTask("Blast",blast_flow)	
        time_tag = int(time.time())

        self.addTask("To_sql",
                     "nohup "+config_hash["Utils"]["gapmap"]+'/blast_sql_multi.py -f %(result)s.xml   -r  %(result)s.xml   -1 forward -2 forward  -n %(name)s_for -N %(name)s_rev -p %(pep)s -d %(dna)s -x %(tag)s'%(
                         {
                             "pep":self.Input,
                             "dna":re.sub("\.faa$",".ffn",self.Input),
                             "result":self.Output,
                             "name":name,
                             "tag":time_tag
                         }
                         ),
                     dependencies="Blast"

                     )



        source_location  = os.path.split(self.Output)[0]+'/source/'
        self.addTask(
            "Build",
            "nohup "+config_hash["Utils"]["gapmap"]+"/Mapping_sql_Multi.py %s %s"%(
                source_location,
                time_tag,
                ) +" && "+config_hash["Utils"]["gapmap"]+"/Show_all_Mapping.py %s %s"%(
                    os.path.split(self.Output)[0]+"/Gene_Mapping.tsv",
                    time_tag,
                    ),
            dependencies=["Blast","To_sql"]
        )
        self.addTask(
            "Make",
            "nohup "+config_hash["Tools"]["sphinx"] +" -b html -d %(out)s/doctrees %(location)s %(out)s/pathway"%(
                {   
                    "out":self.Output,
                    "location":source_location
                }   
                ),  
            dependencies=["Blast","To_sql","Build"]
        )           
        self.addTask(
            "Database",
            "nohup "+scripts_path+"/KEGG_Database.py "+self.Total_Database+" "+self.Output+".top1"+" "+os.path.split(self.Output)[0]+"/Gene_Mapping.tsv",

            dependencies=["Blast","To_sql","Build"]
        )		

        self.addTask(
            "Stat",
            "nohup "+scripts_path+"/Pathway_stats.py %(name)s %(out)s.detail %(out)s.stat"%(
                {
                    "name":time_tag,
                    "out":self.Output
                }
                ),
            dependencies=["Blast","To_sql"]

        )        
        self.addTask(
            "Draw",
            "nohup " +scripts_path+"/Pathway_Draw.py   %(out)s.detail %(path)sstat.png  %(path)sstat.R"%(
                {
                    "out":self.Output,
                    "path":os.path.split(self.Output)[0]+'/'


                }
                ),
            dependencies=["Blast","To_sql","Stat"]

        )    
        self.addTask(
            "Clean",
            "nohup rm %(raw)s && rm %(source)s -rf"%(
                {
                    "raw":config_hash["Utils"]["gapmap"]+'/%s'%(time_tag),
                    "source":source_location,
                }
                ),
            dependencies=["Blast","To_sql","Build","Make","Stat"]

        )        





class Data_prapare(WorkflowRunner):
    def __init__(self,Contig,OUTPUT):
        self.Contig = Contig
        if not OUTPUT.endswith('/'):
            OUTPUT+='/'
        self.Output = OUTPUT
        Get_Path(OUTPUT)
        Check_file([["",self.Contig]])

        self.ref_fasta = ""	
    def get_contigs(self):
        return glob.glob(os.path.abspath(self.result_path)+'/*.fasta')
    def workflow(self):
        dependcy = []
        refer_path = self.Output+"/reference/"
        circyle_path = self.Output+"/Circyled_contig/"
        adjusted_path = self.Output+"/Adjusted_contig/"

        splited_path = self.Output+"/Assembly_END/"
        self.result_path = splited_path
        if config_hash["Reference"]["gbk"]:
            Id_All = config_hash["Reference"]["gbk"]
            down_flow = Download_Ref(Id_All, refer_path)
            self.addWorkflowTask("Download", down_flow)
            self.gbk_list = down_flow.gbk_list
            self.ref_fasta = down_flow.fasta
            dependcy.append("Download")

        if config_hash["Pipeline"]["checkassembly"].strip().lower()=="yes":
            Ver = True
        else:
            Ver = False
        cir_flow = Circle_Contig(self.Contig,circyle_path+"Circled.Contigs",Ver)
        self.addWorkflowTask("Circle",cir_flow,dependencies=dependcy)
        dependcy.append("Circle")
        adjusted_result = cir_flow.Output


        # Adjusted Result
        if config_hash["Reference"]["gbk"]:
            adjust_flow = Order_Adjust(adjusted_result, self.ref_fasta, adjusted_path+"assembly_end.fasta")
            self.addWorkflowTask("Adjusted",adjust_flow,dependencies= dependcy)
            adjusted_result = adjust_flow.Output
            dependcy.append("Adjusted")

        split_flow = Split_Sequence(adjusted_result, splited_path, config_hash["Threshold"]["genomesize"])
        self.addWorkflowTask("Split",split_flow,dependencies=dependcy)
        dependcy.append("Split")
        print (colored(split_flow.totalfna,"red"))
        repeatmasker_flow = RepeatMasker(split_flow.totalfna, self.Output+"/RepeatMasker/")
        self.addWorkflowTask("Repeat",repeatmasker_flow,dependencies=dependcy)

class Annotation_Run(WorkflowRunner):
    def __init__(self,Contig_list,OUTPUT):
        self.Contig_list = Contig_list
        self.Output = os.path.abspath(OUTPUT)
        Get_Path(OUTPUT)
    def workflow(self):
        dependcy = []
        annotation_path = self.Output+"/Annotation/"
        splited_path = self.Output+"/Assembly_END/"
        prediction_path  =  self.Output+"/Prediction/"
        protein_sequence_list = []


        # Gene Prediction
        for each_contig in self.Contig_list:
            prefix = re.search("^(\w+\d+)\.",os.path.split(each_contig)[-1]).group(1)
            category = re.search("^(\w+)\d+\.",os.path.split(each_contig)[-1]).group(1)
            genius = config_hash["Taxon"]["genius"]
            spieces = config_hash["Taxon"]["spieces"]
            strain = config_hash["Taxon"]["strain"]
            center = config_hash["Taxon"]["center"]

            each_prediction_path = prediction_path+'/%s/'%(prefix)
            if category =="Plasmid":
                plasmid = prefix
            else:
                plasmid=''
            self.addWorkflowTask(
                "%s_prediction"%(prefix),
                Gene_Prediction(
                    each_contig,
                    genius,
                    spieces, 
                    strain, 
                    center, 
                    prefix, 
                    each_prediction_path, 
                    plasmid,
                    config_hash["Threshold"]["e_value"]
                    ),
            )
            dependcy.append(
                "%s_prediction"%(prefix)
            )
            protein_sequence_list.append(
                each_prediction_path+'/%s.faa'%(prefix)
            )	

        # COG,Pathway,GO,Nr Annotation
        for each_protein in protein_sequence_list:

            each_dependcy = dependcy
            each_name = os.path.split(each_protein)[-1].rsplit('.',1)[0]
            self.addWorkflowTask(
                "COG%s"%(each_name),
                COG_Mapping(each_protein, 
                            annotation_path+'/%s/COG/%s'%(each_name,each_name),
                            config_hash["Database"]["eggnog"],
                            config_hash["Threshold"]["e_value"]

                            ),
                dependencies= dependcy
            )			
            each_dependcy.append("COG%s"%(each_name))            
            self.addWorkflowTask(
                "Pathway%s"%(each_name),
                Pathway_Mapping(
                    each_protein, 
                    annotation_path+'/%s/Pathway/%s'%(each_name,each_name),
                    config_hash["Database"]["kegg"],
                    config_hash["Threshold"]["e_value"]
                    ),
                dependencies= dependcy
            )	
            each_dependcy.append("Pathway%s"%(each_name))            
            self.addWorkflowTask(
                "Nr%s"%(each_name),
                Nr_Mapping(
                    each_protein, 
                    annotation_path+'/%s/nr/%s'%(each_name,each_name)
                    ),
                dependencies= dependcy
            )

            each_dependcy.append("Nr%s"%(each_name))

            self.addWorkflowTask(
                "GO%s"%(each_name),
                GO_Mapping(each_protein, 
                           annotation_path+'/%s/GO/%s'%(each_name,each_name),
                           config_hash["Database"]["swiss"],
                           config_hash["Threshold"]["e_value"]

                           ),
                dependencies= dependcy
            )			
            each_dependcy.append("GO%s"%(each_name))




class TotalAnno_Run(WorkflowRunner):
    def __init__(self,OUTPUT):
        self.PATH = os.path.abspath(OUTPUT)+'/'
    def workflow(self):
        self.addTask("Total",scripts_path+"/Total_Out.py "+self.PATH+"total.db "+self.PATH+"annotation.xls")

if __name__ == '__main__':
    (options, args) = parser.parse_args()
    Sequence = options.Sequence
    OUTPUT   = options.Output
    Config   = options.Config
    os.environ["PATH"] = os.getenv("PATH")+'; '+scripts_path
    if not os.path.isfile(Config):
        raise Exception("File %s is not exist!!"%(Config))
    Get_Addtional_Config( Config )
    Config_Parse(general_config)
    print config_hash
    data_prepare_flow = Data_prapare(Sequence,OUTPUT)

    error = data_prepare_flow.run()
    Contig_list = data_prepare_flow.get_contigs()

    annotation_flow = Annotation_Run(Contig_list, OUTPUT)
    error = annotation_flow.run()
    cobine_flow = TotalAnno_Run(OUTPUT)
    error = cobine_flow.run()
