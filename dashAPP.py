from pandas.io.formats.format import DataFrameFormatter, Datetime64Formatter
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px

import pandas as pd
import numpy as np


# Import the initial dataset and clearn data
def cleaner():
    data = pd.read_csv(r'Crime_Data_from_2010_to_2019.csv')
    data = data[(data['LAT']!= 0) & (data['LON'] !=0)]
    data = data.drop(columns=['TIME OCC', 'AREA ', 'Part 1-2', 'Crm Cd Desc', 'Mocodes', 'Premis Cd', 'Premis Desc', 'Weapon Used Cd', 'Weapon Desc', 'Status', 'Status Desc', 'Crm Cd 1', 'Crm Cd 2', 'Crm Cd 3', 'Crm Cd 4', 'Cross Street'])
    data['DATE OCC'] = pd.to_datetime(data['DATE OCC'], errors='coerce')
    data['year']= data['DATE OCC'].dt.year
    pd.to_csv('new_dataset.csv')


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('Years', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=[{
                'label': '2010',
                'value': 2010
            }, {
                'label': '2011',
                'value': 2011
            },
                {
                    'label': '2012',
                    'value': 2012
                },
                {
                    'label': '2013',
                    'value': 2013
                },
                {
                    'label': '2014',
                    'value': 2014
                },
                {
                    'label': '2015',
                    'value': 2015
                },
                {
                    'label': '2016',
                    'value': 2016
                },
                {
                    'label': '2017',
                    'value': 2017
                },
                {
                    'label': '2018',
                    'value': 2018
                },
                {
                    'label': '2019',
                    'value': 2019
                },
            ],
            value=[2010],  # default value
            multi=False
        ),
        html.Br(),
        html.P('Victim Age', style={
            'textAlign': 'center'
        }),
        dcc.RangeSlider(
            id='range_slider',
            min=0,
            max=100,
            step=1,
            value=[5, 15]
        ),
        html.P('Victim Sex', style={
            'textAlign': 'center'
        }),
        dbc.Card([dbc.Checklist(
            id='check_list',
            options=[{
                'label': 'Male',
                'value': 'M'
            },
                {
                    'label': 'Female',
                    'value': 'F'
                },
                {
                    'label': 'Unknown',
                    'value': 'X'
                }
            ],
            value=['M', 'F', 'X'],
            inline=True
        )]),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=[], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=[], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [   html.H4(id='card_title_2', children=[], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2', children=[], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_3', children=[], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_3', children=[], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_4', children=[], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_4', children=[], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])

content_halfSec_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=12
        )
    ]
)

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_2'), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=6
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content = html.Div(
    [
        html.H2('LA Crime Analytics', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        content_halfSec_row,
        content_second_row,
        content_third_row
    ],
    style=CONTENT_STYLE
)

# Import data
data = pd.read_csv(r'new_dataset.csv')

# Create dash object
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])


@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df.groupby(['year', 'Vict Descent']).size().reset_index(name='counts')
    print("test")
    print(df)
    fig = px.line(df, x="year", y="counts", color="Vict Descent")
    return fig


@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    df = df[df['Vict Sex'].isin(check_list_value)]
    df = df[(df['Vict Age'] >= range_slider_value[0]) & (df['Vict Age'] <= range_slider_value[1])]
    newdf = df.groupby(['Vict Descent']).size().reset_index(name='counts')
    fig = px.pie(newdf, values='counts', names='Vict Descent')
    fig.update_traces(textposition='inside')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig


@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])

def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    df = df[df['Vict Sex'].isin(check_list_value)]
    df = df[(df['Vict Age'] >= range_slider_value[0]) & (df['Vict Age'] <= range_slider_value[1])]
    print(df.shape)
    fig = px.histogram(df, x="Vict Sex")
    return fig


@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value): 
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    df = df[df['Vict Sex'].isin(check_list_value)]
    df = df[(df['Vict Age'] >= range_slider_value[0]) & (df['Vict Age'] <= range_slider_value[1])]
    fig = px.scatter_mapbox(df,
            mapbox_style="open-street-map",
            lat=df.LAT,
            lon=df.LON,
            hover_name="DATE OCC", hover_data=["Vict Age", "Vict Sex", "Vict Descent"],
            zoom=10
            )
    fig.update_layout({
        'height': 600
    })
    return fig


# Card 1
@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    return 'Total crimes this year'

@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    totalCrime = df.shape[0]
    return str(totalCrime)

# Card 2
@app.callback(
    Output('card_title_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    return 'Total male victims'

@app.callback(
    Output('card_text_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    totalMale = df[df['Vict Sex'] == 'M'].shape[0]
    return str(totalMale)

# Card 3
@app.callback(
    Output('card_title_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    return 'Total female victims'

@app.callback(
    Output('card_text_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    totalFemale = df[df['Vict Sex'] == 'F'].shape[0]
    return str(totalFemale)

# Card 4
@app.callback(
    Output('card_title_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    return 'Avg age of victims'

@app.callback(
    Output('card_text_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value):
    df = data.copy()
    df = df[df["year"] == dropdown_value]
    avgAge = round(df["Vict Age"].mean(),0)
    return str(avgAge)

if __name__ == '__main__':
    app.run_server(port='8085')
