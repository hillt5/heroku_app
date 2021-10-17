# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 09:25:01 2021

@author: janep
"""


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


##question1

soql_health = pd.DataFrame()

for i in range(1,6): #iterate through each borough
    soql_url =('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname, spc_common,health,count(tree_id)' +\
        '&$where=borocode='+str(i) +' AND status=\'Alive\'' +\
        '&$group=boroname,spc_common, health').replace(' ', '%20')
    soql_boro = pd.read_json(soql_url) #generate piece of dataframe
    soql_health = soql_health.append(soql_boro) #append to final dataframe

soql_health = soql_health.dropna()
soql_health['spc_common'] = soql_health['spc_common'].str.title()
soql_health = soql_health.sort_values('spc_common')
soql_health = soql_health.reset_index()


##question2

soql_health_steward = pd.DataFrame()

for i in range(1,6): #iterate through each borough
    soql_url1 =('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname, spc_common,health, steward,count(tree_id)' +\
        '&$where=borocode='+str(i) +' AND status=\'Alive\' AND steward!=\'None\'' +\
        '&$group=boroname,spc_common, health, steward').replace(' ', '%20')
    soql_url2 =('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +\
        '$select=boroname, spc_common,health, steward,count(tree_id)' +\
        '&$where=borocode='+str(i) +' AND status=\'Alive\' AND steward=\'None\'' +\
        '&$group=boroname,spc_common, health, steward').replace(' ', '%20')
    soql_boro1 = pd.read_json(soql_url1)
    soql_boro2 = pd.read_json(soql_url2)
    soql_health_steward = soql_health_steward.append([soql_boro1,soql_boro2])

soql_health_steward = soql_health_steward.dropna()
soql_health_steward['spc_common'] = soql_health_steward['spc_common'].str.title()
soql_health_steward = soql_health_steward.sort_values('spc_common')
soql_health_steward = soql_health_steward.reset_index()


#soql_health  = pd.read_csv('health.csv') #temporary local storage of csv
#soql_health_steward = pd.read_csv('health-steward.csv') #temporary local storage of csv

###dash code

app = dash.Dash()
server = app.server


tree_options = soql_health['spc_common'].unique() #unique tree names
borough_options = soql_health['boroname'].unique() #unique borough names

app.layout = html.Div([
    html.H1(children='DATA 608 Module 4: Trees of New York 2015, Health Report and Stewardship Efforts'),
    dcc.Tabs([
        dcc.Tab(label='Tree Health', children=[
            html.H6('Select the tree you\'re interested in:'),
            dcc.Dropdown(id='tree1-column', value = 'Type the Tree Here',
                         options=[{'label' : i, 'value': i} for i in tree_options]),
            dcc.Graph(id='health-graph')
            ]),
        dcc.Tab(label='Tree Health versus Stewardship Efforts', children=[
            html.H6('Select the tree and borough you\'re interested in:'),
            dcc.Dropdown(id='city2-column', value = 'Type the Tree Here',
                         options=[{'label' : i, 'value': i} for i in borough_options]),
            dcc.Dropdown(id='tree2-column', value = 'Type the Tree Here',
                         options=[{'label' : i, 'value': i} for i in tree_options]),
            dcc.Graph(id='steward-graph')
            ])
            ])
            ])


    
@app.callback(
    Output('health-graph', 'figure'),
   Output('steward-graph','figure'),
    [Input('tree1-column', 'value')],
    [Input('city2-column', 'value')],
    [Input('tree2-column', 'value')]
    )
    
    
def update_graphs(tree_name1,boro_name2,tree_name2):
    
    dff1 = soql_health[soql_health['spc_common'] == tree_name1]
    
    fig1 = px.treemap(dff1, path=[px.Constant("New York City"),
                                'boroname', 'spc_common', 'health'],
                     values='count_tree_id', color='health')
    
    dff2 = soql_health_steward[soql_health_steward['spc_common'] == tree_name2]

    dff2 = dff2[dff2['boroname'] == boro_name2]
    
    fig2 = px.bar(dff2, x = 'steward', y = 'count_tree_id',
                 color = 'health', barmode = 'group')
    
    return fig1, fig2



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)
