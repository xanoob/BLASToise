#!/bin/bash
shopt -s nullglob

cat REF.txt

spfaa=''
rps=''
dir=''
type=''
folder=''
group=''
ext='faa'

usage() { echo -e "USAGE:\n -s flag process files from arCOG ftp to create .faa for each arCOG \n -r flag to create RPS database \n -d location of faa query \n -f flag to indicate location in -d is a directory, for processing multiple fasta files \n -t 'genome' or 'group' (ortholog family) \n -g name of group \n -e query file extension, default '.faa' \n -h help \n \n EXAMPLE: \n BLASToise.sh -s -r -d ../COGT/FAM1 -t group -g Mesophiles -e fa" 1>&2; exit 1; }

while getopts ":srhd:t:fg:e:" opt; do
	case $opt in
		s) spfaa='true' ;;
		r) rps='true' ;;
		h) usage ;;			
		d) dir="$OPTARG" ;;
		t) type="$OPTARG" ;;
		f) folder='true' ;;
		g) group="$OPTARG" ;;
		e) ext="$OPTARG" ;;
		\?) echo "Invalid option -$OPTARG. See -h for details" >&2
			exit 1 ;;
		:) echo "Option -$OPTARG requires an argument." >&2
			exit 1 ;;
	esac
done

if [ $OPTIND -eq 1 ]; then 
	echo "No options were passed, see -h for help/usage"
	exit 0
fi


if [ "$spfaa" = true ] ; then
	echo "Preprocessing ar14.arCOG.csv and ar14.arCOGdef.tab..."
	Rscript 01_dfpre.R
	echo "Done."
	
	mkdir arCOG_in
	mv *.tab arCOG_in
	mv *.csv arCOG_in

	echo "Creating fasta files for each arCOG. This will take a while..."
	python 02_split2faa.py
fi

if [ "$rps" = true ] ; then
	makeblastdb -in arCOG03201.faa -dbtype 'prot' -out decoyDB > temp.out
	
	echo "Creating alignments and PSSMs. This will take a while..."
	
	mkdir arCOG_aln_o
	for f in *.faa
	do
        name=`basename $f .faa`
        mafft --thread 32 --clustalout --anysymbol --auto --quiet "$f" > "$name.paln"
		sed -r "s/gi\|([0-9]+)\|ref{0,1}/$name\_\1/g" "$name.paln" > "$name.raln"
		python 03_randseqid.py -i "$name.raln" -o "$name.aln"
    	mv "$name.paln" arCOG_aln_o
    	rm "$name.raln"
    	psiblast -in_msa "$name.aln" -db decoyDB -out_pssm "$name.pssm" -outfmt 6 -comp_based_stats 0 > temp.out
	done
	
	mkdir arCOG_faa
	mv *.faa arCOG_faa
	
	mkdir arCOG_aln
	mv *.aln arCOG_aln 
	
	mkdir decoyDB
	mv decoyDB* decoyDB
		
	ls *.smp > arCOGdb.pn
	
	echo "Creating RPS-BLAST database 'arCOGdb'..."
	makeprofiledb -title arCOGdb -in arCOGdb.pn -out arCOGdb -scale 1 -dbtype 'rps' -index true > temp.out

	mkdir arCOG_pssms
	mv *.smp arCOG_pssms
	rm temp.out
fi

if [ "$folder" = true -a "$type" != genome ] ; then
	echo "-f flag is for supplying directory containing multiple genomes only"
	exit 0
fi


if [ "$type" = genome -a "$folder" = true ] ; then
	echo "Assigning arCOGs to genome CDS..."
	for x in "$dir"/*."$ext"
	do 
		name=`basename $x .$ext`
		echo "Processing $name ..."
    		rpsblast+ -db arCOGdb -query "$x" -out "$name.tab" -evalue 1e-05 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send qcovs evalue bitscore"
		python 04_getanno.py -i "$name.tab" -a arCOG_in/ar14_anno.tab -t single > "$name.anno"
	done
	echo "FINISHED!"
fi

if [ "$type" = genome -a "$folder" = false ] ; then
	echo "Assigning arCOGs to genome CDS..."
		name=`basename $dir .$ext`
		echo "Processing $name ..."
    		rpsblast+ -db arCOGdb -query "$dir" -out "$name.tab" -evalue 1e-05 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send qcovs evalue bitscore"
		python 04_getanno.py -i "$name.tab" -a arCOG_in/ar14_anno.tab -t single > "$name.anno"
	echo "FINISHED!"
fi



if [ "$type" = group -a "$group" != '' ] ; then
	echo "Assigning arCOGs to ortholog families..."
	mkdir "${group}_RPS"
	mkdir "${group}_anno"
	for x in "$dir"/*."$ext"
	do 
		name=`basename $x .$ext`
		echo "Processing $name ..."
    		rpsblast+ -db arCOGdb -query "$x" -out "$name.tab" -evalue 1e-05 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send qcovs evalue bitscore"
		python 04_getanno.py -i "$name.tab" -a arCOG_in/ar14_anno.tab -t "$type" > "$name.anno"
	done
	mv *.tab "${group}_RPS"
	cat *.anno > "${group}_anno.all"
	mv *.anno "${group}_anno"
	echo "FINISHED!"
	
fi

if [ "$type" = group -a "$group" = '' ] ; then
	echo "Please provide name for group with option -g."
	exit 0
fi
