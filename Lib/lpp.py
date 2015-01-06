#!/usr/bin/env python3
#coding=utf-8
#Producer=LPP
import re
import glob,os,sys,gzip
from collections import defaultdict
from xml.dom.minidom import parse
from codecs import open
import string,shutil
#class SmithWaterman():
	#"""docstring for SmithWaterman
	#seq1 需要比对的第一个序列
	#seq2 需要比对的第二个序列
	#使用align方法进行比对
	#而后score属性是每一个比对的打分

	#"""
	#def __init__(self, seq1, seq2):
		#self.seq1 = seq1
		#self.seq2 = seq2
		#self.subs_matrix = [[5, -4, -4, -4,-4], [-4, 5, -4, -4,-4], [-4, -4, 5, -4,-4], [-4, -4, -4, 5,-4],[  -4, -4, -4, -4,-4    ]]
		#self.m = len(seq1)
		#self.n = len(seq2)
		#self.gap_penalty = -4
		#self.max_score = 0
		##the DP table
		#self.score = numpy.zeros((self.m+1, self.n+1))
		##to store the traceback path
		#self.pointer = numpy.zeros((self.m+1, self.n+1))
		#self.align1, self.align2 = '',''
		#self.create_dp_and_pointers()

	#def create_match_score(self, alpha, beta):
		#"""get match/dismatch score from subs_matrix"""
		#alphabet={}
		#alphabet["A"] = 0
		#alphabet["C"] = 1
		#alphabet["G"] = 2
		#alphabet["T"] = 3
		#alphabet["N"] = 4
		#lut_x=alphabet[alpha]
		#lut_y=alphabet[beta]
		#return self.subs_matrix[lut_x][lut_y]

	#def create_dp_and_pointers(self):
		##calculate DP table and mark pointers
		#for i in range(1,self.m+1):
			#for j in range(1,self.n+1):
				#score_up = self.score[i-1][j] + self.gap_penalty;
				#score_down = self.score[i][j-1] + self.gap_penalty;
				#score_diagonal = self.score[i-1][j-1] + \
				    #self.create_match_score(self.seq1[i-1],self.seq2[j-1]);
				#self.score[i][j] = max(0, score_up, score_down, score_diagonal)
				#if self.score[i][j] == 0:
					##0 means end of the path
					#self.pointer[i][j] = 0;
				#if self.score[i][j] == score_up:
					##1 means trace up
					#self.pointer[i][j] = 1; 
				#if self.score[i][j] == score_down:
					##2 means trace left
					#self.pointer[i][j] = 2;
				#if self.score[i][j] == score_diagonal:
					##3 means trace diagonal
					#self.pointer[i][j] = 3;
				#if self.score[i][j] >= self.max_score:
					#self.max_i, self.max_j= i, j
					#self.max_score = self.score[i][j]

	#def trace_back(self):
		#while self.pointer[self.max_i][self.max_j]!=0:
			#if self.pointer[self.max_i][self.max_j]==3:
				#self.align1 = self.align1 + self.seq1[self.max_i-1];
				#self.align2 = self.align2 + self.seq2[self.max_j-1];
				#self.max_i -= 1;
				#self.max_j -= 1;
			#elif self.pointer[self.max_i][self.max_j] == 2:
				#self.align1 = self.align1 + '-'
				#self.align2 = self.align2 +self.seq2[self.max_j - 1]
				#self.max_j -= 1
			#elif self.pointer[self.max_i][self.max_j] == 1:
				#self.align1 = self.align1 + self.seq1[self.max_i - 1]
				#self.align2 = self.align2 + '-'
				#self.max_i -= 1

	#def align(self):
		#self.trace_back()
		#align1, align2 = self.align1[::-1], self.align2[::-1]
		#i, j = 0, 0
		#symbol=''
		#found, self.score = 0, 0
		#identity, similarity=0, 0
		#for i in range(0, len(align1)):
			##if two AAs are the same, then output the letter
			#if align1[i] == align2[i]:
				#symbol = symbol + align1[i];
				#identity += 1
				#similarity += 1
				#self.score += self.create_match_score(align1[i],align2[i])
			##if there are mismatches
			#elif align1[i] != align2[i] and '-' not in [align1[i], align2[i]]:
				#self.score += self.create_match_score(align1[i],align2[i])
				## add mismatching base character
				#symbol = symbol + '*'
				#found = 0
			##if one of them is a gap, output a space
			#elif '-' in [align1[i], align2[i]]:
				#symbol += '-'
				#self.score += self.gap_penalty
		#if align1 == 0:
			#self.identity = 0
		#else: 
			#self.identity = float(identity)/len(align1)*100
		#if align2 ==0:
			#self.similarity = 0
		#else:
			#self.similarity = float(similarity)/len(align2)*100;
		##print 'Identity =', "%3.3f" % self.identity, 'percent';
		##print 'Similarity =', "%3.3f" % self.similarity, 'percent';
		##print 'Score =', self.score;
		##print align1
		##print symbol
		##print align2


