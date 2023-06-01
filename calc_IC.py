#Creates an updated version of the Information Content (IC) list
#based on the hpo.db package and the gene_to_phenotype file
#of the hpo site
#to run this script, please run get_ancestors.R first
#to create the ancestors_list file
#this script creates a table of IC that is posteriorly loaded
#by the script to run the phenotypic overlap
#Usage:
#python3.6 calc_IC.py gene_to_phenotype ancestors_list > IC_inhouse
#########################################
#Dependencies:
from sys import argv
import math
import subprocess


def read_disease_terms(infile):
	"""reads the gene to phenotype file,
	and saves the information as 
	dic[HP]=set([diseaseA, diseaseB...])
	retrives the dic and the number of annotated diseases"""
	f=open(infile)
	f.readline()
	dic={}
	dis_l=set()
	for i in f:
		line=i.split("\t")
		if line[2] not in dic:
			dic[line[2]]=set([line[8].strip()])
		else:
			dic[line[2]].add(line[8].strip())
		dis_l.add(line[8].strip())
	f.close()
	return dic

def count_diseases(infile):
	aa=set()
	f=open(infile)
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	f.readline()
	for i in f:
		line=i.split("\t")
		aa.add(line[0])
	f.close()
	return len(aa)
	
def read_ancestors(infile):
	"""reads the ancestors file. Creates and retrieves
	a dictionary as 
	dic[HP]=[HP_ancestor1, HP_ancestor2...]"""
	f=open(infile)
	dic={}
	key=""
	val=set()
	for i in f:
		if i.startswith("$"):
			key=i.split("`")[1]
		elif "[" in i and "NA" not in i:
			vv=i.split(" ")
			for el in vv:
				if "HP" in el:
					val.add(el.split('"')[1])
		else:
			dic[key]=val
			key=""
			val=set()
	f.close()
	return dic

def merge_ancestrals(dic_disease, dic_ancs):
	"""using the dics of HP-diseases, and HP ancestors,
	adds to each term the diseases annotated to their 
	child terms. Returns an updated dictionary of HP-disease"""
	terms=dic_disease.keys()
	new_dis={}
	for t in terms:
		diseases=dic_disease[t]
		ancestors=dic_ancs[t]
		if t not in new_dis:
			new_dis[t]=diseases
		else:
			new_dis[t]=new_dis[t].union(diseases)
		for ek in ancestors:
			if ek not in new_dis:
				new_dis[ek]=diseases
			else:
				new_dis[ek]=new_dis[ek].union(diseases)
	return new_dis
	
	
def calc_IC(new_dis, sz):
	"""reads the updated dic created by merge ancestrals
	and calculates the IC for each term. writes the list of
	ICs to a file"""
	to_zero=["HP:0000001","HP:0000005","HP:0000118","HP:0012823","HP:0032443","HP:0032223","HP:0040279"]
	print("termlist\tontology\tX0")
	for key,value in new_dis.items():
		if key in to_zero:
			print("\t".join([key,"PA","0"]))
		else:
			IC=-1*math.log(float(len(value))/sz)
			print("\t".join([key,"PA",str(IC)]))

dic_disease=read_disease_terms(argv[1])#gene_phenotype
sz=count_diseases(argv[2])#phenotype.hpoa
calc_IC(merge_ancestrals(dic_disease, read_ancestors(argv[3])),sz)#ancestors list


	
	
	
	
	
	
