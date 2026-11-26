import json,urllib.request,datetime as dt,time
import numpy as np
T={"Clonmel":("Suir",52.375,-7.675),"Fermoy":("Blackwater",52.125,-8.225),"Mallow":("Blackwater",52.125,-8.625),"Bandon":("Bandon",51.775,-8.725),"Enniscorthy":("Slaney",52.525,-6.575),"Ennis":("Fergus",52.825,-9.025),"Athlone":("Shannon",53.425,-7.975),"Carrick-on-Shannon":("Shannon",53.925,-8.075)}
TOWN_CENTRE={"Clonmel": [52.355, -7.703], "Fermoy": [52.1385, -8.2745], "Mallow": [52.135, -8.642], "Bandon": [51.745, -8.74], "Enniscorthy": [52.501, -6.558], "Ennis": [52.844, -8.98], "Athlone": [53.4235, -7.94], "Carrick-on-Shannon": [53.946, -8.09]}
out={}
for t,(riv,la,lo) in T.items():
    u=f"https://flood-api.open-meteo.com/v1/flood?latitude={la}&longitude={lo}&daily=river_discharge&start_date=2016-01-01&end_date=2025-12-31"
    for k in range(4):
        try: d=json.load(urllib.request.urlopen(u));break
        except Exception as e: time.sleep(10)
    days=d["daily"]["time"];v=np.array([np.nan if x is None else x for x in d["daily"]["river_discharge"]])
    ok=~np.isnan(v);p95,p99=np.percentile(v[ok],[95,99])
    ev={}
    for y in range(2016,2025):
        s=dt.date(y,10,1);e=dt.date(y+1,3,31);n=0;prev=False
        for i,ds in enumerate(days):
            D=dt.date.fromisoformat(ds)
            if s<=D<=e:
                hi=ok[i] and v[i]>=p99
                if hi and not prev:n+=1
                prev=hi
        ev[f"{y}/{str(y+1)[2:]}"]=n
    vals=list(ev.values())
    out[t]={"town_lat":TOWN_CENTRE[t][0],"town_lon":TOWN_CENTRE[t][1],"river":riv,"lat":d["latitude"],"lon":d["longitude"],"requested_lat":la,"requested_lon":lo,"days":int(ok.sum()),"missing":int((~ok).sum()),"mean":round(float(v[ok].mean()),2),"median":round(float(np.median(v[ok])),2),"max":round(float(v[ok].max()),1),"p95":round(float(p95),2),"p99":round(float(p99),2),"events_by_winter":ev,"events_total":sum(vals),"first4":sum(vals[:4]),"last4":sum(vals[-4:])}
    print(t,out[t]["lat"],out[t]["lon"],out[t]["days"],out[t]["mean"],out[t]["p95"],out[t]["p99"],out[t]["events_total"],out[t]["first4"],out[t]["last4"])
json.dump({"period":"2016-01-01 to 2025-12-31","source":"Open-Meteo Flood API (GloFAS v4 reanalysis), CC BY 4.0","percentile_method":"linear interpolation (numpy default) over all daily values","computed":dt.date.today().isoformat(),"towns":out},open("data/history_summary.json","w"),indent=1)
