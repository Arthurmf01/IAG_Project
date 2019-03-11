#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as pg
import pandas as pd 
import pandas.io.sql as psql

#%% Connect to Post GRE Database 

#conn = pg.connect(database="postgres", user = "postgres",password = "", host = "127.0.0.1", port = "5432")
#print ("Opened database successfully")
#df = pd.read_sql_query('select * from "Test1_1";', conn)

#%% Set Up Layout 
   
#%% BUilding the App 

#%%
app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.H2('Hello World TEST'),
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


#%%
