# Process and trim ar14.arCOG.csv and ar14.arCOGdef.tab from NCBI into friendlier tab-delimited format. These files should be in your path.
# Generates files called ar14_GI (containing arCOG and GI information) and ar14_anno (arCOG ID, category, annotation)

ar14_csv = read.csv("ar14.arCOG.csv", header=FALSE, stringsAsFactors=FALSE)
ar14_GI = ar14_csv[,c(3,7,9)]
ar14_GI = ar14_GI[which(ar14_GI$V7 != ""),]
write.table(ar14_GI, file="ar14_GI.tab", sep="\t", row.names=FALSE, col.names=FALSE)

ar14_def = read.csv("ar14.arCOGdef.tab", sep="\t", header=FALSE, stringsAsFactors=FALSE)
ar14_anno = ar14_def[,c(1,2,4)]
write.table(ar14_anno, file="ar14_anno.tab", sep="\t", row.names=FALSE, col.names=FALSE)