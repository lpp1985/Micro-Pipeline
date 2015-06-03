#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2014/12/30
"""
import sys,os

sys.path.append(os.path.abspath(os.path.abspath(os.path.split(__file__)[0]))+'/../Lib/')
from lpp import *

from Dependcy import *
pathway_cat = {
    '6. Human Diseases': {'Drug resistance': ['map00312'], 'Infectious diseases: Bacterial': ['map05111']}, '4. Cellular Processes': {'Transport and catabolism': ['map04144', 'map04145', 'map04142', 'map04146', 'map04140'], 'Cell motility': ['map02030', 'map02040']}, '2. Genetic Information Processing': {'Transcription': ['map03020', 'map03022', 'map03040'], 'Translation': ['map03010', 'map00970', 'map03013', 'map03015', 'map03008'], 'Replication and repair': ['map03030', 'map03410', 'map03420', 'map03430', 'map03440', 'map03450', 'map03460'], 'Folding, sorting and degradation': ['map03060', 'map04141', 'map04130', 'map04120', 'map04122', 'map03050', 'map03018']}, '7. Drug Development': {'Chronology: Nervous system agents': ['map07032', 'map07030', 'map07033', 'map07015', 'map07039', 'map07028', 'map07029', 'map07031', 'map07027', 'map07056', 'map07057'], 'Target-based classification: G protein-coupled receptors': ['map07220', 'map07215', 'map07214', 'map07213', 'map07212', 'map07227', 'map07211', 'map07228', 'map07224', 'map07229'], 'Target-based classification: Nuclear receptors': ['map07225', 'map07226', 'map07223', 'map07222'], 'Target-based classification: Enzymes': ['map07216', 'map07219', 'map07024', 'map07217', 'map07218'], 'Target-based classification: Ion channels': ['map07221', 'map07230', 'map07036', 'map07231', 'map07232', 'map07235'], 'Skeleton-based classification': ['map07110', 'map07112', 'map07114', 'map07117'], 'Chronology: Antiinfectives': ['map07011', 'map07012', 'map07013', 'map07021', 'map07019', 'map07020', 'map07014', 'map07023', 'map07026', 'map07044', 'map07053'], 'Target-based classification: Transporters': ['map07233', 'map07234'], 'Structure-based classification': ['map07025', 'map07034', 'map07035'], 'Chronology: Other drugs': ['map07055', 'map07016', 'map07017', 'map07018', 'map07037', 'map07038', 'map07046', 'map07047', 'map07048', 'map07049', 'map07050', 'map07051', 'map07052', 'map07054'], 'Chronology: Antineoplastics': ['map07040', 'map07041', 'map07042', 'map07043', 'map07045']}, '3. Environmental Information Processing': {'Signal transduction': ['map02020'], 'Membrane transport': ['map02010', 'map02060', 'map03070']}, '1. Metabolism': {'Nucleotide metabolism': ['map00230', 'map00240'], 'Metabolism of terpenoids and polyketides': ['map00900', 'map00902', 'map00909', 'map00904', 'map00906', 'map00905', 'map00981', 'map00908', 'map00903', 'map00281', 'map01052', 'map00522', 'map01051', 'map01056', 'map01057', 'map00253', 'map00523', 'map01054', 'map01053', 'map01055'], 'Glycan biosynthesis and metabolism': ['map00510', 'map00513', 'map00512', 'map00514', 'map00532', 'map00534', 'map00533', 'map00531', 'map00563', 'map00601', 'map00603', 'map00604', 'map00540', 'map00550', 'map00511'], 'Lipid metabolism': ['map00061', 'map00062', 'map00071', 'map00072', 'map00073', 'map00100', 'map00120', 'map00121', 'map00140', 'map00561', 'map00564', 'map00565', 'map00600', 'map00590', 'map00591', 'map00592', 'map01040'], 'Energy metabolism': ['map00190', 'map00193', 'map00195', 'map00196', 'map00710', 'map00720', 'map00680', 'map00910', 'map00920'], 'Metabolism of other amino acids': ['map00410', 'map00430', 'map00440', 'map00450', 'map00460', 'map00471', 'map00472', 'map00473', 'map00480'], 'Metabolism of cofactors and vitamins': ['map00730', 'map00740', 'map00750', 'map00760', 'map00770', 'map00780', 'map00785', 'map00790', 'map00670', 'map00830', 'map00860', 'map00130'], 'Xenobiotics biodegradation and metabolism': ['map00362', 'map00627', 'map00364', 'map00625', 'map00361', 'map00623', 'map00622', 'map00633', 'map00642', 'map00643', 'map00791', 'map00930', 'map00351', 'map00363', 'map00621', 'map00626', 'map00624', 'map00365', 'map00984', 'map00980', 'map00982', 'map00983'], 'Amino acid metabolism': ['map00250', 'map00260', 'map00270', 'map00280', 'map00290', 'map00300', 'map00310', 'map00330', 'map00340', 'map00350', 'map00360', 'map00380', 'map00400'], 'Chemical structure transformation maps': ['map01010', 'map01060', 'map01061', 'map01062', 'map01063', 'map01064', 'map01065', 'map01066', 'map01070'], 'Global and overview maps': ['map01200', 'map01210', 'map01212', 'map01230', 'map01220'], 'Biosynthesis of other secondary metabolites': ['map00940', 'map00945', 'map00941', 'map00944', 'map00942', 'map00943', 'map00901', 'map00403', 'map00950', 'map00960', 'map01058', 'map00232', 'map00965', 'map00966', 'map00402', 'map00311', 'map00332', 'map00331', 'map00521', 'map00524', 'map00231', 'map00401', 'map00254'], 'Carbohydrate metabolism': ['map00010', 'map00020', 'map00030', 'map00040', 'map00051', 'map00052', 'map00053', 'map00500', 'map00520', 'map00620', 'map00630', 'map00640', 'map00650', 'map00660', 'map00562']}
}
sys.path.append(
    config_hash["Utils"]["gapmap"] 
)
from parse import *
Dbname = sys.argv[1]
Ddatabase_engine = create_engine(  "sqlite:///%s/%s"%(base_dir,Dbname) )
Ddatabase_engine.connect()
Base = declarative_base()
Session = sessionmaker( bind = Ddatabase_engine  )
session = Session()	
def get_GeneIdAndKoid(  dir_id  ):

    mapped = session.query( Gene_Ko_Table  ).filter( 
        Gene_Ko_Table.Property_Id == dir_id  
        )

    mapped_ko_hash = dict(  
        [ 
            [i.Ko_id,''] for i in     mapped
        ]
    )

    mapped_gene_hash = dict(  
        [ 
            [i.Gene_id,''] for i in    mapped 
        ]
    )

    return mapped, mapped_ko_hash, mapped_gene_hash


function_cate = Ddict()
for key in pathway_cat:
    for key2 in pathway_cat[key]:
        function_cate[key2]= pathway_cat[key][key2]
detail = Ddict()
stats = {}

mapped_GeneKO,mapped_Ko_Id ,mapped_gene_Id = get_GeneIdAndKoid(2)

for each_cat in function_cate:
    all_pathway_sub = session.query(Pathway_Table).filter(
        Pathway_Table.Name.in_(
            function_cate[each_cat]
            )
        ).group_by(Pathway_Table.Id).subquery()
    
    
    Ko_subquery =  session.query( Association_Table ).join(all_pathway_sub,Association_Table.Pathway_Id==all_pathway_sub.c.Id).group_by(Association_Table.KO_Id).subquery()
    
    all_need = mapped_GeneKO.join(Ko_subquery,Gene_Ko_Table.Ko_id == Ko_subquery.c.KO_Id).group_by(Gene_Ko_Table.Gene_id)
    for each_data in all_need:
        detail[each_cat][each_data.Gene.Name]=""
END = open(sys.argv[2],'w')
END.write("Category\tGene\n")
END2 = open(sys.argv[3],'w')
END2.write("Category\tGene Number\n")
for key in detail:
    END2.write(key+'\t%s\n'%(  len(detail[key])    ))
    for key2 in detail[key]:
        END.write(key+'\t'+key2+'\n')


