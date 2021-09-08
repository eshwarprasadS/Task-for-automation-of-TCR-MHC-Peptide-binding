#!/usr/bin/env python

"""
"""

__author__ = "Eshwar Prasad Sivaramakrishnan"
__email__ = "esivaram@usc.edu"

import os
import csv
from chimera import runCommand

# Mapping of 1-alphabet representation to 3-alphabet representation of amino acids
AMINO_MAPPING = {
    'A' : 'ala',
    'G' : 'gly',
    'I' : 'ile',
    'L' : 'leu',
    'P' : 'pro',
    'V' : 'val',
    'F' : 'phe',
    'W' : 'trp',
    'Y' : 'tyr',
    'D' : 'asp',
    'E' : 'glu',
    'R' : 'arg',
    'H' : 'his',
    'K' : 'lys',
    'S' : 'ser',
    'T' : 'thr',
    'C' : 'cys',
    'M' : 'met',
    'N' : 'asn',
    'Q' : 'gln'
}

# Names of Input files
file_name = "1bd2-ligand peptide-template.pdb"
reference_list = 'material for automation of TCR-MHC-peptide binding - synthesized peptides.csv'

# Core Function to mutate the 9 amino acids
def mutate_ligand(file_name, reference_list):
    
    # Finding all the 9-bp long synthesized peptides
    with open(reference_list) as csvfile:
        csvfile2 = csv.reader(csvfile)
        peptideList = list(filter(lambda p: len(p) == 9, [row[1] for row in list(csvfile2)[1:]]))

    # Mutating the 1bd2-ligand tax peptide
    with open(file_name) as f:

        runCommand("open " + file_name)

        for n,peptide in enumerate(peptideList):
            for i, char in enumerate(peptide):
                runCommand("swapaa {} #0:{}".format(AMINO_MAPPING[char],i+1))

            result1_name = "mutation_result_{}".format(n+1)
            result2_name = "mutation_result_{}_modified.pdb".format(n+1)
        
            runCommand("write format pdb #0 {}.pdb".format(result1_name))

            modify_pdb(result1_name, result2_name)

        runCommand("close all")

    # Closing Chimera once script runs to termination
    runCommand("stop now")

# Function to modify the result pdb file to have 'LIG', 'L', '1' 
def modify_pdb(pdb_file_name, result_name):
    with open(pdb_file_name + '.pdb') as pdbfile:
        filedata = pdbfile.readlines()

    for i, line in enumerate(filedata):
            if line[:4] == "ATOM" or line[:6] == "HETATM" or line[:3] == "TER":
                # Split the line according to PDB SPECIFIED FORMAT
                split_line = [line[:6], line[6:11], line[12:16], line[17:20], line[21], line[22:26], line[30:38], line[38:46], line[46:54], line[54:60], line[60:66], line[72:76], line[76:78]]
                split_line[3] = 'LIG'
                split_line[4] = 'L'
                split_line[5] = '   1'

                # Produce modified line according to exact PDB SPECIFIED FORMAT
                result_line = '{:<6}{:>5} {:>4} {:>3} {}{:>4}    {:>8}{:>8}{:>8}{:>6}{:>6}      {:<4}{:>2}\n'.format(*split_line)

                filedata[i] = result_line

    # Write modified line to new pdb file
    with open(result_name, 'w') as writefile:
        writefile.writelines(filedata)

# Driver Code
mutate_ligand(file_name, reference_list)