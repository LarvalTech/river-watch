# Compares OPW staff-gauge LEVEL (waterlevel.ie, last ~5 weeks) with the Open-Meteo/GloFAS daily FLOW for the same days.
# OPW publishes level here, not flow, so this checks direction and timing, not absolute m3/s.
import csv,io,json,urllib.request,collections
def get(u): return urllib.request.urlopen(u).read().decode()
S={"Clonmel":("16011",52.375,-7.675),"Fermoy":("18107",52.125,-8.225),"Mallow":("18056",52.125,-8.625),"Bandon":("20001",51.775,-8.725),"Ennis":("27066",52.825,-9.025),"Athlone":("26027",53.425,-7.975)}
def rank(v):
    o=sorted(range(len(v)),key=lambda i:v[i]);r=[0]*len(v)
    for k,i in enumerate(o):r[i]=k
    return r
def spear(a,b):
    ra,rb=rank(a),rank(b);n=len(a);m=(n-1)/2
    return sum((x-m)*(y-m) for x,y in zip(ra,rb))/(sum((x-m)**2 for x in ra)**.5*sum((y-m)**2 for y in rb)**.5)
for t,(sid,la,lo) in S.items():
    rows=list(csv.DictReader(io.StringIO(get(f"https://waterlevel.ie/data/month/{sid}_0001.csv"))))
    d=collections.defaultdict(list)
    for r in rows:
        try:d[r['datetime'][:10]].append(float(r['value']))
        except:pass
    lv={k:sum(v)/len(v) for k,v in d.items() if len(v)>=20}
    fc=json.loads(get(f"https://flood-api.open-meteo.com/v1/flood?latitude={la}&longitude={lo}&daily=river_discharge&past_days=35&forecast_days=0"))['daily']
    fl=dict(zip(fc['time'],fc['river_discharge'])); days=sorted(set(lv)&set(fl))
    a=[lv[x] for x in days];b=[fl[x] for x in days]
    print(t,sid,len(days),"days; level %.2f-%.2f m; GloFAS %.1f-%.1f m3/s; Spearman %.2f"%(min(a),max(a),min(b),max(b),spear(a,b)))
