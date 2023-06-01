from sys import argv
import obonet
import networkx

def read_table(infile, a1, a2):
	"""creates dictionaries with the data from gene_to_phenotype
	returns the dictionary and the bigger number of collumns in the data
	to be correctly parsed later to R"""
	f=open(infile)
	f.readline()
	dic={}
	for i in f:
		if i.startswith("#")==False and i.startswith("datab")==False:
			line=i.split("\t")
			if line[a1].strip() not in dic:
				dic[line[a1].strip()]=set([line[a2].strip()])
			else:
				dic[line[a1].strip()].add(line[a2].strip())
	f.close()
	bigger=check_bigger(dic)
	return dic, bigger

def read_table_increment(infile, dic, is_omim_first):
	"""add to the lists the OMIM diseases with no associated gene
	using the file phenitype_annotation. The output is the incremented
	dictionary created by read_table"""
	f=open(infile)
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	for i in f:
		if i.startswith("OMIM"):
			line=i.split("\t")
			if is_omim_first==True:
				a=line[0]#"OMIM:"+line[1]
				b=line[3].strip() #line[4].strip()
			else:
				b=line[0]# "OMIM:"+line[1]
				a=line[3].strip()#line[4].strip()
			if a not in dic:
				dic[a]=set([b])
			else:
				dic[a].add(b)
	f.close()
	bigger=check_bigger(dic)
	return dic, bigger
	
def check_bigger(dic):
	"""returns the ID of the dic of the
	entry of the dic with more elements.
	This is needed to correctly input to rda
	file in the next step."""
	aa=0
	bb=""
	for key,value in dic.items():
		if len(value)>aa:
			bb=key
			aa=len(value)
	return bb


def write_dic(dic, bigger, outfile):
	"""write the output files"""
	out=open(outfile, "w")
	out.write(bigger+"\t"+"\t".join(list(dic[bigger]))+"\n")
	for key, value in dic.items():
		if key!=bigger:
			out.write(key+"\t"+"\t".join(list(value))+"\n")

def activate_obo():
	"""activate the API conection to the HPO database and returns
	the variable graph that is used for the explorattion of the ontology"""
	url='https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
	graph = obonet.read_obo(url)
	return graph

def writerr(graph, outfile):
	"""write activate obo"""
	id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
	out=open(outfile, "w")
	for el in id_to_name.keys():
		out.write(el+"\n")
	out.close()

def get_disease_list(infile):
	f=open(infile)
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	ll=set()
	for i in f:
		ll.add(i.split("\t")[0])
	f.close()
	return ll
	
#get_disease_gene(get_disease_list(phenotype_annotation), gene_to_phenotype_older)
			
#python3 convert_to_prepare_rda.py gene_to_phenotype.txt phen_R disease_hpo disease_gene terms term_disease phenotype_annotation.tab
#write gene list 
dic, bigger=read_table(argv[1], 0, 2)
write_dic(dic,bigger, argv[2])
#write disease
dic, bigger=read_table(argv[7], 0, 3)
dic, bigger=read_table_increment(argv[7], dic, True)
write_dic(dic,bigger, argv[3])
#write disease - gene
dic, bigger=read_table(argv[1], 8, 1)
write_dic(dic,bigger, argv[4])
#write terms
writerr(activate_obo(), argv[5])
#write terms-disease
dic, bigger=read_table(argv[7], 3, 0)#dic, bigger=read_table(argv[1], 2, 8)
dic, bigger=read_table_increment(argv[7], dic, False)
write_dic(dic,bigger, argv[6])
