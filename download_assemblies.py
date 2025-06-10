import os
import requests
from tqdm import tqdm

# List of genome accessions
accessions = [
  "GCF_004115265.1_mRhiFer1_v1.p", "GCF_022682495.2_HLdesRot8A.1",
    # Add more as needed]

# Root output folder
output_dir = "ncbi_genomes"
os.makedirs(output_dir, exist_ok=True)

# NCBI assembly FTP base
BASE_FTP = "https://ftp.ncbi.nlm.nih.gov/genomes/all"

def download_file(url, dest):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=8192), desc=f"Downloading {os.path.basename(dest)}"):
                if chunk:
                    f.write(chunk)
    else:
        print(f"Failed to download: {url}")

def get_ftp_path(accession):
    # Extract the numeric part from accession (e.g., 027563665)
    acc_core = accession.split("_")[1].split(".")[0]
    chunks = [acc_core[i:i+3] for i in range(0, len(acc_core), 3)]
    prefix = accession.split("_")[0]
    return f"{BASE_FTP}/{prefix}/{'/'.join(chunks)}/{accession}"

def download_genome_files(accession):
    # Create subfolder for this genome
    genome_dir = os.path.join(output_dir, accession)
    os.makedirs(genome_dir, exist_ok=True)

    ftp_path = get_ftp_path(accession)
    file_types = ["_genomic.fna.gz", "_protein.faa.gz", "_genomic.gtf.gz", "_cds_from_genomic.fna.gz"]  # Add .gtf.gz if needed

    for suffix in file_types:
        file_name = accession + suffix
        url = f"{ftp_path}/{file_name}"
        dest = os.path.join(genome_dir, file_name)
        print(f"Trying to download: {url}")
        download_file(url, dest)

# Download all genomes
for acc in accessions:
    download_genome_files(acc)
