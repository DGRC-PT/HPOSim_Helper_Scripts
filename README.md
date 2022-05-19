# HPOSim_Helper_Scripts

## Helper scripts to create state-of-the-art HPO.db R package and hpodata.rda file, needed to run HPOSim

HPOSim is an R package used to calculate similarities between sets of HPO terms. For that, it needs the HPO.db R package, and the hpodata.rda files, that are not updated since 2017, leaving several HPO terms and disease-gene-term associations out of the analysis.

Here we designed scripts to create updated versions of these packages, allowing HPOSim to perform searches with state of the art data.

## hpodata.rda creation

### **Pre-requisites**
* Python 3
* Python 3 [sys module](https://docs.python.org/3/library/sys.html)
* Python 3 [obonet module](https://pypi.org/project/obonet/)
*  Python 3 [networkx module](https://networkx.org/)
* State-of-the-art genes_to_phenotype.txt annotation file from [HPO](https://hpo.jax.org/app/download/annotation)
* [R](https://www.r-project.org/)

### Walk-through

1. Download the genes_to_phenotype.txt file from HPO website
2. Run:

    `python3 convert_to_prepare_rda.py genes_to_phenotype.txt phen_R disease_hpo disease_gene terms term_disease`

    (phen_R, disease_hpo, disease_gene, terms, and term_disease are output files)

3. Run the R-script make_RDA.R on the same directory where the previously output files are located, or change their paths on the R-script. **The output of this script will be the  hpodata.rda file.** 


## HPO.db creation

### **Pre-requisites**

* Python 3
* Python 3 [sys module](https://docs.python.org/3/library/sys.html)
* Python 3 [obonet module](https://pypi.org/project/obonet/)
*  Python 3 [networkx module](https://networkx.org/)
* Python 3 [sqlite3 module](https://docs.python.org/3/library/sqlite3.html)
* State-of-the-art HPO.obo ontology file from [HPO](https://hpo.jax.org/app/download/ontology)
* The old version of [HPO.db](https://sourceforge.net/projects/hposim/)
* [R](https://www.r-project.org/)


### Walk-through

**Since we are only updating the data used by the package, in this walk-through its explained how to update the sqlite file of the package, leaving the rest untouched**

1. Download the HPO.obo file from the HPO website
2. Download the old version of HPO.db from the website
3. Run:

    `python3 obo2sqlite.py hp.obo`

    (This command will create a sqlite database, with the name HPO.sqlite)

4. Decompress the HPO.db file downloaded on point 2
5. Make a copy of the HPO.db directory found inside the HPO.db compressed file
6. Navigate inside this folder to the location of the sqlite file ( inst/extdata) 
7. Replace the old sqlite file by the new, script-created, sqlite file. Make sure that the new file have exactly the same name of the file being replaced
8. Close the folder and compress it with tar.gz:

    `tar -czvf HPO.db_2.0.tar.gz HPO.db` 

9.Now, the package can be installed on R, as ay other locale package:

    (Inside R)
    `install.packages("/path to folder with the package/HPO.db_2.0.tar.gz", repos = NULL, type = "source")` 
    
## Update the Information content (IC) data

By default, even with the update of HPO.db, HPOSim seems to maintain its default IC data. 
To surpass this, we developed a workaround, to create a table of ICs that can be easily loaded when using HPOSim.
The IC of each term here is calculated as indicated by [Köhler et al, 2009](https://pubmed.ncbi.nlm.nih.gov/19800049/) : the negative natural logarithm of the ratio between the number of diseases annotated with the term and the total of anotated diseases.

### Walk-through

1. First, to create the list of each term's ancestors, run the Rscript:

    `Rscript get_ancestors.R` 

2. Then, using as input the genes_to_phenotype.txt file and the ancestors files created on the first step, run:

    `python3.6 calc_IC.py gene_to_phenotype ancestors_list > IC_inhouse` 

This will create a file "IC_inhouse" that can be load into HPOSim in replacement of their normal IC environmental variable.

    (Inside R)
    #Instead of 
    `IC <- get("termIC", envir = HPOSimEnv)`
    #Use
    `IC<-read.table("IC_inhouse", header = TRUE, stringsAsFactors = FALSE)`


## Create a manipulated Ancestors file (Optional)
One must want to create an manipulator ancestors RDAta file to run SVInterpreter. This manipulated ancestors file, provides the ancestors of each term until 4 levels above.
To create this file, the above steps must be performed first.
Then:

`Rscript create_new_ancestors.R`

This will create a file - new_ancestors.Rdata - that must be loaded to R for use. after load, the containing data is under the list variable "new_list".


## Notes

* After this process, one can normally install HPOSim and use it: HPO.db is already installed on the system, and the rda file is directly called on the script
* This was designed as a "workaround" method to use HPOSim with state of the art data, nothing more. Nevertheless, its fair to assume that other uses of HPO.db package may  also work
* These scripts were developed on the context of a larger tool, for the analysis of structural Variants - [SVInterpreter](https://dgrctools-insa.min-saude.pt/cgi-bin/SVInterpreter.py)
