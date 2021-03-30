
disease<-"disease_hpo"
phen_R<-"phen_R"
hpo<-"terms"
disease_gene<-"disease_gene"
td<-"term_disease"

a<-read.table(disease, sep="\t", fill=TRUE)#test dataset
mylist <- list()
bb=1
while (bb<=nrow(a)){
  gg<-as.character(unlist(a[bb,2:ncol(a)]))
  jj<-as.character(a[bb,1])
  mylist[[jj]]<-gg
  bb=bb+1
}
disease<-lapply(mylist, function(x) x[nzchar(x)])

a<-read.table(td, sep="\t", fill=TRUE)#test dataset
mylist <- list()
bb=1
while (bb<=nrow(a)){
  gg<-as.character(unlist(a[bb,2:ncol(a)]))
  jj<-as.character(a[bb,1])
  mylist[[jj]]<-gg
  bb=bb+1
}
term_disease<-lapply(mylist, function(x) x[nzchar(x)])

a<-read.table(phen_R, sep="\t", fill=TRUE)#test dataset
mylist <- list()
bb=1
while (bb<=nrow(a)){
  gg<-as.character(unlist(a[bb,2:ncol(a)]))
  jj<-as.character(a[bb,1])
  mylist[[jj]]<-gg
  bb=bb+1
}
genes<-lapply(mylist, function(x) x[nzchar(x)])

termi<-read.table(hpo, sep="\t", fill=TRUE)#test dataset
hpo_terms<-termi$V1

a<-read.table(disease_gene, sep="\t", fill=TRUE)#test dataset
mylist <- list()
bb=1
while (bb<=nrow(a)){
  gg<-as.character(unlist(a[bb,2:ncol(a)]))
  jj<-as.character(a[bb,1])
  mylist[[jj]]<-gg
  bb=bb+1
}
disgen<-lapply(mylist, function(x) x[nzchar(x)])

save(hpo_terms, disease, genes, disgen, term_disease, file="hpodata.rda")