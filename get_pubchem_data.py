import urllib.request
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import progressbar
import os


class MyProgressBar:
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def csv_to_parquet(csv_file, parquet_file):
    csv_stream = pd.read_csv(
        csv_file,
        compression="gzip",
        sep="\t",
        chunksize=100000,
        names=["cid", "value"],
    )
    parquet_schema = pa.schema([("cid", pa.int32()), ("value", pa.string())])
    parquet_writer = pq.ParquetWriter(parquet_file, parquet_schema)
    for chunk in csv_stream:
        if csv_file == "CID-Synonym-filtered.gz":
            chunk["value"] = chunk["value"].str.lower()
        table = pa.Table.from_pandas(chunk, schema=parquet_schema)
        parquet_writer.write_table(table)
    parquet_writer.close()


urllib.request.urlretrieve(
    "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz",
    "CID-Synonym-filtered.gz",
    MyProgressBar(),
)
csv_to_parquet("CID-Synonym-filtered.gz", "pubchem_synonyms.parquet")
os.remove("CID-Synonym-filtered.gz")


urllib.request.urlretrieve(
    "ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-SMILES.gz",
    "CID-SMILES.gz",
    MyProgressBar(),
)
csv_to_parquet("CID-SMILES.gz", "pubchem_smiles.parquet")
os.remove("CID-SMILES.gz")
