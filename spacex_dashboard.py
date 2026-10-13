"""Run from this directory: python spacex_dashboard.py"""
from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df=pd.read_csv(Path(__file__).parent/'data/dataset_part_2.csv')
df['Outcome label']=df['Class'].map({0:'Class 0',1:'Class 1'})
df['Block label']=df['Block'].astype(int).astype(str)
app=Dash(__name__)
app.layout=html.Div([
 html.H1('SpaceX Launch Records',style={'color':'#0B49CB','marginBottom':'6px'}),
 html.P('Falcon 9 course dataset · 90 launches · 2010–2020 · Class 1 includes controlled ocean outcomes'),
 html.Label('Launch site'),
 dcc.Dropdown(id='site',options=[{'label':'All sites','value':'ALL'}]+[{'label':x,'value':x} for x in sorted(df.LaunchSite.unique())],value='ALL',clearable=False),
 html.Div(id='summary',style={'fontSize':'20px','paddingTop':'14px'}),
 dcc.Graph(id='pie',style={'height':'330px'}),
 html.Label('Payload range (kg)'),
 dcc.RangeSlider(id='payload',min=0,max=16000,step=500,value=[0,16000],marks={x:f'{x:,}' for x in range(0,16001,4000)},tooltip={'placement':'bottom','always_visible':True}),
 dcc.Graph(id='scatter',style={'height':'340px'}),
 html.P('Source: IBM Applied Data Science Capstone, dataset_part_2.csv. Associations do not establish causes. Payload includes mean-imputed values.',style={'fontSize':'13px'})
],style={'fontFamily':'Arial','maxWidth':'1100px','margin':'20px auto','padding':'0 24px'})

@app.callback(Output('pie','figure'),Output('scatter','figure'),Output('summary','children'),Input('site','value'),Input('payload','value'))
def update(site,payload):
 selected=df if site=='ALL' else df[df.LaunchSite==site]
 if site=='ALL':
  values=selected.groupby('LaunchSite',as_index=False)['Class'].sum()
  pie=px.pie(values,names='LaunchSite',values='Class',title='Share of the 60 successful outcomes',color_discrete_sequence=['#0B49CB','#21a675','#f2a541'])
 else:
  values=selected.groupby('Outcome label').size().reindex(['Class 0','Class 1'],fill_value=0).reset_index(name='Count')
  pie=px.pie(values,names='Outcome label',values='Count',title=f'{site}: outcome ratio',color='Outcome label',color_discrete_map={'Class 0':'#d65f5f','Class 1':'#21a675'})
 pie.update_traces(textinfo='label+value+percent')
 filtered=selected[selected.PayloadMass.between(*payload)]
 scatter=px.scatter(filtered,x='PayloadMass',y='Class',color='Block label',hover_data=['LaunchSite','FlightNumber','Date','Outcome'],title=f'Payload and outcome: {payload[0]:,}–{payload[1]:,} kg ({len(filtered)} launches)',labels={'PayloadMass':'Payload (kg)','Class':'Outcome class','Block label':'Booster block'})
 scatter.update_traces(marker={'size':10,'opacity':.75})
 scatter.update_yaxes(tickvals=[0,1],ticktext=['Class 0','Class 1'],range=[-.18,1.18])
 for fig in [pie,scatter]:fig.update_layout(template='plotly_white',font={'family':'Arial','size':14},margin={'l':55,'r':25,'t':50,'b':45})
 summary=f'{site if site!="ALL" else "All sites"}: {len(selected)} launches, {selected.Class.sum()} Class 1 outcomes ({selected.Class.mean():.1%})'
 return pie,scatter,summary

if __name__=='__main__':app.run(debug=False,port=8051)
