from fastapi import FastAPI
import pyarrow.parquet as pq
import pyarrow as pa


synonyms = pq.read_table("/code/pubchem_synonyms.parquet", memory_map=True)
smiles = pq.read_table("/code/pubchem_smiles.parquet", memory_map=True)


app = FastAPI()


@app.get("/name-to-structure/{name}")
def n2s(name: str):
    res = synonyms.filter(pa.compute.equal(synonyms["synonym"], name.lower()))
    if not res:
        cid = None
    else:
        cid = res["cid"][0]
    if cid:
        res = smiles.filter(pa.compute.equal(smiles["cid"], cid))
    if not res:
        structure = None
    else:
        structure = res["SMILES"][0].as_py()
    return {"structure": structure}