def Get_Path( path ):
	if not os.path.exists(path):
		
		os.makedirs( path )

def complement( char ):
	char = re.sub( '\s+','',char  )

	libary=string.maketrans('atcgATCG','tagcTAGC')
	end = char[::-1].translate(libary)
	return end
class fastq_check( object ):
	class NotFastqError(  ValueError ):
		pass
	def __init__( self,file_handle ):
		assert isinstance(  file_handle, file ),'The paramater input must be a File Handle'
		self.linenumber = 0
		self.filename = file_handle.name
		self.file_handle = iter( file_handle  )
		for line in self.file_handle:
			self.linenumber+=1
			if line[0]=='@':
				self.define=line

				break
	def __iter__( self ):
		return self
	def next(self):
		if not self.define:
			self.define=self.file_handle.next()
			self.linenumber+=1
		name = self.define
		seq = self.file_handle.next()
		self.linenumber+=1
		define2 = self.file_handle.next()
		self.linenumber+=1
		quality = self.file_handle.next()
		self.linenumber+=1
		self.define = ''

		if name [1:] == define2[1:]:
			return ( name,seq,define2,quality  )
		else:
			error_message = ' the File %s of  line %s  is not fastq format!!!!  '%( self.filename , self.linenumber-3)  
			raise self.NotFastqError, error_message
class Ddict(defaultdict,dict):
	def __init__(self):
		defaultdict.__init__(self, Ddict)
	def __repr__(self):
		return dict.__repr__(self)
class File_dict(object):
	'''file_ddict(file_TAG,options)   options=1,from 2 lines to start,
	oprions=0 from the first to start
	'''
	def __init__(self,FILE_HANDLE,OPTIONS=0):
		self.__FILE=FILE_HANDLE
		self.__OPTIONS=OPTIONS
		self.__HASH={}
		for i in range(0,self.__OPTIONS):
			self.file.next()
	def read(self,NUMBER_1,NUMBER_2):
		assert isinstance(NUMBER_1,int);assert isinstance(NUMBER_2,int)
		for _line in self.__FILE:
			line_list =_line[:-1].split('\t')
			_1_list= line_list[ NUMBER_1-1 ].split(';')   
			for element in _1_list:
				self.__HASH[element.strip()]=line_list[NUMBER_2-1].strip()
		self.__FILE.seek(0,0)
		return self.__HASH
