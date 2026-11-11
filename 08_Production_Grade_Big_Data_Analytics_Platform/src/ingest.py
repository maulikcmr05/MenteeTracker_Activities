import json,sys,time
from pathlib import Path
src=Path(sys.argv[1] if len(sys.argv)>1 else "data/events.jsonl")
out=Path(sys.argv[2] if len(sys.argv)>2 else "warehouse/events.jsonl")
out.parent.mkdir(parents=True,exist_ok=True); t=time.perf_counter(); n=0
with src.open() as a,out.open("a") as b:
    for line in a: b.write(json.dumps(json.loads(line))+"\n"); n+=1
print(f"records={n} elapsed_seconds={time.perf_counter()-t:.6f}")
