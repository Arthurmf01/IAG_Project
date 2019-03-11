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
import plotly.graph_objs as go

#%% Connect to Post GRE Database 

conn = pg.connect(database="postgres", user = "postgres",password = "", host = "127.0.0.1", port = "5432")
print ("Opened database successfully")
df = pd.read_sql_query('select * from "Test1_1";', conn)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#%% BUilding the App 

app.layout = html.Div(children=[
    html.H1('IAG PROJECT', style={'textAlign': 'center', 'color': '#7FDBFF'}),    
    html.H4(children='Test first table'), generate_table(df),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@app.callback(dash.dependencies.Output('display-value', 'children'), [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)





#%%
