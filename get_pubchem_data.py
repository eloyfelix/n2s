import pandas as pd
import urllib.request
import os

urllib.request.urlretrieve(
    "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz",
    "CID-Synonym-filtered.gz",
)
urllib.request.urlretrieve(
    "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-SMILES.gz", "CID-SMILES.gz"
)

df = pd.read_csv(
    "CID-Synonym-filtered.gz",
    compression="gzip",
    sep="\t",
    names=["cid", "synonym"],
    engine="pyarrow",
)
df["synonym"] = df["synonym"].str.lower()
df.to_parquet("pubchem_synonyms.parquet")
os.remove("CID-Synonym-filtered.gz")

df = pd.read_csv(
    "CID-SMILES.gz",
    compression="gzip",
    sep="\t",
    names=["cid", "SMILES"],
    engine="pyarrow",
)
df.to_parquet("pubchem_smiles.parquet")
os.remove("CID-SMILES.gz")
