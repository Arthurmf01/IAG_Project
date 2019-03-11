#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as pg
import pandas as pd 
import pandas.io.sql as psql
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
import flask
import pandas as pd
import numpy as np
app = dash.Dash()
#%% COnnect to Post GRE Database 

conn = pg.connect(database="postgres", user = "postgres",password = "", host = "127.0.0.1", port = "5432")
print ("Opened database successfully")
df = pd.read_sql_query('select * from "Test1_1";', conn)
map_data=df

#%% Set Up Layout 

# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Each dot is an NYC Middle School eligible for SONYC funding',
    mapbox=dict(
        #accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)
        
#%% BUilding the App 
    

# Map + table + Histogram
html.Div(
    [
        html.Div(
            [
                dcc.Graph(id='map-graph',
                          style={'margin-top': '20'})
            ], className = "six columns"
        ),
        html.Div(
            [
                dt.DataTable(
                    rows=map_data.to_dict('records'),
                    columns=map_data.columns,
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='datatable'),
            ],
            #style=layout_right,
            className="six columns"
        ),
        html.Div(
            [
                dcc.Graph(id="histogram")
            ],className="twelve columns")
    ], className="row"
)

#%%
app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
