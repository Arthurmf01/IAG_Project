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

df = pd.read_sql_query('select * from "Critical_Service_Availability2" limit 1000;', conn)

dff=pd.read_sql_query('select * from "Critical_Service_Availability2";', conn)
dff['year'] = pd.DatetimeIndex(dff['Date_raised']).year
dff['month'] = pd.DatetimeIndex(dff['Date_raised']).month


df = pd.read_sql_query('select "Incident_ID","Priority","CI_Name","Domain", "Service" from "Critical_Service_Availability2";', conn)
servAvail_df = pd.read_sql_query('select * from "ServAvailJF_1";', conn)

#%%
#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
    )

#Reading Data from the database : return a  toble (key,value)

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))])
#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True
#%% BUilding the App 

#%% Define value name for dropdown selection 
mgr_options=df["CI_Name"].unique()
mgr_options2=dff["Month "].unique()
mgr_options3=dff["Domain"].unique()
mgr_options4=dff["Service"].unique()



app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("", className='app-title'),
            
            html.Div(
                html.Img(src='https://s3-eu-west-1.amazonaws.com/iag-test1/test2.png',height="100%")
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
                    dcc.Tab(label="Critical Incident per Month", value="opportunities_tab"),
                    dcc.Tab(label="Critical Incident per Month", value="leads_tab"),
                    dcc.Tab(id="cases_tab",label="Critical Incident per Service", value="cases_tab"),
                ],
                value="leads_tab",
            )

            ],
            className="row tabs_div"
            ),
        # Tab content
        html.Div(
                 
        id="tabs-content-example", style={"margin": "2% 3%","margin-left":"0.5%"}),
        
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


#CALLBACKS SECTION 
#Callbacks for middle selector 

#updates middle indicator based on df updates
# @app.callback(
#     Output("table", "children"),
#     [Input("CI_Name", "value")],
# )
# def update_counter(ci_name):
#     print(ci_name)
#     count = pd.read_sql_query('SELECT COUNT("Incident_ID") FROM "Critical_Service_Availability";', conn)
#     open = len(count)
#     return open
            
# @app.callback(
#     Output("middle_leads_indicator", "children"), [Input('Month','value')]
# )
# def middle_leads_indicator_callback(month):
#     print(domain)
#     print(month)
#     #print(ci_name)
#     #input= dff[(dff['Month '] == month) & (dff['Domain'] == domain)]
#     #df = pd.read_json(df, orient="split")
#     if month == "All_Months":
#         c = len(dff[(dff["Priority"] == "Critical")].index)
#     else:
#         #a = len(dff[(dff["Domain"] == domain)].index)
#         #c = len(dff[(dff["Month "] == month)].index)
#         # c=a+b
#         c=len(dff.groupby([(dff["Domain"] == domain),(dff["Month "] == month)]).size())  
#     return c


@app.callback(
    Output("middle_leads_indicator", "children"), [Input('Month', 'value')]
)
def middle_leads_indicator_callback(ci_name):
    print(ci_name)
    #df = pd.read_json(df, orient="split")
    if ci_name == "All_Months":
        open_leads = len(
        dff[
            (dff["Priority"] == "Critical")
        ].index
    )
    else:
        open_leads = len(
        dff[
            (dff["Month "] == ci_name)
        ].index
    )
    
    return open_leads

#Callbacks for Application
@app.callback(
    dash.dependencies.Output('table', 'children'),
    [dash.dependencies.Input('Month', 'value')])
