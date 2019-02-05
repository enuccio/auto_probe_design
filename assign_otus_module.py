### Description: Script to combine treeOTUs and blast OTUs.  Will create ARB macro and necessary files for running ARB automated probe design
### Erin Nuccio, LLNL
### 10/16/18

from os import makedirs
from os.path import splitext, split, join, basename, dirname, isdir
from optparse import make_option, OptionParser



def parse_treeotu(newick_tree_file, output_fp):
    fh = open(newick_tree_file, "U")
    bname = basename(newick_tree_file)
    root, extension = splitext(bname)
    outfile_path = join(output_fp, root + "_parsed.txt")
    outfh = open(outfile_path, "w")

    results = fh.readline()

    splitresults = results.strip().split("\t")

    for idx, otulist in enumerate(splitresults):
        if idx == 0:
            continue
        else:
            otu_id = "treeotu_" + str(idx)
            [outfh.write(x +","+ otu_id +"\n") for x in otulist.split(",")]
    return outfile_path

def assign_otus(parsed_treeotu_filepath, blast_results_filepath):
    fh_treeotu = open(parsed_treeotu_filepath, "U")
    fh_blast = open(blast_results_filepath, "U")
    root = dirname(parsed_treeotu_filepath)
    bname = basename(blast_results_filepath)
    head, ext = splitext(bname)
    outfile_path = join(root, head + "_OTUs_mergelist.csv")
    

    outfile_otuid_path = join(root, head + "_OTUs.txt")
    outfh = open(outfile_path, "w")
    outfh_otu_ids = open(outfile_otuid_path, "w")
    
    #print "Location of mergelist for ARB: "
    #print outfile_path
    #print "Location of OTU IDs: "
    #print outfile_otuid_path

    extra_seq_ids = []
    all_arb_ids = []
    all_otu_ids = []
    otu_dict = {}

    for line in fh_treeotu: #arb_id,otu_id
        linestrip = line.strip().split(",")
        arb_id = linestrip[0].strip()
        otu_id = linestrip[1].strip()
        otu_dict[arb_id] = otu_id


    for line in fh_blast:
        linestrip = line.strip().split("\t")
        seq_id = linestrip[0]
        arb_id = linestrip[1]

        seq_treeotu_id = otu_dict[seq_id]
        try:
            arb_otu_id = otu_dict[arb_id]
        except KeyError:
            arb_otu_id = "unknown"
            print "Unknown key:", arb_id

        if ( seq_treeotu_id == arb_otu_id ) and ( arb_id not in all_arb_ids ):
            outfh.write(",".join([arb_id, arb_otu_id]) +"\n")
            all_arb_ids.append(arb_id)

            if arb_otu_id not in all_otu_ids:
                all_otu_ids.append(arb_otu_id)
                outfh_otu_ids.write(arb_otu_id + "\n")

    if ( seq_id not in all_arb_ids ) and ( seq_id not in extra_seq_ids ):
            extra_seq_ids.append(seq_id)
            print seq_id

    for x in extra_seq_ids: 
        outfh.write(",".join([x, otu_dict[x]]) +"\n")

    return outfile_otuid_path, outfile_path

def create_macro(otu_id_filepath, mergelist_filepath, template_filepath):
    template_path = template_filepath
    head, tail = split(otu_id_filepath)
    root, ext = splitext(tail)
    outfile_path = join(head, "create_probes_") + root + ".amc"
    outfh = open(outfile_path, "w")

    #print "Location of macro: "
    print outfile_path
    
    with open(template_path, "U") as fh:
        for line in fh:
            if "FILEPATH1" in line:
                correctline = line.replace("FILEPATH1", otu_id_filepath)
                #print otu_id_filepath
                outfh.write(correctline)
            elif "FILEPATH2" in line:
                correctline = line.replace("FILEPATH2", mergelist_filepath)
                #print mergelist_filepath
                outfh.write(correctline)
            elif "PTSERVER" in line:
                correctline = line.replace("PTSERVER", str(pt_server-1))
                outfh.write(correctline)
            else:
                outfh.write(line)
    outfh.close()
            
def main():
    # Change so these are input on the command line...
    parsed_treeotu_filepath = parse_treeotu(treeotu_fp, output_fp)
    otu_id_filepath, mergelist_filepath = assign_otus(parsed_treeotu_filepath, blast_fp)
    create_macro(otu_id_filepath, mergelist_filepath, template_filepath)

    
###### Set-up command line prompts

desc = "Parse TreeOTU results.  Combine TreeOTU and BLAST results, and generate AMC macro file for ARB (to assign OTUs to the cluster, only keep members of the TreeOTU that are 97% similar to the original sequence)"
usage = "Specify input directory path (-i), treeotu results, blast results, macro template, and line number of the PT server. Output path is optional(-o).  Example: python assign_otus_module.py -i treeotu_results.txt -b blast_results.txt -t macro_template.amc --pt 7"

parser = OptionParser(usage=usage, description=desc)
parser.set_defaults(verbose=True)
options = [make_option('-i','--treeotu_fp',type="string", help='[REQUIRED] The TreeOTU results filepath. '),
           make_option('-b', '--blast_fp',type="string",help='[REQUIRED] The Blast output from blasting sequences against Silva database'),
           make_option('-p','--pt',type="int", help='[REQUIRED] The line number of the PT server.  Go to the PT Server admin and determine which line the server is on.'),
           make_option('-t','--template_fp',type="string", help='[REQUIRED] The macro template filepath. ',
           make_option('-o','--output_fp',type="string", help='[OPTIONAL] The output filepath.  If not specified, will save to same folder as input.')]

parser.add_options(options)
opts,args = parser.parse_args()
treeotu_fp = opts.treeotu_fp
blast_fp = opts.blast_fp
pt_server = opts.pt
output_fp = opts.output_fp
template_filepath = opts.template_fp

#print "TESTTEST", output_fp
#print "test", pt_server

if treeotu_fp is None:
    parser.print_help()
    parser.error('***Must specify a TreeOTU results file!')

if blast_fp is None:
    parser.print_help()
    parser.error('***Must specify a Blast results file!')

if pt_server is None:
    parser.print_help()
    parser.error('***Must specify the line number of the PT Server in ARB using --pt!  Open PT server admin and determine which line the server is on.')
    
if template_filepath is None:
    parser.print_help()
    parser.error('***Enter path for macro template file')
    
if output_fp is None:
    output_fp = dirname(treeotu_fp)
else:
    try: 
        makedirs(output_fp)
    except OSError:
        if not isdir(output_fp):
            raise

#print "TEST", output_fp





######
    
if __name__ == "__main__":
    main()
