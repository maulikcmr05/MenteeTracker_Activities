from pathlib import Path
import joblib,numpy as np
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
app=FastAPI(title="PCA API")
class Rows(BaseModel): rows:list[list[float]]
def train():
    x=np.random.default_rng(42).normal(size=(200,4)); s=StandardScaler().fit(x); m=PCA(n_components=2).fit(s.transform(x))
    Path("artifacts").mkdir(exist_ok=True); joblib.dump((s,m),"artifacts/pca.joblib"); return s,m
@app.on_event("startup")
def init(): app.state.bundle=joblib.load("artifacts/pca.joblib") if Path("artifacts/pca.joblib").exists() else train()
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/transform")
def transform(p:Rows):
    x=np.asarray(p.rows,float)
    if x.ndim!=2 or x.shape[1]!=4 or not np.isfinite(x).all(): raise HTTPException(422,"finite rows with four values required")
    s,m=app.state.bundle
    return {"coordinates":m.transform(s.transform(x)).tolist(),"variance_ratio":m.explained_variance_ratio_.tolist()}
