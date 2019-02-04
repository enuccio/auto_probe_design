{\rtf1\ansi\ansicpg1252\cocoartf1504\cocoasubrtf830
{\fonttbl\f0\fmodern\fcharset0 Courier;\f1\fmodern\fcharset0 Courier-Bold;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;}
{\*\expandedcolortbl;;\csgray\c0;\csgray\c100000;}
\margl1440\margr1440\vieww18900\viewh16080\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## Automated probe design\
\
#### Protocol\
1.) Insert sequences into ARB tree.  Export Newick tree, using \'93name\'94 as the branch IDs.  Delete all the stuff at the top of the file enclosed by brackets [].  Your sequence names must be shorter than 16 characters.\
\
2.) Run TreeOTU on Newick tree. Tree OTU can be downloaded from [https://github.com/dongyingwu/TreeOTU]\
\
```\
perl 
\f1\b TreeOTU.pl
\f0\b0  -i mytree.tree -c 0.02 -o treeotu_output.txt\
```\
\
3.) Export ARB database in FASTA wide format.  Make a BLAST database from the ARB database.  Blast OTU or AMV sequences against ARB sequences.\
\
```\

\f1\b makeblastdb
\f0\b0  -dbtype 'nucl' -parse_seqids -in arb_database.fasta -input_type 'fasta' -out arb_database.db\
\

\f1\b blastn
\f0\b0  -db arb_database.db -query otus.fasta -outfmt '6' -max_target_seqs 2000 -perc_identity 97 > otu_blast_ARB.txt\
```\
\
4.) Build ARB PT server.  Note the line that the server is on for assign_otus_module.py\
\
\
5.) Generate ARB macro to design probes for each OTU or AMV, as well as a cluster of its nearest sequences in ARB (<97% similar by blast and within 0.02 tree distance units)\
-i tree OTU results\
-b blast results\
-pt line number of your PT server\
\
\
```\
python 
\f1\b \cf2 \cb3 \CocoaLigature0 assign_otus_module.py
\f0\b0 \cf0 \cb1 \CocoaLigature1  -i treeotu_output.txt -b otu_blast_ARB.txt --pt 7\
```\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf0 \
\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 ### 6.) Run Macro to generate probe files for each OTU or AMV.\
\
arb --execute otu_blast_ARB.amc arb_database.arb\
\
\
\
\
\
\
}