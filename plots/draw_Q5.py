import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_Q5 import get_data_Q5

color = '#000000'
colors = 'reds'


def draw_map_vietnam_provinces(vietnam_geo,data):
    app = dash.Dash()

    categories = sorted(data.columns[2:])

    cat_options = []
    for cat in categories:
        cat_options.append({'label':cat,'value':cat})

    app.layout = html.Div([
        html.H2("Tương quan giữa mức lương và địa điểm làm việc",
                style={'text_align': 'center', 'font_weight': 'bold', 'font':'Arial', 'font_color': color}),

        dcc.Dropdown(id='job',
                    options=cat_options,
                    value=cat_options[0],
                    style={'width':'900px','border-radius': '10px','font':'Arial'}),
        
        dcc.Graph(id='graph', style={'width': '80%', 'margin': 'auto'})    
    ])


    @app.callback(Output('graph', 'figure'),Input('job', 'value'))
    def update_graph(selected_job):
        dff = data.copy()
        dff = dff[['Code',selected_job]]
        trace = go.Choroplethmapbox(
            geojson = vietnam_geo,
            featureidkey= 'properties.Code',
            locations = data["Code"],
            z = data.loc[0:, selected_job],
            hovertext = 'Province: ' + data['Provinces'],
            colorscale =colors,
            marker_opacity=0.9,
            marker_line_width=0.9,
            showscale=True
            )
        layout = go.Layout(
            height=900,
            width=900,  
            mapbox=dict(
                style='white-bg',
                center=dict(
                    lat=17,  
                    lon=106 
                ),
                zoom=4.5
            ),
    )
        return {
            'data': [trace],
            'layout': layout
        }
    return app
    
df = pd.read_csv('txl_data.csv')
df_code = pd.read_csv('provinces.csv')
vietnam_geo = json.load(open("vietnam_state.geojson","r"))
data=get_data_Q5(df,df_code)

draw_map_vietnam_provinces(vietnam_geo,data).run_server()