class File_Ddict(object):
	'''file_ddict(file_TAG,options)   options=1,from 2 lines to start,
	oprions=0 from the first to start
	'''
	@staticmethod
	def check( cache_hash ):
		cache_exec = {'':''}
		def creep( i ):
			cache_new = {}
			for j in cache_hash[i]:
				for each_key in cache_exec:
					cache_new[ each_key+'[ key_%s_%s ]'%(i,j) ]=''
			return cache_new
		for i in sorted( cache_hash ):
			cache_exec = creep( i )
		return cache_exec 
	def __init__(self,_file,options=0,separate=';'):
		assert isinstance(options,int)
		self.file=iter(_file)
		self.separate=separate
		for i in range(0,options):
			self.file.next()
		self.hash=Ddict()
	'''number_1 the first value's number '''   		
	def read(self,*number_list):
		number_list=[key1-1 for key1 in number_list]
		for key1 in  number_list:
			assert isinstance(key1,int)
		for line in self.file:
			line_l = line.replace('\n','').split('\t')
			cache_hash=Ddict()
			i=0
			for each_number in number_list:
				j=0
				if  not self.separate:
					line_l_cache = line_l[ each_number ]
				else:
					line_l_cache = line_l[ each_number ].split(self.separate)
				for each_key in line_l_cache:
					exec(  'key_%s_%s = each_key'%( i,j )  )
					cache_hash[i][j]=''
					j=j+1
				i=i+1
			for key1 in self.check( cache_hash ):
				exec( 'self.hash%s=\'\''%( key1 ) )

		return self.hash
class block_reading(object):
	def __init__(self,file_handle,tag):
		self.file=iter(file_handle)
		self.tag=tag
	def __iter__(self):
		return self
	def next(self):
		self.container=[]
		for line in self.file:
			if re.match(self.tag,line):
				break
			elif line=='\n' or line=='\r\n':
				continue
			else:
				self.container.append(line)
		self.container=''.join(self.container)
		if not self.container:
			raise StopIteration
		return self.container
class fasta_check(object):
	def __init__(self,file_handle):
		assert isinstance( file_handle,file ),'The Input paramater must be a File Handle'
		self.file=iter(file_handle)
		for line in self.file:
			if line[0]=='>':
				self.define=line
				break
	def __iter__(self):
		return self
	def next(self):
		if not self.define:
			raise StopIteration

		name=self.define
		self.define=''        
		s=[]
		for line in self.file:
			if line[0]!='>':
				s.append(line)
			else:
				self.define=line
				break
		s=''.join(s)
		return (name,s)
def static(RAW):
	dom=parse(RAW)
	all_kinds_element=[]
	elements_list=dom.documentElement.childNodes
	element={}
	length=len(elements_list)
	for k in range(1,length):
		element_name=elements_list.item(k).nodeName
		element[element_name]=''
	del element['#text']
	return element,dom
def kill(name):
	import re
	name=re.sub('#','',name)
	name=re.sub('\t',';',name)
	name=re.sub('\n',';',name)
	return name
def getx(node):
	if node.hasAttribute('rdf:ID'):
		name=node.getAttribute('rdf:ID')
		name=name.replace('\n','')
	elif node.hasAttribute('rdf:resource'):
		name=node.getAttribute('rdf:resource')
		name=name.replace('\n','')
	else:
		try:
			name=node.childNodes.item(0).data
		except:
			name=''
	name=kill(name)
	return name
