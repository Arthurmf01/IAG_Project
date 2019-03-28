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
import os
import dash
import plotly.plotly as py
from plotly import graph_objs as go
#import math


#%% Connect to Post GRE Database 

#Activate this connection if you want to work online
#DATABASE_URL = os.environ['https://s3-eu-west-1.amazonaws.com/iag-test1/Test1.csv']
conn = pg.connect("postgres://tydzgthbfkifxy:58678ccbab767710674d5f5864118633bdcedaf676617ec4f5dd4475cd36d1bc@ec2-23-23-241-119.compute-1.amazonaws.com:5432/d3c492q00bssm9")
#Activate this connection if you want to work with the local PostGre Database (Localhost)
#conn = pg.connect(database="postgres", user = "postgres",password = "", host = "127.0.0.1", port = "5431")
print ("Opened database successfully")

df = pd.read_sql_query('select * from "Test1" limit 20;', conn)


#Reading Data from the database : return a  toble (key,value)




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

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("IAG FIRST DRAFT", className='app-title'),
            
            html.Div(
                html.Img(src='https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe-inverted.png',height="100%")
                ,style={"float":"right","height":"100%"})
            ],
            className="row header"
            ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height":"20","verticalAlign":"middle"},
                children=[
                    dcc.Tab(label="Overviews", value="opportunities_tab"),
                    dcc.Tab(label="IT's view", value="leads_tab"),
                    dcc.Tab(id="cases_tab",label="Business's views", value="cases_tab"),
                ],
                value="leads_tab",
            )

            ],
            className="row tabs_div"
            ),
       
                
        # divs that save dataframe for each tab
        html.Div(id="opportunities_df", style={"display": "none"}), # CEO tab df
        html.Div(id="leads_df", style={"display": "none"}), # Manager tab df
        html.Div(id="cases_df", style={"display": "none"}), # IT tabs df



        # Tab content
        html.Div(
            children=[
            html.Iframe(
            src = "//plot.ly/~arthur_mf/75.embed",
            style={"width":"500","height":"500","frameborder":"0"}),
            html.Iframe(
            src= "//plot.ly/~arthur_mf/77.embed",
            style={"width":"500", "height":"500","frameborder":"0", "scrolling":"no"}),
            html.Div(generate_table(df), 
            style={"margin-top": "5px","max-height": "350px","overflow-y": "scroll","padding": "8px","background-color": "white","border": "1px solid rgb(200, 212, 227)","border-radius": "3px",},
            ), 
        ],     
        id="tab_content", className="row", style={"margin": "2% 3%","margin-left":"0.5%"}),
        
        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)


if __name__ == '__main__':
    app.run_server(debug=True)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})






#%%
