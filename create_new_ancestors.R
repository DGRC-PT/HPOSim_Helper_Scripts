#########CREATES A MANIPULATED ANCESTORS RDATA FILE
#this script takes the HPOSim/HPO.db Ancestors environment variable
#and creates a new ancestors file that is limited to 4 levels above the term
#this ancestor data is used by the SVInterpreter overlap script.

library(HPO.db)
library(HPOSim)
.initialize()
combinemethod = "funSimMax"
method = "Resnik"
IC <- get("termIC", envir = HPOSimEnv)


getLevelForTerm <-function(term, comm){
	a=FALSE
	countp=1
	if (comm %in% term){
	countp=0}
	else{
	while (a==FALSE){
		ancestor<-unlist(getTermParents(term))
		if (comm %in% ancestor){
			a=TRUE
		}
		else{
			term<-ancestor
			countp=countp+1}
	}}
	return(countp)}


getAncestors()
ancestor <- get("Ancestors", envir = HPOSimEnv)
#new_list<-list()
#for (names in names(ancestor)){
#	fam<-c()
#	for (el in ancestor[[names]]){
#		lv=getLevelForTerm(names, el)
#		if (lv<=4){
#			fam<-c(fam,el)
#	ll<-list(names=fam)
#	new_list<-append(new_list,ll)}
#}}

new_list<-list()
for (namess in names(ancestor)){
        fam<-c()
        for (el in ancestor[[namess]]){
                lv=getLevelForTerm(namess, el)
                if (lv<=4){
                        fam<-c(fam,el)}}
        ll<-list(fam)
		names(ll)<-namess
        new_list<-append(new_list,ll)
}



save(new_list, file="new_ancestors.Rdata")