def extract(element,dom):
	for node in element:
		file=re.sub('bp:','',node)
		FILE=open(file+'.txt','wb','utf-8')        
		one_node=dom.getElementsByTagName(node)
		grid_hash={}
		grid=[]
		for one_element in one_node:
			try:
				child_nodes=one_element.childNodes
			except:
				continue
			length=len(child_nodes)
			for i in range(1,length):
				if child_nodes.item(i).nodeName!='#text':
					grid_hash[child_nodes.item(i).nodeName]=''
		for key in grid_hash:
			grid.append(key)
		grid.sort()
		tittle_length=len(grid)
		FILE.write('id')
		for i in range(0,tittle_length):
			kk=re.sub('bp:','',grid[i])
			kk=re.sub('\n','',kk)
			FILE.write('\t'+kk)
			grid_hash[grid[i]]=i
		FILE.write('\n')
		for one_element in one_node:
			local_hash={}
			try:
				child_nodes=one_element.childNodes
			except:
				continue
			node_id=getx(one_element)
			length=len(child_nodes)
			for i in range(1,length):
				element_id=child_nodes.item(i).nodeName
				try:
					attr=getx(child_nodes.item(i))
					attr=re.sub('\n','',attr)
				except:
					attr=''
				attr=kill(attr)
				if element_id in local_hash:
					local_hash[element_id]=local_hash[element_id]+';'+attr
				else:
					local_hash[element_id]=attr
			output={}
			character=[]
			for key1 in local_hash:
				for key2 in grid_hash:
					if key1==key2:
						output[grid_hash[key1]]=local_hash[key1]
			for key3 in grid_hash:
				if grid_hash[key3] not in output:
					output[grid_hash[key3]]='-'
			for i in  range(0,len(output)):
				character.append(output[i])
			end='\t'.join(character)
			end=re.sub('bp:','',end)
			end=re.sub('\n','',end)
			FILE.write(node_id+'\t'+end+'\n')
			del end
			del output
			del character
		FILE.close()
class dom_nomal_parse(object):
	def __init__(self,file_name,first_attribute='rdf:ID',secondary_attribute='rdf:resource',del_tag='bp:'):
		file_handle=open(file_name,'rU')
		nodes_list,dom=static(file_handle)
		self.nodes_list=nodes_list
		self.dom=dom
	def parse(self):
		STATIC=open('static.txt','wb')
		for el in self.nodes_list:
			element=self.dom.getElementsByTagName(el)
			node_length=len(element)
			node_length=str(node_length)
			name=el.replace('bp:','')
#            STATIC.write(name+'\t'+node_length+'\n')
		end=extract(self.nodes_list,self.dom)
'''______________________________humancyc parse____________________________________________________________'''
def manipulate(file):
	def static(dom):
		hash={}
		children=dom.childNodes
		for child in children:
			if child.nodeType==1:
				if child.hasAttribute('rdf:ID'):
					hash[child.nodeName]=0
				hash.update(static(child))
		return hash
	def extract(name,dom,FILE):
		total=[]
		tittle=[]
		tittle_hash={}
		grid_hash={}
		control=0
		def getx(node):
			try:
				attr1=node.getAttribute('rdf:ID')
			except:
				attr1=''
			try:
				attr2=node.getAttribute('rdf:resource')
			except:
				attr2=''
			try:
				attr3=node.childNodes.item(0).data
			except:
				attr3=''
			attr=attr1+attr2+attr3
			attr=re.sub('\n','',attr)
			attr=re.sub('\s\s+','',attr)
			attr1=re.sub('\s','',attr)
			try:
				name=node.nodeName
			except:
				name=''
			if attr1=='':
				try:
					attr=getx(node.childNodes.item(1))
				except:
					attr=''
			else:
				pass
			attr=kill(attr)
			return attr
		def kill(character):
			character=re.sub('\n',';',character)
			character=re.sub('\t',';',character)
			character=re.sub('#','',character)
			return character
		total_element=dom.getElementsByTagName(name)
		for element in total_element:
			if element.hasAttribute('rdf:ID') and element.hasChildNodes:
				one_all_child=element.childNodes
				for one_child in one_all_child:
					tittle_name=one_child.nodeName
					tittle_name=kill(tittle_name)
					if tittle_name not in tittle_hash and tittle_name!='/text':
						tittle_hash[tittle_name]=''
						tittle.append(tittle_name)
		tittle.sort()
		for i in range(0,len(tittle)):
			grid_hash[tittle[i]]=i
		tittle_name='\t'.join(tittle)
		tittle_name=re.sub('text','',tittle_name)
		tittle_name=re.sub('bp:','',tittle_name)
		FILE.write('id'+'\t'+tittle_name+'\n')
		for element in total_element:
			location_hash={}
			if element.hasAttribute('rdf:ID'):
				one_all_child=element.childNodes
				e_name=element.getAttribute('rdf:ID')
				e_name=kill(e_name)
				e_name=re.sub('bp:','',e_name)
				FILE.write(e_name)
				all_key=[]
				del all_key
				for one_child in one_all_child:
					if one_child.nodeType==one_child.ELEMENT_NODE:
						attr=getx(one_child)
						if one_child.nodeName in location_hash and len(location_hash[one_child.nodeName])>0:
							location_hash[one_child.nodeName]=location_hash[one_child.nodeName]+';'+attr
						else:
							location_hash[one_child.nodeName]=attr
				output={}
				for key1 in location_hash:
					for key2 in grid_hash:
						if key1==key2:
							output[grid_hash[key2]]=location_hash[key1]
				for key1 in grid_hash:
					if grid_hash[key1] not in output:
						output[grid_hash[key1]]='-'
				all_key=output.keys()
				sorted(all_key)
				for key1 in all_key:
					FILE.write('\t'+output[key1])
				FILE.write('\n')  
	dom=parse(file)
	all=static(dom)
	for element in all:
		file=re.sub('bp:','',element)
		nodes=dom.getElementsByTagName(element)
		for node  in nodes:
			if node.hasAttribute('rdf:ID'):
				all[element]=all[element]+1
		FILE=open(file+'.txt','wb','utf-8')
		extract(element,dom,FILE)
