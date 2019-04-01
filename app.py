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
import dash
#import dash_auth
import dash_core_components as dcc
import dash_html_components as html
#import plotly

#import math
# Keep this out of source code repository - save in a file or a database
# VALID_USERNAME_PASSWORD_PAIRS = [
#     ['test', 'test1']
# ]

#import os
# Modify these variables with your own info
# APP_NAME = 'Dash Authentication Sample App'
# APP_URL = 'https://my-dash-app.herokuapps.com'

#%% Connect to Post GRE Database 

#Activate this connection if you want to work online
#DATABASE_URL = os.environ['https://s3-eu-west-1.amazonaws.com/iag-test1/Test1.csv']
conn = pg.connect("postgres://tydzgthbfkifxy:58678ccbab767710674d5f5864118633bdcedaf676617ec4f5dd4475cd36d1bc@ec2-23-23-241-119.compute-1.amazonaws.com:5432/d3c492q00bssm9")
#Activate this connection if you want to work with the local PostGre Database (Localhost)
#conn = pg.connect(database="postgres", user = "postgres",password = "", host = "127.0.0.1", port = "5431")
print ("Opened database successfully")

#df = pd.read_sql_query('select * from "Critical_Service_Availability2" limit 1000;', conn)

dff=pd.read_sql_query('select * from "Critical_Service_Availability2";', conn)
dff['year'] = pd.DatetimeIndex(dff['Date_raised']).year
dff['month'] = pd.DatetimeIndex(dff['Date_raised']).month


df = pd.read_sql_query('select "Incident_ID","Description","Date_Start","Priority","MTTR", "CI_Name","Assigned_Group", "Service" from "Critical_Service_Availability2";', conn)
servAvail_df = pd.read_sql_query('select * from "ServAvailJF_1";', conn)

backlog= pd.read_sql_query('select * from "Backlog Analysis";', conn)

backlog=pd.read_sql_query('select "Incidenct Code","Priority","Last Modified Date","Tower Group", "Incident Description","Aging (Days)" from "Backlog Analysis"', conn)
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
                className="indicator_value",
                style= {"color":"#CE3030","font-size": "25px"}
            ),
        ],
        className="four columns indicator",
        
    )

#Best indicator 

def indicator2(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value",
                style= {"color":"#1CBA27","font-size": "25px"}
            ),
        ],
        className="four columns indicator",
        
    )

#Reading Data from the database : return a  toble (key,value)
def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [   

                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "New Month",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="leads_modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # modal form
                        html.Div(
                            [
                                html.P(
                                    [
                                        "File Name",
                                        
                                    ],
                                    style={
                                        "float": "left",
                                        "marginTop": "4",
                                        "marginBottom": "2",
                                    },
                                    className="row",
                                ),
                                dcc.Input(
                                    id="new_lead_company",
                                    # placeholder="Enter company name",
                                    type="text",
                                    value="",
                                    style={"width": "100%"},
                                ),
                                html.P(
                                    "Company State",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="new_lead_state",
                                    options=[
                                            {"label": "January", "value": "January"},
                                            {"label": "February", "value": "February"},
                                            {"label": "March", "value": "March"},
                                            {"label": "April", "value": "April"},
                                            {"label": "May", "value": "May"},
                                            {"label": "June", "value": "June"},
                                            {"label": "July", "value": "July"},
                                            {"label": "August", "value": "August"},
                                            {"label": "September", "value": "September"},
                                            {"label": "October", "value": "October"},
                                            {"label": "November", "value": "November"},
                                            {"label": "December", "value": "December"},
                                        ],
                                    placeholder="Select an Month",
                                ),
                                html.P(
                                    "Status",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                html.P(
                                    "Source",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="new_lead_source",
                                    options=[
                                        {"label": "CSV File", "value": "Web"},
                                        {
                                            "label": "Excel File",
                                            "value": "Phone Inquiry",
                                        },
                                        {
                                            "label": "SQL Query",
                                            "value": "Partner Referral",
                                        },
                                    ],
                                    value="Web",
                                ),
                            ],
                            className="row",
                            style={"padding": "2% 8%"},
                        ),

                        # submit button
                        
                        html.Div([
                                dcc.Upload([
                                    'Drag and Drop or ',
                                    html.A('Select a File')
                                ], style={
                                    'width': '100%',
                                    'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center'
                                    })
                                ]),
                        html.Hr(),
                        
                        html.Span(
                            "Submit",
                            id="submit_new_lead",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )
            ],
            className="modal",
        ),
        id="leads_modal",
        style={"display": "none"},
    )

#%% Set Up Layout 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions']=True

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )
#%% BUilding the App 

