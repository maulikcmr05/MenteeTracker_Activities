import sys
for line in sys.stdin:
    for t in line.split():
        try: n=int(t)
        except ValueError: continue
        print(f"all\t1,{n},{n*n}")
