#!/usr/bin/env python
#coding=UTF-8
import obonet
import networkx
from sys import argv
import sqlite3
from sqlite3 import Error


def activate_obo():
	"""activate the API conection to the HPO database and returns
	the variable graph that is used for the explorattion of the ontology"""
	url='https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo'
	graph = obonet.read_obo(url)
	return graph


def get_offsprint(graph, child_term):
	"""uses the graph from activate_obo to get the superterms (parent_terms)
	of a child term. The terms are retrived in a set"""
	parent_terms=networkx.descendants(graph, child_term)
	return parent_terms

def make_hpo_offspring(graph, hpo_term):#os hpo_terms nao podem ter os obsoletos
	"""using the total list of terms from make_term_list, we get the
	superterms of each term. it returns a list as [[superterm, childterm],
	[superterm2, childterm]... the terms are represented by the sequential
	numbers given on make_term_list"""
	hpo_offspring=[]
	to_count=set()
	for key,value in hpo_term.items():
		to_write=get_offsprint(graph, key)
		for el in to_write:
			to_count.add(hpo_term[el][0])
			hpo_offspring.append([hpo_term[el][0], value[0]])
	return hpo_offspring, to_count


def make_term_list(graph):
	"""using obo graph, gets all the terms and respective descriptions. Returns
	a dictionary with the term, description and an assigned sequential number
	that is used to interconect tables: HP:XXXX:[1, description]"""
	id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
	hpo_term={}
	aa=1
	for key,value in id_to_name.items():
		hpo_term[key]=[aa, value]
		aa+=1
	return hpo_term


def make_hpo_obsolete(infile):
	"""using the obo file directly (the python library dont save obsoletes),
	makes a list of obsolete terms. this list is saved on a dictionary as
	HP:XXX:desc.Returns also an dictionary with the consider HPOs of
	the obsoletes. returns a dic with the obsolete term as key and a list of
	consider terms as value."""
	f=open(infile, encoding="UTF8")
	hpo_consider={}
	is_obsolte=False
	term=""
	desc=""
	consider=[]
	hpo_obsolete={}
	for i in f:
		if i.startswith("[Term"):
			if is_obsolte==True:
				hpo_obsolete[term]=desc
				if len(consider)!=0:
					hpo_consider[term]=consider
			is_obsolte=False
			term=""
			desc=""
			consider=[]
		if i.startswith("id:"):
			aa=i.split(" ")
			term=aa[1].strip()
		if i.startswith("name:"):
			aa=i.split(" ")
			desc=aa[1].strip()
		if i.startswith("is_obsolete"):
			is_obsolte=True
		if i.startswith("consider"):
			aa=i.split(" ")
			consider.append(aa[1].strip())
	if is_obsolte==True:
		hpo_obsolete[term]=desc
		if len(consider)!=0:
			hpo_consider[term]=consider
	f.close()
	return hpo_obsolete, hpo_consider

def make_parent_id(from_obsolete, graph, hpo_term):#hpo term que entra aqui ja tem de ter os obsoletos
	"""makes the hpo_parents dataset using the output from hpo term and obsolete. it returns a list of lists
	where each sublist is composed by 3 elements, the _Ids of the terms involved and the respective category"""
	hpo_parents=[]
	to_count=set()
	id_to_is_a = {id_: data.get('is_a') for id_, data in graph.nodes(data=True)}
	for key,value in id_to_is_a.items():
		if value!=None:
			to_count.add(hpo_term[key][0])
			for el in value:
				hpo_parents.append([hpo_term[key][0], hpo_term[el][0], "is_a"])
	for key,value in from_obsolete.items():
		to_count.add(hpo_term[key][0])
		for el in value:
			hpo_parents.append([hpo_term[key][0], hpo_term[el][0], "consider"])
	return hpo_parents, to_count


def make_synonym(graph, hpo_term):
	"""makes the synonym table with synonyms and the alternative
	IDs. returns a list of lists, where each sublist has all the elements
	of a line of the table."""
	hpo_syn=[]
	syn = {id_: data.get('synonym') for id_, data in graph.nodes(data=True)}
	for key,value in syn.items():
		if value!=None:
			for el in value:
				hpo_syn.append([hpo_term[key][0], el, "", 0])
	alt_id={id_: data.get('alt_id') for id_, data in graph.nodes(data=True)}
	for key,value in alt_id.items():
		if value!=None:
			for el in value:
				hpo_syn.append([hpo_term[key][0], el, el, 1])
	return hpo_syn


