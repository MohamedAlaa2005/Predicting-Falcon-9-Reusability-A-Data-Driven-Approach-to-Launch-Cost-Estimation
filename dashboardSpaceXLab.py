import dash
import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Load and preprocess data
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Dash layout
app.layout = html.Div(children=[
    html.H1("SpaceX Launch Analysis Dashboard"),
    html.Div(dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a launch site",
        searchable=True
    )),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Div(dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={f"{k}":f"{k}" for k in range(0,10001,1000)},
        value=[0, 10000]
    )),
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])


@app.callback(
    [Output(component_id='success-pie-chart', component_property='figure'),
     Output(component_id='success-payload-scatter-chart', component_property='figure')],
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_charts(selected_site, payload_range):
    filtered_df = df

    if selected_site == 'ALL':
        pie_data = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        pie_chart = px.pie(pie_data, names='Launch Site', values='class',title="All Site")

        scatter_data = filtered_df[
            (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
            (filtered_df['Payload Mass (kg)'] <= payload_range[1])
            ]
        scatter_chart = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color="Booster Version Category")

        return pie_chart, scatter_chart
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        pie_data = filtered_df.value_counts('class').reset_index()
        pie_chart = px.pie(pie_data, names='class', values=0,title=f"{selected_site} Site")

        scatter_data = df[
            (df['Payload Mass (kg)'] >= payload_range[0]) &
            (df['Payload Mass (kg)'] <= payload_range[1])
            ]
        scatter_chart = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color="Booster Version Category")

        return pie_chart, scatter_chart


if __name__ == '__main__':
    app.run_server()


