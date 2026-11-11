import argparse
from pathlib import Path
import numpy as np,pandas as pd,matplotlib.pyplot as plt,tensorflow as tf
p=argparse.ArgumentParser(); p.add_argument("--csv",default="data/series.csv"); p.add_argument("--lookback",type=int,default=24); p.add_argument("--cell",choices=["LSTM","SimpleRNN"],default="LSTM"); p.add_argument("--units",type=int,default=32); p.add_argument("--epochs",type=int,default=20); p.add_argument("--out",default="artifacts"); a=p.parse_args()
s=pd.read_csv(a.csv).value.to_numpy("float32"); cut=int(.7*len(s)); vc=int(.85*len(s)); mean=s[:cut].mean(); std=s[:cut].std() or 1; z=(s-mean)/std
X=np.array([z[j-a.lookback:j] for j in range(a.lookback,len(z))]); y=z[a.lookback:]; ix=np.arange(a.lookback,len(z)); tr=ix<cut; va=(ix>=cut)&(ix<vc); te=ix>=vc
layer=getattr(tf.keras.layers,a.cell); m=tf.keras.Sequential([tf.keras.layers.Input((a.lookback,1)),layer(a.units),tf.keras.layers.Dense(1)]); m.compile("adam","mse")
h=m.fit(X[tr],y[tr],validation_data=(X[va],y[va]),epochs=a.epochs,verbose=0,callbacks=[tf.keras.callbacks.EarlyStopping(patience=4,restore_best_weights=True)])
pred=m.predict(X[te],verbose=0).ravel()*std+mean; actual=y[te]*std+mean; out=Path(a.out); out.mkdir(exist_ok=True); rmse=np.sqrt(np.mean((actual-pred)**2))
(out/"metrics.txt").write_text(f"RMSE={rmse:.6f}\nMAE={np.mean(np.abs(actual-pred)):.6f}\n")
pd.DataFrame({"index":ix[te],"actual":actual,"forecast":pred}).to_csv(out/"predictions.csv",index=False)
plt.plot(h.history["loss"],label="train"); plt.plot(h.history["val_loss"],label="validation"); plt.legend(); plt.savefig(out/"loss_curves.png"); plt.close()
plt.plot(ix[te],actual,label="actual"); plt.plot(ix[te],pred,label="forecast"); plt.legend(); plt.savefig(out/"forecast.png")
