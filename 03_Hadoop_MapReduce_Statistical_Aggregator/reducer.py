import sys
n=s=ss=0
for line in sys.stdin:
    try: _,v=line.rstrip().split("\t"); c,a,b=map(int,v.split(","))
    except ValueError: continue
    n+=c; s+=a; ss+=b
if n: print(f"count={n} sum={s} sum_squares={ss} mean={s/n:.6f} population_variance={ss/n-(s/n)**2:.6f}")
