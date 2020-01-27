import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

df_table = pd.read_csv('C:/Users/TLIU/Desktop/demo_data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(
        style={
            'textAlign': 'center',
        },
        children=['Line Chart'],
    ),
    html.Div([
        html.P('Promotion 1'),
        dcc.Input(id='prom1', value='0', type='number'),
    ],
             style={
                 'width': '25%',
                 'display': 'inline-block'
             }),
    html.Div([
        html.P('Promotion 2'),
        dcc.Input(id='prom2', value='0', type='number'),
    ],
             style={
                 'width': '25%',
                 'display': 'inline-block'
             }),
    html.Div([
        html.P('Promotion 3'),
        dcc.Input(id='prom3', value='0', type='number'),
    ],
             style={
                 'width': '25%',
                 'display': 'inline-block'
             }),
    html.Div([html.Button('Submit', id='submit-button', n_clicks=0)],
             style={
                 'width': '15%',
                 'display': 'inline-block'
             }),
    dcc.Graph(id='table')
])


@app.callback(Output("table", 'figure'), [Input('submit-button', 'n_clicks')], [
    State('prom1', 'value'),
    State('prom2', 'value'),
    State('prom3', 'value')
])
def update_df(n_clicks, prom1, prom2, prom3):
    df_table.loc[df_table.month > 9, 'prom1'] = prom1
    df_table.loc[df_table.month > 9, 'prom2'] = prom2
    df_table.loc[df_table.month > 9, 'prom3'] = prom3
    df_table.loc[df_table.month > 9, 'output'] = float(
        prom1) * df_table.prom1_coef + float(
            prom2)**df_table.prom2_coef + float(prom3) * df_table.prom3_coef
    return {
        'data': [
            dict(x=df_table.month,
                 y=df_table.output,
                 mode='lines+markers',
                 marker={
                     'size': 10,
                 })
        ],
        'layout':
        dict(
            xaxis={
                'title': "Month",
                'tickmode': 'linear'
            },
            yaxis={'title': "TRx"},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)