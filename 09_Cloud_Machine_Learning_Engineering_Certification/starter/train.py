from pathlib import Path
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report
X,y=load_iris(return_X_y=True); a,b,c,d=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=500)); m.fit(a,c)
print("accuracy generated on run",accuracy_score(d,m.predict(b))); print(classification_report(d,m.predict(b)))
Path("artifacts").mkdir(exist_ok=True); joblib.dump(m,"artifacts/iris.joblib")
