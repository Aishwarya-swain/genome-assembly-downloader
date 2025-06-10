# genome-assembly-downloader
Download genome assembly files (FASTA, GFF, GTF, GenBank, etc.) from NCBI using GCA or GCF accession IDs

# Genome Assembly Downloader

This repository contains a Python script that automatically downloads genome assembly files (FASTA, GTF, CDS, and protein) from NCBI using a list of GCA or GCF accession numbers.

## Features

- Accepts a list of NCBI GCA/GCF accession IDs
- Constructs the correct FTP path using accession format
- Downloads `.fna`, `.faa`, `.gtf`, and `.cds_from_genomic.fna` files
- Displays download progress using `tqdm`
- Organizes downloads into individual folders per genome

## Files Downloaded Per Genome

- `*_genomic.fna.gz` (nucleotide FASTA)
- `*_protein.faa.gz` (protein FASTA)
- `*_genomic.gtf.gz` (annotations in GTF format)
- `*_cds_from_genomic.fna.gz` (coding sequences)

##  Requirements

- Python 3.6+
- `requests`
- `tqdm`

## Input Format
The script expects each genome entry to be 
The full assembly name or label as provided in the NCBI FTP (e.g., GCF_004115265.2_mRhiFer1_v1.p)

### Customizing the Downloaded File Types
By default, the script downloads the following files for each genome:

    Genomic FASTA (_genomic.fna.gz)
    Protein FASTA (_protein.faa.gz)
    GTF annotation (_genomic.gtf.gz)
    CDS from genomic FASTA (_cds_from_genomic.fna.gz)

You can easily add or remove file types by editing this line in the script:

_file_types = ["_genomic.fna.gz", "_protein.faa.gz", "_genomic.gtf.gz", "_cds_from_genomic.fna.gz"]_
For example, to also download GenBank flat files (.gbff) and RNA sequences, update it as follows:
_file_types = ["_genomic.fna.gz", "_protein.faa.gz", "_genomic.gtf.gz", "_cds_from_genomic.fna.gz", "_genomic.gbff.gz", "_rna_from_genomic.fna.gz"]_

 %%% You can find the available file types for a specific assembly by visiting its NCBI FTP folder and inspecting the files listed there.