#%% Define value name for dropdown selection 
mgr_options=df["CI_Name"].unique()
mgr_options2=dff["Month "].unique()
mgr_options3=dff["Domain"].unique()
mgr_options4=dff["Service"].unique()
mgr_options5=backlog["Priority"].unique()



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
                    dcc.Tab(label="Overview performance", value="opportunities_tab"),
                    dcc.Tab(label="Performance of Critical Services per Month", value="leads_tab"),
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
    style={"margin": "0%",
         "height": "150%",
    },
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
# reset to 0 add button n_clicks property 
@app.callback(
    Output("new_lead", "n_clicks"),
    [Input("leads_modal_close", "n_clicks"), Input("submit_new_lead", "n_clicks")],
)
def close_modal_callback(n, n2):
    return 0

@app.callback(
    Output("middle_leads_indicator", "children"), [Input('Month', 'value')]
)
def middle_leads_indicator_callback(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = '.COM - 99.1%'
    if input == "January":
        worst_service = 'Flight - 99.36%'
    if input == "February":
        worst_service = 'MAD HUB - 99.3%'
    return worst_service

@app.callback(
    Output("middle_leads_indicator2", "children"), [Input('Month', 'value')]
)
def middle_leads_indicator_callback(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = 'Ticketing - 99.97%'
    if input == "January":
        worst_service = 'Ticketing - 99.98%'
    if input == "February":
        worst_service = 'Flight Dispatching - 99.98%'
    return worst_service

@app.callback(
    Output("middle_leads_indicator3", "children"), [Input('Month', 'value')]
)
def middle_leads_indicator_callback(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = '97.7% YTD'
    if input == "January":
        worst_service = '97.8% MTD'
    if input == "February":
        worst_service = '97.6% MTD'
    return worst_service

@app.callback(
    Output("left_leads_indicator", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = '.COM - 5,5 DAYS'
    if input == "January":
        worst_service = '.COM - 5 DAYS'
    if input == "February":
        worst_service = '.COM - 6 DAYS'
    return worst_service


@app.callback(
    Output("left_leads_indicator2", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = 'Flight Dispatching - 30 DAYS'
    if input == "January":
        worst_service = 'Flight Dispatching - 30 DAYS'
    if input == "February":
        worst_service = 'Flight Dispatching - 30 DAYS'
    return worst_service

@app.callback(
    Output("left_leads_indicator3", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = '19537 Incidents (Jan/Feb)'
    if input == "January":
        worst_service = '10 401 Incidents'
    if input == "February":
        worst_service = '9 136 Incidents'
    return worst_service


@app.callback(
    Output("right_leads_indicator", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = 'Flight Tracking - 296 MIN'
    if input == "January":
        worst_service = 'Flight Tracking - 430 MIN'
    if input == "February":
        worst_service = 'Crew Mng - 300 MIN'
    return worst_service

@app.callback(
    Output("right_leads_indicator3", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = '1293 Incidents remaining YTD'
    if input == "January":
        worst_service = '1293 Incidents remaining'
    if input == "February":
        worst_service = '1186 Incidents remaining'
    return worst_service

@app.callback(
    Output("right_leads_indicator2", "children"), [Input('Month', 'value')]
)
def Reliability(input):
    #print(input)
    #df = pd.read_json(df, orient="split")
    if input == "All_Months":
       worst_service = 'Flight Dispatching - 162 MIN'
    if input == "January":
        worst_service = 'Flight Dispatching - 97 MIN'
    if input == "February":
        worst_service = 'Flight Tracking - 161 MIN'
    return worst_service
#Callbacks for Application
# @app.callback(
#     dash.dependencies.Output('table', 'children'),
#     [dash.dependencies.Input('dropdown-1', 'value')])
# def update_graph(ci_name):
#     if dropdown-1 == ".COM":
#     a = df_plot.loc[df_plot["Service"] == ci_name]
#     return generate_table(a)

@app.callback(
    dash.dependencies.Output('table', 'children'),
    [dash.dependencies.Input('Service', 'value')])
def update_graph(ci_name):
    print(ci_name)
    if ci_name == "All Applications":
        df_plot = df.copy()
    else:
        df_plot = df[df['Service'] == ci_name]

    a = df_plot.loc[df_plot["Service"] == ci_name]

    return generate_table(a)

# hide/show modal
@app.callback(Output("leads_modal", "style"), [Input("new_lead", "n_clicks")])
def display_leads_modal_callback(n):
    print(n)
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}


@app.callback(
    dash.dependencies.Output('table2', 'children'),
    [dash.dependencies.Input('Service2', 'value')])
def update_graph(ci_name):
    print(ci_name)
    if ci_name == "All Applications":
        df_plot = df.copy()
    else:
        df_plot = backlog[backlog['Priority'] == ci_name]

    a = df_plot.loc[df_plot["Priority"] == ci_name]

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
                html.Div(
                        dcc.Dropdown(
                                        id="Month",
                                        options=[
                                            {"label": "All Months", "value": "All_Months"},
                                            {"label": "January", "value": "January"},
                                            {"label": "February", "value": "February"},
                                            # {"label": "March", "value": "March"},
                                            # {"label": "April", "value": "April"},
                                            # {"label": "June", "value": "June"},
                                        ],
                                        value='All_Months',
                                    ),
                        dcc.Dropdown(
                                        id='dropdown-1',
                                        options=[{'label': i,'value': i} for i in mgr_options],
                                        value='All Applications'
                        ),
                            className="two columns",
                            style={"float": "left"},
                ),
                html.Div(
                html.Span(
                    "Add new Month",
                    id="new_lead",
                    n_clicks=0,
                    className="button button--primary",
                    style={
                        "height": "34",
                        "background": "#119DFF",
                        "border": "1px solid #119DFF",
                        "color": "white",
                    },
                ),
                className="two columns",
                style={"float": "right"},
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
                            "#00cc96", "Worst Service (Number of Days between 2 failures):", "left_leads_indicator"
                        ),
                        indicator(
                            "#119DFF", "Availability - Worst Service:", "middle_leads_indicator"
                        ),
                        indicator(
                            "#EF553B",
                            "Worst Service (Average time to repair per month):",
                            "right_leads_indicator",
                        ),
                    ],
                    className="row",
                    style={"marginTop": "10"}
                ),
            html.Div(
                    [
                        indicator2(
                            "#00cc96", "Best Service (Number of Days between 2 failures):", "left_leads_indicator2"
                        ),
                        indicator2(
                            "#119DFF", "Availability - Best Service:", "middle_leads_indicator2"
                        ),
                        indicator2(
                            "#EF553B",
                            "Best Service (Average time to repair per month):",
                            "right_leads_indicator2",
                        ),
                    ],
                    className="row",
                    style={"marginTop": "10"}
                ),


                        #Chart row div 
            html.Div(
                [
                html.Div(
                    [      
                    html.Iframe(
                                src="//plot.ly/~arthur_mf/89.embed?showlink=false",
                                style={"width":"100%" ,"height":"100%","frameborder":"0"}
                       )],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px' },
                ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/91.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px'
                },
                ),
                ],
                className="row",
                style={"marginTop": "10",
                        'height': '525px'
                },
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

        # html.Div(
        #         [
        #         html.Div(
        #             [
        #                     dcc.Graph(
        #                     id='graph2',
        #                     style={"width":"100%","height":"100%","frameborder":"0"},
        #                     config=dict(displayModeBar=False),
        #                     ),
        #             ],
        #         className="six columns chart_div"
        #         ),
        #         html.Div(
        #             [
        #         html.Iframe(
        #                     src="//plot.ly/~arthur_mf/84.embed?showlink=false",
        #                     style={"width":"100%" ,"height":"100%","frameborder":"0"}
        #                  ),
        #             ],
        #         className="six columns chart_div"
        #         ),
        #         ],
        #         className="row",
        #         style={"max-height": "300px","marginTop": "10px"},
        # ),
                     #table div   
            
            
            
            # html.Div(
            #     generate_table(df), 
            #     className="row",
            #     id = "table", 
            #     style={
            #         "margin-top": "30px",
            #     "max-height": "350px",
            #     "overflow-y": "scroll",
            #     "padding": "8px",
            #     "background-color": "white","border": "1px solid rgb(200, 212, 227)","border-radius": "3px",},
            # ),
            html.Div([
    #html.H2("Application Report"),
                 html.Div([
                     html.Div([
            dcc.Dropdown(
                id="Service",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options4],
                value='.COM'
               )
                ])
                # dcc.Graph(id='graph44'),
            ])
        ],
                className="row",
                style={"marginTop": "10px"},
        ),
        html.Div([
            html.Div(generate_table(df), id = "table")],
            className="row",
            style={
                    "margin-top": "30px",
                "max-height": "350px",
                "overflow-y": "scroll",
                "padding": "8px",
                "background-color": "white","border": "1px solid rgb(200, 212, 227)",
                "border-radius": "3px"},
                    ),
        html.Div(
                [
                html.Div(
                    [      
                    html.Iframe(
                                src="//plot.ly/~arthur_mf/96.embed?showlink=false",
                                style={"width":"100%" ,"height":"100%","frameborder":"0"}
                       )],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px' },
                ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/97.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px'
                },
                ),
                ],
                className="row",
                style={"marginTop": "10",
                        'height': '525px'
                },
        ),
        modal()


            ])
 
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
        return html.Div(
            [
                html.Div(
                    [
                html.Div(
                        dcc.Dropdown(
                                        id="Month",
                                        options=[
                                            {"label": "All Months", "value": "All_Months"},
                                            {"label": "January", "value": "January"},
                                            {"label": "February", "value": "February"},
                                        ],
                                        value='All_Months',
                                    ),
                        dcc.Dropdown(
                                        id='dropdown-1',
                                        options=[{'label': i,'value': i} for i in mgr_options],
                                        value='All Applications'
                        ),
                            className="two columns",
                            style={"float": "left"},
                ),
                    ],
                    className="row",
                ),
            html.Div(
                    [
                        indicator(
                            "#00cc96", "Total number of Incidents :", "left_leads_indicator3"
                        ),
                        indicator2(
                            "#119DFF", "% of the incident solved (Raised-Solved):", "middle_leads_indicator3"
                        ),
                        indicator(
                            "#EF553B",
                            "Nb of Incident in Backlog:",
                            "right_leads_indicator3",
                        ),
                    ],
                    className="row",
                    style={"marginTop": "10"}
                ),
            # html.Div(
            #         [
            #             indicator2(
            #                 "#00cc96", "Best Service (Number of Days between 2 failures):", "left_leads_indicator2"
            #             ),
            #             indicator2(
            #                 "#119DFF", "Availability - Best Service:", "middle_leads_indicator2"
            #             ),
            #             indicator2(
            #                 "#EF553B",
            #                 "Best Service (Average time to repair per month):",
            #                 "right_leads_indicator2",
            #             ),
            #         ],
            #         className="row",
            #         style={"marginTop": "10"}
            #     ),
            html.Div(
                [
                html.Div(
                    [      
                    html.Iframe(
                                src="//plot.ly/~arthur_mf/99.embed?showlink=false",
                                style={"width":"100%" ,"height":"100%","frameborder":"0"}
                       )],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px' },
                ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/101.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px'
                },
                ),
                ],
                className="row",
                style={"marginTop": "10",
                        'height': '525px'
                },
        ),
        # html.Div([
        #     html.Div([
        #         html.Div([
        #             dcc.Dropdown(
        #             id='dropdown-55',
        #             options=[{'label': i, 'value': i} for i in mgr_options4],
        #             value='.COM',
        #             placeholder="Select a Service",
        #             )
        #         ])
        #     ])
        # ],
        #         className="row",
        #         style={"marginTop": "10px"},
        # ),
        html.Div(
                [
                html.Div(
                    [      
                    html.Iframe(
                                src="//plot.ly/~arthur_mf/103.embed?showlink=false",
                                style={"width":"100%" ,"height":"100%","frameborder":"0"}
                       )],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px' },
                ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/105.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px'
                },
                ),
                ],
                className="row",
                style={"marginTop": "10",
                        'height': '525px'
                },
        ),
        html.Div(
                [
                html.Div(
                    [      
                    html.Iframe(
                                src="//plot.ly/~arthur_mf/108.embed?showlink=false",
                                style={"width":"100%" ,"height":"100%","frameborder":"0"}
                       )],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px' },
                ),
                html.Div(
                    [#html.P("% per Service" ),
                html.Iframe(
                            src="//plot.ly/~arthur_mf/111.embed?showlink=false",
                            style={"width":"100%" ,"height":"100%","frameborder":"0"}
                         ),
                    ],
                className="six columns chart_div",
                style={"marginTop": "10",
                        'height': '500px'
                },
                ),
                ],
                className="row",
                style={"marginTop": "10",
                        'height': '525px'
                },
        ),
        html.Div([
                 html.Div([
                     html.Div([
            dcc.Dropdown(
                id="Service2",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options5],
                value='.COM'
               )
                ])
            ])
        ],
                className="row",
                style={"marginTop": "10px"},
        ),
        html.Div(
            
            [
            html.P("INCIDENT IN THE BACKLOG YTD" ),
            html.Div(generate_table(backlog), id = "table2")],
            className="row",
            style={
                    "margin-top": "30px",
                "max-height": "350px",
                "overflow-y": "scroll",
                "padding": "8px",
                "background-color": "white","border": "1px solid rgb(200, 212, 227)",
                "border-radius": "3px"},
                    ),


            ])

@app.callback(
    Output('graph44', 'figure'),
    [Input('dropdown-55', 'value') 
    ])


def graph_44(input):
    #print(input)

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
            title="Service Availability Trends for {}".format(input)
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

app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})






#%%
