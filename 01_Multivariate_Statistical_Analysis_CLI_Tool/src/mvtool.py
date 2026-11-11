import argparse
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
p=argparse.ArgumentParser(); p.add_argument("csv"); p.add_argument("--out",default="artifacts"); a=p.parse_args()
o=Path(a.out); o.mkdir(parents=True,exist_ok=True)
x=pd.read_csv(a.csv).select_dtypes(include=[np.number]).dropna()
z=x.to_numpy(float); mu=z.mean(0); cov=np.cov(z,rowvar=False); d=z-mu
md2=np.einsum("ij,jk,ik->i",d,np.linalg.pinv(cov),d)
pd.DataFrame({"row":x.index,"mahalanobis_squared":md2,"distance":np.sqrt(np.maximum(md2,0))}).to_csv(o/"distances.csv",index=False)
pd.DataFrame(cov,index=x.columns,columns=x.columns).to_csv(o/"covariance.csv")
pd.plotting.scatter_matrix(x,figsize=(8,8),diagonal="hist"); plt.tight_layout(); plt.savefig(o/"matrix_scatter.png",dpi=140)
print("rows",len(x),"features",x.shape[1],"mean",mu.tolist())
