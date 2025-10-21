import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup  # new dependency
###Download the genome files from the NCBI RefSeq assembly ID

# List of genome accessions (only GCF/GCA IDs)
accessions = [
    "GCF_022029035.1",
    "GCF_014673295.1",
    "GCF_001721585.1",
    "GCF_026192095.1",
    "GCF_031626575.1",
    "GCF_023554755.1",
    "GCF_031626515.1",
    "GCF_031626535.1",
    "GCF_023656405.1",
    "GCF_023656475.1",
    "GCF_023656445.1",
    "GCF_024198195.1",
    "GCF_032334565.1",
    "GCF_001756905.1",
    "GCF_001721545.1",
    "GCF_009695525.1",
    "GCF_004209795.1",
    "GCF_004295405.1",
]


# Root output folder
output_dir = "ncbi_genomes"
os.makedirs(output_dir, exist_ok=True)

BASE_FTP = "https://ftp.ncbi.nlm.nih.gov/genomes/all"

def download_file(url, dest):
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=8192), desc=f"Downloading {os.path.basename(dest)}"):
                if chunk:
                    f.write(chunk)
    else:
        print(f"⚠️ Failed to download: {url} (status {response.status_code})")

def get_ftp_path(accession):
    """Construct base FTP path from accession."""
    acc_core = accession.split("_")[1].split(".")[0]
    chunks = [acc_core[i:i+3] for i in range(0, len(acc_core), 3)]
    prefix = accession.split("_")[0]
    return f"{BASE_FTP}/{prefix}/{'/'.join(chunks)}"

def get_asm_name_from_listing(accession):
    """
    Look inside the folder listing and extract the correct ASM directory name.
    """
    base_path = get_ftp_path(accession)
    url = f"{base_path}/"
    print(f"Checking directory listing at: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f" Could not fetch directory listing for {accession}")
        return None

    # Parse HTML directory listing
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.text.strip("/") for a in soup.find_all('a') if a.text.startswith(accession)]
    if links:
        asm_name = links[0].split("_")[-1]
        print(f" Found assembly directory: {links[0]}")
        return links[0]
    else:
        print(f"⚠️ No ASM directory found for {accession}")
        return None

def download_genome_files(accession):
    """Download genome FASTA, CDS, GTF, etc., for a given accession."""
    asm_folder = get_asm_name_from_listing(accession)
    if asm_folder is None:
        print(f" Skipping {accession} (no ASM folder found)")
        return

    genome_dir = os.path.join(output_dir, accession)
    os.makedirs(genome_dir, exist_ok=True)

    ftp_path = f"{get_ftp_path(accession)}/{asm_folder}"

    file_types = ["_genomic.fna.gz", "_protein.faa.gz", "_genomic.gtf.gz", "_cds_from_genomic.fna.gz"]

    for suffix in file_types:
        file_name = asm_folder + suffix
        url = f"{ftp_path}/{file_name}"
        dest = os.path.join(genome_dir, file_name)
        print(f"Trying to download: {url}")
        download_file(url, dest)

# --- MAIN ---
for acc in accessions:
    print(f"\n=== Processing {acc} ===")
    download_genome_files(acc)


