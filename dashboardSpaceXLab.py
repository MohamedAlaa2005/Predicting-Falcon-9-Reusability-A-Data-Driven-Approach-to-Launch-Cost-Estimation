import dash
import pandas as pd
from dash import html, dcc, Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Load and preprocess data
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Dash layout
app.layout = html.Div(
    style={'font-family': 'Arial', 'background-color': '#f9f9f9', 'padding': '20px'},
    children=[
        html.H1("SpaceX Launch Analysis Dashboard", style={'text-align': 'center', 'color': '#2c3e50'}),

        html.Div(
            dcc.Dropdown(
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
                searchable=True,
                style={'width': '60%', 'margin': 'auto'}
            ),
            style={'margin-bottom': '30px'}
        ),

        html.Div(
            dcc.Graph(id='success-pie-chart'),
            style={'margin-bottom': '30px'}
        ),

        html.Div(
            children=[
                html.Label("Select Payload Range (kg):", style={'margin-right': '15px'}),
                dcc.RangeSlider(
                    id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0 kg', 2500: '2500 kg', 5000: '5000 kg', 7500: '7500 kg', 10000: '10000 kg'},
                    value=[0, 10000],
                    tooltip={"placement": "bottom", "always_visible": True},
                    style={'width': '80%', 'margin': 'auto'}
                )
            ],
            style={'margin-bottom': '30px', 'text-align': 'center'}
        ),

        html.Div(
            dcc.Graph(id='success-payload-scatter-chart'),
            style={'margin-bottom': '30px'}
        )
    ]
)


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
        pie_chart = px.pie(pie_data, names='Launch Site', values='class', title="Total Success Launches by Site")

        scatter_data = filtered_df[
            (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
            (filtered_df['Payload Mass (kg)'] <= payload_range[1])
            ]
        scatter_chart = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                                   title="Correlation between Payload and Success",
                                   labels={"class": "Success", "Payload Mass (kg)": "Payload Mass (kg)"})

        return pie_chart, scatter_chart
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        pie_data = filtered_df.value_counts('class').reset_index()
        pie_chart = px.pie(pie_data, names='class', values=0, title=f"Total Success Launches for {selected_site}")

        scatter_data = filtered_df[
            (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
            (filtered_df['Payload Mass (kg)'] <= payload_range[1])
            ]
        scatter_chart = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                                   title=f"Correlation between Payload and Success for {selected_site}",
                                   labels={"class": "Success", "Payload Mass (kg)": "Payload Mass (kg)"})

        return pie_chart, scatter_chart


if __name__ == '__main__':
    app.run_server()

