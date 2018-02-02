#!/usr/bin/env python
""" This script takes the output of my 'parse.xml.py' script and outputs all of
the database sequences that had a blast hit. Also outputs a simple stats file
"""

import re
import sys

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print "Usage: retrieve_blast_hits.py <.xml.parsed file> <db fasta file> \
           <query fasta file (optional)>\n"
    quit()

queries = 0
hits_list = []
query_list = []
parsed_file = open(sys.argv[1], "r")

# This will read through the .xml.parsed file and retrieve all queries and targets
for line in parsed_file:
    if line.startswith("Query_"):
        regex = re.match("Query_\d+: (.*?)\n", line)
        query = regex.group(1)
        query_list.append(query)
        queries += 1
    if line.startswith("Target"):
        regex = re.match("Target.*?: (.*?)\n", line)
        hit = regex.group(1)
        hits_list.append(hit)
parsed_file.close()

hits_list = set(hits_list)

seqs_dict = {}
seqs_file = open(sys.argv[2], "r")

# This goes through the database fasta file and pulls out sequences that were BLASTED to
for line in seqs_file:
    if line.startswith(">"):
        regex = re.match(">(.*?)\n", line)
        header = regex.group(1)
        seqs_dict[header] = ""
    else:
        seqs_dict[header] += line[:-1]
seqs_file.close()

query_dict = {}

# This will go through the query file and pull out sequences that had a BLAST hit (optional)
if len(sys.argv) == 4:
    query_file = open(sys.argv[3], "r")
    for line in query_file:
        if line.startswith(">"):
            regex = re.match(">(.*?)\n", line)
            header = regex.group(1)
            query_dict[header] = ""
        else:
            query_dict[header] += line[:-1]
    query_file.close()

    out = open(sys.argv[1] + ".query_seqs", "w")
    for item in query_list:
        if item in query_dict:
            out.write(">%s\n%s\n" % (item, query_dict[item]))
    out.close()

out = open(sys.argv[1] + ".seqs", "w")

seqs_length = 0
lengths = []

# This writes the target sequences to a file (fasta format)
for item in hits_list:
    out.write(">%s\n%s\n" % (item, seqs_dict[item]))
    seqs_length += len(seqs_dict[item])
    lengths.append(len(seqs_dict[item]))
out.close()

lengths_sum = 0
lengths.sort(reverse = True)

# This just calculates the N50 of the target sequences
for item in lengths:
    lengths_sum += item
    if lengths_sum >= (0.5 * seqs_length):
        N50 = item
        break

# Writes a few stats to a file, mostly for fun
stats = open(sys.argv[1] + ".stats", "w")
stats.write("Total query sequences: %s\nTotal scaffolds: %s\nAverage scaffold\
             length: %s\nN50: %s\nTotal scaffold length: %s" % (queries,
              len(hits_list), (seqs_length / len(hits_list)), N50, seqs_length))
stats.close()
