from pathlib import Path
import math
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
OUT=Path(__file__).resolve().parent
(OUT/'maps').mkdir(exist_ok=True)
d=pd.read_csv(OUT/'data/dataset_part_2.csv')
sites=d.groupby('LaunchSite')[['Latitude','Longitude']].first()
def map_base(center,zoom):
 m=folium.Map(location=center,zoom_start=zoom,tiles='OpenStreetMap',control_scale=True)
 MousePosition().add_to(m)
 return m
def title(m,t,sub):
 m.get_root().html.add_child(folium.Element(f'<div style="position:fixed;top:12px;left:65px;z-index:9999;background:white;padding:14px 20px;font:18px Arial;box-shadow:0 1px 5px #aaa"><b>{t}</b><br><span style="font-size:14px">{sub}</span></div>'))
m=map_base([33,-98],4)
for name,row in sites.iterrows():
 folium.CircleMarker([row.Latitude,row.Longitude],radius=8,color='#0B49CB',fill=True,fill_opacity=.85,tooltip=name).add_to(m)
 folium.Marker([row.Latitude,row.Longitude],icon=folium.DivIcon(html=f'<div style="font:bold 14px Arial;background:white;width:150px;padding:4px">{name}</div>',icon_anchor=(-10,25 if name=='KSC LC 39A' else -5))).add_to(m)
title(m,'Falcon 9 launch sites','90 launches, 2010â€“2020 | Dataset site names retained')
m.save(OUT/'maps/launch_sites.html')
m=map_base([28.59,-80.62],11)
cluster=MarkerCluster(name='Launch outcomes').add_to(m)
for _,r in d.iterrows():
 folium.Marker([r.Latitude,r.Longitude],icon=folium.Icon(color='green' if r.Class else 'red',icon='ok' if r.Class else 'remove'),tooltip=f'Flight {r.FlightNumber}: {r.Date}, Class {r.Class}',popup=f'{r.LaunchSite}<br>{r.Outcome}<br>Payload: {r.PayloadMass:,.0f} kg').add_to(cluster)
title(m,'Launch outcomes by site','Green: Class 1 | Red: Class 0 | Click a cluster to separate overlapping launches')
folium.LayerControl().add_to(m)
m.save(OUT/'maps/launch_outcomes.html')
# Selected nearby map points. Straight-line distances, not surveyed nearest distances.
origin=sites.loc['CCAFS SLC 40'].tolist()
points={'Coastline sample':[28.5630,-80.5675], 'Road sample':[28.5631,-80.5829], 'Rail sample':[28.5721,-80.5854]}
def distance(a,b):
 p,q=map(math.radians,[a[0],b[0]]);dl=math.radians(b[1]-a[1]);dp=q-p
 return 6371*2*math.asin(math.sqrt(math.sin(dp/2)**2+math.cos(p)*math.cos(q)*math.sin(dl/2)**2))
m=map_base(origin,14)
folium.Marker(origin,tooltip='CCAFS SLC 40',icon=folium.Icon(color='blue')).add_to(m)
dist=[]
for (name,p),color in zip(points.items(),['blue','green','purple']):
 km=distance(origin,p);dist.append({'name':name,'latitude':p[0],'longitude':p[1],'km':km})
 folium.PolyLine([origin,p],color=color,weight=3,tooltip=f'{name}: {km:.2f} km').add_to(m)
 folium.CircleMarker(p,radius=5,color=color,fill=True).add_to(m)
 folium.Marker(p,icon=folium.DivIcon(html=f'<div style="font:14px Arial;background:white;width:170px;padding:4px">{name}: {km:.2f} km</div>',icon_anchor=(0,0))).add_to(m)
title(m,'CCAFS SLC 40 proximity','Approximate distance to selected map points, not minimum distance or safety clearance')
m.save(OUT/'maps/proximity.html')
