import dash
import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Load and preprocess data
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
# Dash layout
app.layout = html.Div(children=[html.H1("spaceX dashboard"),html.Div(dcc.Dropdown(id='1',options=[{'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'VAFB SLC-4E',
                                                                                                      'value': 'VAFB SLC-4E'},
                                                                                                     {
                                                                                                      'label': 'CCAFS SLC-40',
                                                                                                      'value': 'CCAFS SLC-40'} ],value='ALL', placeholder="place holder here",searchable=True)),
html.Div(dcc.Graph(id='e')),
html.Div(dcc.RangeSlider(id='id',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[0, 10000])),
            html.Div(dcc.Graph(id='m'))                ]
                      )
@app.callback([Output(component_id='e', component_property='figure'),Output(component_id='m', component_property='figure')],[Input(component_id='1', component_property='value'),Input(component_id='id', component_property='value')])
def getg(site,n):
    r=df

    if site=='ALL':
        f=r.groupby('Launch Site')['class'].sum().reset_index()
        fig=px.pie(f,names='Launch Site',values='class')
        h = df[df['Payload Mass (kg)'] >= n[0]]
        h = h[h['Payload Mass (kg)'] <= n[1]]
        fig2 = px.scatter(h, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig,fig2
    else:
        r = df[df['Launch Site'] == site]
        f = r.value_counts('class').reset_index()
        fig = px.pie(f, names='class', values=0)
        h=r
        h = h[h['Payload Mass (kg)'] >= n[0]]
        h = h[h['Payload Mass (kg)'] <= n[1]]
        fig2 = px.scatter(h, x='Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig,fig2

if __name__ == '__main__':
    app.run_server()
