#!/usr/bin/env python

"""
This script takes a blast .xml file and parses it with the following format:
Query: QUERY_NAME
Length: XXX

Target: TARGET FUNCTION / ORGANISM (for blastp, at least)
Accession: TARGET ACCESSION
Alignment length: XX    Target length: XXX    Percent identity: XX    evalue: X.XXXX
Query start: XXX    Query end: XXX    Hit start: XXX    Hit end: XXX

For non-blastp versions, the script works fine, but the accession number is all screwed up.
"""

import sys

if len(sys.argv) != 2:
    print "Usage: parse_xml.py <blast_output.xml>\n"
    quit()

xml = open(sys.argv[1], "r")
out = open(sys.argv[1] + ".parsed", "w")

# This is the meat of the script. It just goes through the .xml file line by
# line, and prints the information for each query and each target sequence.
# Could be done more efficiently, but it works.
for line in xml:
    if line.startswith("  <Iteration_query-ID>"):
        new_query = True
        hit_number = 0
        start = line.find(">")
        end = line.rfind("<")
        query_number = line[start + 1:end]
    elif line.startswith("  <Iteration_query-def>"):
        start = line.find(">")
        end = line.rfind("<")
        query_name = line[start + 1:end]
    elif line.startswith("  <Iteration_query-len>"):
        start = line.find(">")
        end = line.rfind("<")
        query_length = line[start + 1:end]
    elif line.startswith("  <Hit_def>"):
        if "&gt" in line:
            hit_number += 1
            start = line.find(">")
            end = line.find("&")
            hit_funx = line[start + 1:end]
        elif "&gt" not in line:
            hit_number += 1
            start = line.find(">")
            end = line.rfind("<")
            hit_funx = line[start + 1:end]
    elif line.startswith("  <Hit_accession>"):
        start = line.find(">")
        end = line.rfind("<")
        hit_accession = line[start + 1:end]
    elif line.startswith("  <Hit_len>"):
        start = line.find(">")
        end = line.rfind("<")
        hit_length = line[start + 1:end]
    elif line.startswith("      <Hsp_query-from>"):
        start = line.find(">")
        end = line.rfind("<")
        query_start = line[start + 1:end]
    elif line.startswith("      <Hsp_query-to>"):
        start = line.find(">")
        end = line.rfind("<")
        query_end = line[start + 1:end]
    elif line.startswith("      <Hsp_hit-from>"):
        start = line.find(">")
        end = line.rfind("<")
        hit_start = line[start + 1:end]
    elif line.startswith("      <Hsp_hit-to>"):
        start = line.find(">")
        end = line.rfind("<")
        hit_end = line[start + 1:end]
    elif line.startswith("      <Hsp_evalue>"):
        start = line.find(">")
        end = line.rfind("<")
        evalue = line[start + 1:end]
    elif line.startswith("      <Hsp_identity"):
        start = line.find(">")
        end = line.rfind("<")
        hit_identity = line[start + 1:end]
    elif line.startswith("      <Hsp_align-len>"):
        start = line.find(">")
        end = line.rfind("<")
        alignment_length = line[start + 1:end]
        percent_identity = float(int(hit_identity)) / int(alignment_length) * 100
        if new_query == True:
            out.write("########################################\n%s: %s\n\
                       Length: %s\n\n" % (query_number, query_name, query_length))
            new_query = False
        out.write("Target %d: %s\nAccession: %s\nAlignment length: %s\tTarget \
                   length: %s\tPercent identity: %d\tevalue: %s\nQuery start: \
                   %s\tQuery end: %s\tHit start: %s\tHit end: %s\n\n" %
                  (hit_number, hit_funx, hit_accession, alignment_length,
                   hit_length, percent_identity, evalue, query_start, query_end,
                   hit_start, hit_end))


out.close()
xml.close()