def mergeit(hpo_term, obsolete_term):
	aa=len(hpo_term)+1
	for key,value in obsolete_term.items():
		hpo_term[key]=[aa, value]
		aa+=1
	return hpo_term



def make_map_counts(hpo_term, hpo_obsolete, to_count_offspring, to_count_parent):
	"""make the map counts table, where the key of the dictionary is one column and
	the value is the other."""
	dic=[]
	dic.append(["TERM",len(hpo_term)])
	dic.append(["OBSOLETE",len(hpo_obsolete)])
	dic.append(["OFFSPRING", len(to_count_offspring)])
	dic.append(["CHILDREN", len(to_count_offspring)])
	dic.append(["PARENTS", len(to_count_parent)])
	dic.append(["ANCESTOR", len(to_count_parent)])
	return dic



def make_metadata():
	map_metadata=[]
	map_metadata.append(["TERM","Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	map_metadata.append(["OBSOLETE","Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	map_metadata.append(["OFFSPRING", "Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	map_metadata.append(["CHILDREN","Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	map_metadata.append(["PARENTS","Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	map_metadata.append(["ANCESTOR","Human Phenotype Ontology", "https://hpo.jax.org/", "20201012"])
	metadata=[]
	metadata.append(["HPOVERSION", "202010"])
	metadata.append(["HPOSOURCEDATE", "202010"])
	metadata.append(["HPOSOURCURL", "https://hpo.jax.org/"])
	metadata.append(["HPOSOURCENAME", "Human Phenotype Ontology"])
	metadata.append(["DBSCHEMAVERSION", "2.0"])
	metadata.append(["DBSCHEMA", "HPO_DB"])
	return map_metadata, metadata

###############SQLITE

def run_trans(tt, sql):
	"""
	Adds a set of entries to the database at the same time
	using transaction allows the addition of more entries 
	in a shorter time.
	"""
	sqliteConnection = sqlite3.connect('HPO.sqlite')
	cur = sqliteConnection.cursor()
	cur.execute('BEGIN TRANSACTION')
	for el in tt:
		cur.execute(sql, el)
	sqliteConnection.commit()
	cur.close()
	sqliteConnection.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
        
def create_bd():
    """creates the sqlite table
    with the fields bellow."""
    database = r"HPO.sqlite"
    sql_term_table = """ CREATE TABLE IF NOT EXISTS hpo_term (
                                        _id integer PRIMARY KEY,
                                        hpo_id VARCHAR(12) NOT NULL UNIQUE,
                                        term VARCHAR(255) NOT NULL
                                    ); """
    sql_syn_table = """ CREATE TABLE IF NOT EXISTS hpo_synonym (
                                        _id INTEGER NOT NULL,
                                        synonym VARCHAR(255) NOT NULL,
                                        secondary VARCHAR(12) NULL,
                                        like_hpo_id SMALLINT,
                                        FOREIGN KEY (_id) REFERENCES hpo_term (_id)
                                    ); """
    sql_parents_table = """ CREATE TABLE IF NOT EXISTS hpo_parents (
                                        _id INTEGER NOT NULL,
                                        _parent_id INTEGER NOT NULL, 
                                        relationship_type VARCHAR(7) NOT NULL,
                                        FOREIGN KEY (_id) REFERENCES hpo_term (_id),
                                        FOREIGN KEY (_parent_id) REFERENCES hpo_term (_id)
                                    ); """
    sql_off_table = """ CREATE TABLE IF NOT EXISTS hpo_offspring (
                                        _id INTEGER NOT NULL,
                                        _offspring_id INTEGER NOT NULL,
                                        FOREIGN KEY (_id) REFERENCES hpo_term (_id),
                                        FOREIGN KEY (_offspring_id) REFERENCES hpo_term (_id)
                                    ); """
    sql_obs_table = """ CREATE TABLE IF NOT EXISTS hpo_obsolete (
                                        hpo_id VARCHAR(12) PRIMARY KEY, 
                                        term VARCHAR(255) NOT NULL 
                                    ); """
    sql_mapcounts_table = """ CREATE TABLE IF NOT EXISTS map_counts (
                                        map_name VARCHAR(80) PRIMARY KEY,
                                        count INTEGER NOT NULL
                                    ); """
    sql_mapmetadata_table = """ CREATE TABLE IF NOT EXISTS map_metadata (
                                        map_name VARCHAR(80) NOT NULL,
                                        source_name VARCHAR(80) NOT NULL,
                                        source_url VARCHAR(255) NOT NULL,
                                        source_date VARCHAR(20) NOT NULL
                                    ); """
    sql_metadata_table = """ CREATE TABLE IF NOT EXISTS metadata (
                                        name VARCHAR(80) PRIMARY KEY,
                                        value VARCHAR(255)
                                    ); """
    # create a database connection
    conn = create_connection(database)
    create_table(conn, sql_term_table)
    create_table(conn, sql_syn_table)
    create_table(conn, sql_parents_table)
    create_table(conn, sql_off_table)
    create_table(conn, sql_obs_table)
    create_table(conn, sql_mapcounts_table)
    create_table(conn, sql_mapmetadata_table)
    create_table(conn, sql_metadata_table)

def write_hpo_term(hpo_term):
	sql = '''INSERT INTO hpo_term(_id, hpo_id, term) VALUES(?,?,?)'''
	trna=[]
	for key,value in hpo_term.items():
		t=[value[0], key, value[1]]
		trna.append(t)
		if len(trna)==100:
			run_trans(trna, sql)
			trna=[]
	if len(trna)!=0:
		run_trans(trna, sql)

def write_syn_par_term(term, sql):
	trna=[]
	for el in term:
		trna.append(el)
		if len(trna)==100:
			run_trans(trna, sql)
			trna=[]
	if len(trna)!=0:
		run_trans(trna, sql)

def write_obsolete(obs):
	sql = '''INSERT INTO hpo_obsolete(hpo_id, term) VALUES(?,?)'''
	trna=[]
	for key,value in obs.items():
		t=[key, value]
		trna.append(t)
		if len(trna)==100:
			run_trans(trna, sql)
			trna=[]
	if len(trna)!=0:
		run_trans(trna, sql)


def main(obo_file):
	graph=activate_obo()
	hpo_term=make_term_list(graph)#lista de termos iniciais sem os obsoletos
	hpo_obsolete, obs_consider=make_hpo_obsolete(obo_file)#sai o dicionario dos obsoletos como HP:desc, e o dicionario com os consider
	hpo_offspring, off_count=make_hpo_offspring(graph, hpo_term)#sai a lita de offspring e o numero de offspring
	hpo_syn=make_synonym(graph, hpo_term)#faz a lista de sinonimos
	hpo_term=mergeit(hpo_term, hpo_obsolete)#faz merge do hpo_term com o obsolete
	hpo_parent, parent_count=make_parent_id(obs_consider, graph, hpo_term)#faz o parent
	map_counts=make_map_counts(hpo_term, hpo_obsolete, off_count, parent_count)
	print(map_counts)
	map_metadata, metadata= make_metadata()#faz as tabelas de metadata
	print("data prepared!")
	#começa a escrever no sqlite
	#cria a bd
	create_bd()
	#escreve 
	print("database created! Writing....")
	write_hpo_term(hpo_term)
	print("a")
	sql = '''INSERT INTO hpo_synonym(_id, synonym, secondary, like_hpo_id) VALUES(?,?,?,?)'''
	write_syn_par_term(hpo_syn, sql)
	print("b")
	sql = '''INSERT INTO hpo_parents(_id, _parent_id, relationship_type) VALUES(?,?,?)'''
	write_syn_par_term(hpo_parent, sql)
	print("c")
	sql = '''INSERT INTO hpo_offspring(_id,_offspring_id) VALUES(?,?)'''
	write_syn_par_term(hpo_offspring, sql)
	print("d")
	write_obsolete(hpo_obsolete)
	print("e")
	sql = '''INSERT INTO map_counts(map_name, count) VALUES(?,?)'''
	write_syn_par_term(map_counts, sql)
	print("f")
	sql = '''INSERT INTO map_metadata(map_name, source_name, source_url, source_date) VALUES(?,?,?,?)'''
	write_syn_par_term(map_metadata, sql)
	print("g")
	sql = '''INSERT INTO metadata(name, value) VALUES(?,?)'''
	write_syn_par_term(metadata, sql)
	print("finished!")
	
main(argv[1])
