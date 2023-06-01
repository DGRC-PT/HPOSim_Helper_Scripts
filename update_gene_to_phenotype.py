from sys import argv
import obonet
import networkx
import urllib3
import ssl
import requests


class CustomHttpAdapter (requests.adapters.HTTPAdapter):
	# "Transport adapter" that allows us to use custom ssl_context.

	def __init__(self, ssl_context=None, **kwargs):
		self.ssl_context = ssl_context
		super().__init__(**kwargs)

	def init_poolmanager(self, connections, maxsize, block=False):
		self.poolmanager = urllib3.poolmanager.PoolManager(
			num_pools=connections, maxsize=maxsize,
			block=block, ssl_context=self.ssl_context)


def get_legacy_session():
	ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
	ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
	session = requests.session()
	session.mount('https://', CustomHttpAdapter(ctx))
	return session



def get_associated_diseases(gene_id):
	url="https://hpo.jax.org/api/hpo/gene/"+gene_id
	l=[]
	gg=get_legacy_session().get(url)
	ggg=gg.json()
	for el in ggg["diseaseAssoc"]:
		l.append(el["diseaseId"])
	return l

def read_disease(infile):
	disease={}
	f=open(infile)
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	for i in f:
		line=i.split("\t")
		if line[0] not in disease:
			disease[line[0]]=set([line[3]])
		else:
			disease[line[0]].add(line[3])
	f.close()
	return disease

def read_genes(infile):
	gg={}
	f=open(infile)
	f.readline()
	for i in f:
		line=i.split("\t")
		if line[0] not in gg and line[1]!="-":
			gg[line[0]]=line[1]
	f.close()
	return gg

def complete_gene_to_phenotype(genes, diseases):
	for el in genes:
		dd=get_associated_diseases(el)
		for ele in dd:
			for term in diseases[ele]:
				print("\t".join([el, genes[el], term, "0","0","0","0","0",ele]))

complete_gene_to_phenotype(read_genes(argv[1]), read_disease(argv[2]))
#python update_gene_to_phenotype.py new_gene_to_phenotype phenotype.hpoa