class dom_confusing_parse(object):
	def __init__(self,file_name):
		self.file_name=file_name
	def parse(self):
		manipulate(self.file_name)
class blast_parse(object):
	def __init__(self,blast_file,output_file):
		self.input=iter(block_reading(blast_file,'\s+<Iteration>'))
		self.output=output_file
	def parse(self):
		self.tag=0
		for key1 in self.input:
			if '<Hit>' not in key1:
				continue
			accession='\t'.join( re.findall('<Iteration_\S+?>([^<\n]+)',key1,re.M) )
			for key2 in re.split('</?Hit>',key1):
				if '<Hit_num>'  in key2:
					modules=re.split('</?Hsp>',key2)      
					title=re.findall('<([^>]+)>([^<\n]+)',modules[0],re.MULTILINE)
					head=accession+'\t'+'\t'.join([keym[1] for keym in title])
					if self.tag==0:
						title_out=['Iteration_iter-num','Iteration_query-ID','Iteration_query-def','Iteration_query-len']
						title_out.extend([keym[0] for keym in title])
					for key4 in modules[1:]:
						if '<Hsp_num>' not  in key4:
							continue
						data_all=re.findall('<([^>]+)>([^<\n]+)',key4,re.MULTILINE)
						if self.tag==0:
							title_out.extend([keym[0] for keym in data_all if keym[0]!='Hsp_gaps'])
							self.output.write('\t'.join(title_out)+'\n')
						self.output.write(head+'\t'+'\t'.join([key3[1] for key3 in data_all if key3[0]!='Hsp_gaps'])+'\n')
						self.tag=1

class EMBL_nul_seq(object):
	@classmethod
	def complement(cls,char):
		libary=','.maketrans('atcgATCG','tagcTAGC')
		return char[::-1].translate(libary)
	def getx(self,raw_list):
		[input_data,protein_id] = raw_list
		data_list = input_data.split(',')
		seq_slice=''
		for data in data_list:
			all_loc = re.search('(\d+)\.\.(\d+)',data)
			start = int(all_loc.group(1))-1
			end = int(all_loc.group(2))
			cache_slice = self.seq[start:end]
			if data.startswith('complement('):
				cache_slice = self.complement(cache_slice)
			seq_slice+=cache_slice
		seq_slice = re.sub('(\w{60})(?!\Z)','\\1\n',seq_slice)
		return '>'+protein_id+'\n'+seq_slice+'\n'
	def retrieve_seq(self, data_list ):
		data = map(self.getx,data_list)
		return(''.join(list(data)))
	def __init__(self,s_file):
		self.file  = block_reading(s_file,tag='//')
	def __iter__(self):
		return self
	def next(self):
		block  = self.file.next()
		if not block:
			raise StopIteration
		seq = re.search('\nSQ   [^\n]+\n([^/]+)',block).group(1)
		self.seq = re.sub('\W+|\d+','',seq)
		cds_all = re.findall('\nFT   CDS             ([^/]+).+?\nFT                   /protein_id="(\S+)"',block)
		fasta_end = self.retrieve_seq(cds_all)
		return fasta_end
