from sys import argv
import obonet
import networkx

def read_table(infile, a1, a2):
	f=open(infile)
	f.readline()
	dic={}
	for i in f:
		line=i.split("\t")
		if line[a1].strip() not in dic:
			dic[line[a1].strip()]=set([line[a2].strip()])
		else:
			dic[line[a1].strip()].add(line[a2].strip())
	f.close()
	bigger=check_bigger(dic)
	return dic, bigger


def check_bigger(dic):
	aa=0
	bb=""
	for key,value in dic.items():
		if len(value)>aa:
			bb=key
			aa=len(value)
	return bb


def write_dic(dic, bigger, outfile):
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
	id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
	out=open(outfile, "w")
	for el in id_to_name.keys():
		out.write(el+"\n")
	out.close()
			
#python3 convert_to_prepare_rda.py gene_to_phenotype.txt phen_R disease_hpo disease_gene terms term_disease
#write gene list 
dic, bigger=read_table(argv[1], 0, 2)
write_dic(dic,bigger, argv[2])
#write disease
dic, bigger=read_table(argv[1], 8, 2)
write_dic(dic,bigger, argv[3])
#write disease - gene
dic, bigger=read_table(argv[1], 8, 1)
write_dic(dic,bigger, argv[4])
#write terms
writerr(activate_obo(), argv[5])
#write terms-disease
dic, bigger=read_table(argv[1], 2, 8)
write_dic(dic,bigger, argv[6])
