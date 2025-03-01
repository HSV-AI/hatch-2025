import os
import requests
from urllib.parse import urljoin
from tqdm import tqdm
from zipfile import ZipFile 

# Base URL from GitHub repository

BASE_URL = "https://doctoral.matinf.uj.edu.pl/database/dibas/"

# BASE_URL = "http://130.92.152.193/DIBaS/"  # Example, adjust based on latest source

# List of bacterial species and corresponding subdirectories

BACTERIAL_SPECIES = [
"Acinetobacter.baumanii",
"Actinomyces.israeli",
"Bacteroides.fragilis",
"Bifidobacterium.spp",
"Candida.albicans",
"Clostridium.perfringens",
"Enterococcus.faecium",
"Enterococcus.faecalis",
"Escherichia.coli",
"Fusobacterium",
"Lactobacillus.casei",
"Lactobacillus.crispatus",
"Lactobacillus.delbrueckii",
"Lactobacillus.gasseri",
"Lactobacillus.jehnsenii",
"Lactobacillus.johnsonii",
"Lactobacillus.paracasei",
"Lactobacillus.plantarum",
"Lactobacillus.reuteri",
"Lactobacillus.rhamnosus",
"Lactobacillus.salivarius",
"Listeria.monocytogenes",
"Micrococcus.spp",
"Neisseria.gonorrhoeae",
"Porfyromonas.gingivalis",
"Propionibacterium.acnes",
"Proteus",
"Pseudomonas.aeruginosa",
"Staphylococcus.aureus",
"Staphylococcus.epidermidis",
"Staphylococcus.saprophiticus",
"Streptococcus.agalactiae",
"Veionella"]

# Local directory to save dataset
DATASET_DIR = "../data/DIBaS_Dataset"

# Create dataset directory if it doesn't exist
os.makedirs(DATASET_DIR, exist_ok=True)

# Function to download images while ignoring SSL verification
def download_images(species_name):

    zip_url = urljoin(BASE_URL, f"{species_name}.zip")
    zip_filename = f"{species_name}.zip"

    zip_path = os.path.join(DATASET_DIR, zip_filename)
    extract_path = os.path.join(DATASET_DIR, species_name)

    if not os.path.exists(zip_path):
        try:
            response = requests.get(zip_url, verify=False, stream=True, timeout=60)  # Ignore SSL
            response.raise_for_status()


            # Save image
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Downloaded: {zip_filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {zip_url}: {e}")

    if not os.path.exists(extract_path):
        os.makedirs(extract_path, exist_ok=True)

        with ZipFile(zip_path) as zipped: 
            zipped.extractall(extract_path) 


# Download all bacterial species images
for species in tqdm(BACTERIAL_SPECIES, desc="Downloading DIBaS Dataset"):
    download_images(species)

# clean up one data directory:
if os.path.exists(DATASET_DIR + "/Acinetobacter.baumanii/Acinetobacter.baumanii"):
    os.rename(DATASET_DIR + "/Acinetobacter.baumanii/Acinetobacter.baumanii", DATASET_DIR + "/Acinetobacter.baumanii_1")

if os.path.exists(DATASET_DIR + "/Acinetobacter.baumanii_1"):
    os.rmdir(DATASET_DIR + "/Acinetobacter.baumanii")
    os.rename(DATASET_DIR + "/Acinetobacter.baumanii_1", DATASET_DIR + "/Acinetobacter.baumanii")


print("DIBaS Dataset download complete!")