class uniprot_parse(object):
	@classmethod
	def seq_manup(cls,seq):
		seq = re.sub('\W+','',seq)
		seq = re.sub('(\w{60})',r'\1\n',seq)
		return seq
	def __init__(self,files,tag ):
		self.file  = iter(block_reading( open(files,'rU') ,tag ='//'))
		self.tag =tag
	def __iter__(self):
		return self
	def next(self):
		block = self.file.next()
		if not block:
			raise StopIteration


		oc = re.search('\nOC   ([^\n]+)',block).group(1)
		if self.tag not in oc:
			self.next()
		else:
			uni_id = re.search('ID   (\S+)',block).group(1)
			uni_ac = re.search('\nAC   ([^\n]+)',block).group(1)
			uni_ac_list = uni_ac.split(';')
			uni_ac = ' ;'.join([key1.strip()    for key1 in uni_ac_list if key1.strip()])
			taxon = re.search('NCBI_TaxID=(\d+)',block).group(1)
			seq = re.search('\nSQ   SEQUENCE [^\n]+\n([^/]+)',block).group(1)
			seq = self.seq_manup(seq)+'\n'
			self.id = uni_id
			self.ac = uni_ac
			self.taxon = taxon
			self.seq = seq
		return self
class GBK_nul_seq(object):
	@classmethod
	def complement(cls,char):
		libary=','.maketrans('atcgATCG','tagcTAGC')
		return char[::-1].translate(libary)
	def getx(self,raw_list):
		[(input_data,protein_id)] = raw_list
		data_list = input_data.split(',')
		seq_slice=''
		for data in data_list:
			all_loc = re.search('(\d+)\.\.(\d+)',data)
			start = int(all_loc.group(1))-1
			end = int(all_loc.group(2))
			cache_slice = self.seq[start:end]
			if data.startswith('complement('):
				cache_slice = self.complement(cache_slice)
			seq_slice+=cache_slice
		seq_slice = re.sub('(\w{60})(?!\Z)','\\1\n',seq_slice.upper())
		return '>'+protein_id+'\n'+seq_slice+'\n'
	def retrieve_seq(self, data_list ):
		data = map(self.getx,data_list)
		return(''.join(list(data)))
	def __init__(self,s_file):
		self.file  = block_reading(s_file,tag='//')
	def __iter__(self):
		return self
	def next(self):
		block  = self.file.next()
		if not block:
			raise StopIteration
		seq = re.search('\nORIGIN\s+\n([^/]+)',block).group(1)
		self.seq = re.sub('\W+|\d+','',seq)

		cds_all = re.findall('\n(\s+CDS             .+?)\n     \w+',block,re.DOTALL)
		cds_all = [re.findall('\s+CDS\s+([^/]+).+?/protein_id="(\S+?)"',x,re.DOTALL)     for x in cds_all] 
		fasta_end = self.retrieve_seq(cds_all)
		return fasta_end
def get_taxon_seed( taxon_number ):
	all_end={}
	def creeper(taxon_number):
		if taxon_number in all_spieces:
			all_end[ taxon_number ]=''
			for key1 in all_spieces[ taxon_number ]:
				creeper(key1)
	creeper(taxon_number)
	return all_end