def update_graph(ci_name):
    if ci_name == "All_Months":
        a= df_plot = df.copy()
    else:
        df_plot = df[df["Month "] == ci_name]

    a = df_plot.loc[df_plot["Month "] == ci_name]

    return generate_table(a)

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    # TABS IT 
    if tab == 'leads_tab':
        return html.Div(
            [
                html.Div(
                    [
                # html.Div(
                #         #Dropdown Application
                #         dcc.Dropdown(
                #                         id="CI_Name",
                #                         options=[
                #                             {'label': i,'value': i} for i in mgr_options
                #                             ],
                #                         value='All Applications',
                #                         placeholder="Select an Applications",
                #                     ),
                #             className="two columns",
                # ), 
                        #Dropdown Day (Month only) 
                html.Div(
                        dcc.Dropdown(
                                        id="Month",
                                        options=[
                                            {"label": "All Months", "value": "All_Months"},
                                            {"label": "January", "value": "January"},
                                            {"label": "February", "value": "February"},
                                            {"label": "March", "value": "March"},
                                            {"label": "April", "value": "April"},
                                            {"label": "June", "value": "June"},
                                        ],
                                        
                                        # [
                                        #     {'label': i,'value': i} for i in mgr_options2
                                        #     ],
                                        placeholder="Select a Month",
                                    ),
                        dcc.Dropdown(
                                        id='dropdown-1',
                                        options=[{'label': i,'value': i} for i in mgr_options],
                                        value='All Applications'
                        ),
                            className="two columns",
                            style={"float": "left"},
                ),
                # html.Div(
                #         #Domain Application
                #         dcc.Dropdown(
                #                         id="Domain",
                #                         options=[
                #                             {"label": "All Domains", "value": "All_Domains"},
                #                             {"label": "Operations", "value": "OPERATIONS"},
                #                             {"label": "Airports", "value": "AIRPORTS"},
                #                             {"label": "Commercial", "value": "COMMERCIAL"},
                #                         ],                                 
                #                         # [
                #                         #     {'label': i,'value': i} for i in mgr_options3
                #                         #     ],
                #                         placeholder="Select an Domain",
                #                     ),
                #             className="two columns",
                # ),
                    ],
                    className="row",
                ),
                        #Dropdown only severity 1 
                     
                        #Indicators row div 
            html.Div(
                    [
                        indicator(
                            "#00cc96", "Average level of Availability on the given period:", "left_leads_indicator"
                        ),
                        indicator(
                            "#119DFF", "Total number of Critical Incident on the given period:", "middle_leads_indicator"
                        ),
                        indicator(
                            "#EF553B",
                            "Worst Performing services:",
                            "right_leads_indicator",
                        ),
                    ],
                    className="row",
                    style={"marginTop": "10"}
                ),


                        #Chart row div 
            html.Div(
                [
                html.Div(
                    [       #html.P("Split per Application of the Total Incident" ),
                            dcc.Graph(
                            id='graph2',
                            style={"width":"100%","height":"100%","frameborder":"0"},
                            config=dict(displayModeBar=False),
                            ),
                    ],
                className="six columns chart_div"
                ),
                # html.Div(
                #     [
                # html.Iframe(
                #             src="//plot.ly/~arthur_mf/82.embed?showlink=false",
                #             style={"width":"100%" ,"height":"100%","frameborder":"0"}
                #          ),
                #     ],
                # className="four columns chart_div"
                # ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/84.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div"
                ),
                ],
                className="row",
                style={"marginTop": "10"},
        ),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                    id='dropdown-55',
                    options=[{'label': i, 'value': i} for i in mgr_options4],
                    value='.COM',
                    placeholder="Select a Service",
                    )
                ])
                # dcc.Graph(id='graph44'),
            ])
        ],
                className="row",
                style={"marginTop": "10px"},
        ),
        html.Div([
                dcc.Graph(id='graph44')
        ],
                        className="row",
                        style={"marginTop": "10px"},
        ),

        html.Div(
                [
                html.Div(
                    [
                            dcc.Graph(
                            id='graph2',
                            style={"width":"100%","height":"100%","frameborder":"0"},
                            config=dict(displayModeBar=False),
                            ),
                    ],
                className="six columns chart_div"
                ),
                # html.Div(
                #     [
                # html.Iframe(
                #             src="//plot.ly/~arthur_mf/82.embed?showlink=false",
                #             style={"width":"100%" ,"height":"100%","frameborder":"0"}
                #          ),
                #     ],
                # className="four columns chart_div"
                # ),
                html.Div(
                    [
                html.Iframe(
                            src="//plot.ly/~arthur_mf/84.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div"
                ),
                ],
                className="row",
                style={"max-height": "300px","marginTop": "10px"},
        ),
                     #table div   
            html.Div(
                generate_table(df), 
                className="row",
                id = "table", 
                style={
                    "margin-top": "30px",
                "max-height": "350px",
                "overflow-y": "scroll",
                "padding": "8px",
                "background-color": "white","border": "1px solid rgb(200, 212, 227)","border-radius": "3px",},
            ),
            ],
        )
        #TABS BUSINESS (TO DO)
    elif tab == 'cases_tab':
        return html.Div([
            html.H3('Tab content 2'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
        #Tabs overview : Here you'll be able to do some callbacks. 
    elif tab == 'opportunities_tab' :
        return html.Div([
            html.H3('Tab content 1'),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [3, 1, 2],
                        'type': 'bar'
                    }]
                }
            )
        ])

#Callback Critical per incident services
@app.callback(
    Output('graph44', 'figure'),
    [Input('dropdown-55', 'value') 
    ])


def graph_44(input):
    print(input)

    filtered_df = servAvail_df[servAvail_df['Service']==input]

    months = ['January','February','March','April','May','June']

    availability=[]

    for i in months:
        p=filtered_df[i].unique()
        p=p.tolist()
        p=p[0]
        availability.append(p)

       
    return ({
        'data': [{'x':months, 'y':availability,'type':'scatter', 'name':input}
        ],
        'layout': go.Layout(
            xaxis={'type':'category', 'title': 'Month'},
            yaxis={'title': '% Availability'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title="Availability for {}".format(input)
            )
        }
        )


@app.callback(
    Output('graph2', 'figure'),
    [Input('Month', 'value')])
def graph_2(input):
    #print(input)
    #print(other)
    fil= dff[(dff['Month '] == input)]
    
 #   prio=filtered_df['Priority'].unique()
    domain = fil['Domain'].unique()


    
    traces = []

    for i in domain:
        
        app = fil[fil['Domain']==i].groupby('CI_Name').size()
        nb_app = fil[fil['Domain']==i]['CI_Name'].unique()

        traces.append(go.Bar(
            x=nb_app,
            y=app,
            name=i,

        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type':'category', 'title': input},
            yaxis={'title': 'Number of Incidents'},
            barmode="group",
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )}


if __name__ == '__main__':
    app.run_server(debug=True)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})






#%%
