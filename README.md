## Automated probe design

**Note: This protocol works with the most recent version of ARB.** Homebrew install ARB: https://github.com/arb-project/homebrew-arb


#### Protocol
1.) Insert sequences into ARB tree.  Export Newick tree, using “name” as the branch IDs.  Delete all the stuff at the top of the file enclosed by brackets [].  Your sequence names must be shorter than 16 characters.

2.) Run TreeOTU on Newick tree. TreeOTU can be downloaded from https://github.com/dongyingwu/TreeOTU

```
perl TreeOTU.pl -i mytree.tree -c 0.02 -o treeotu_output.txt
```

3.) Export ARB database in FASTA wide format.  Make a BLAST database from the ARB database.  Blast OTU or AMV sequences against ARB sequences.

```
makeblastdb -dbtype 'nucl' -parse_seqids -in arb_database.fasta -input_type 'fasta' -out arb_database.db

blastn -db arb_database.db -query otus.fasta -outfmt '6' -max_target_seqs 2000 -perc_identity 97 > otu_blast_ARB.txt
```

4.) Build ARB PT server.  Note the line that the server is on for assign_otus_module.py


5.) Generate ARB macro to design probes for each OTU or AMV, as well as a cluster of its nearest sequences in ARB (<97% similar by blast and within 0.02 tree distance units)
- -i tree OTU results
- -b blast results
- -pt line number of your PT server


```
python assign_otus_module.py -i treeotu_output.txt -b otu_blast_ARB.txt --pt 7
```


6.) Run Macro to generate probe files for each OTU or AMV.

```
arb --execute otu_blast_ARB.amc arb_database.arb
```





