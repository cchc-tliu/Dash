import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import numpy as np

df_table = pd.read_csv('C:/Users/TLIU/Desktop/Cobbs/Dash/demo_data.csv')

hovertemplate = "<b> Month %{x} <br> TRx %{y} <br> Type: %{z}"

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
                 'width': '10%',
                 'display': 'inline-block'
             }),
    html.Div([html.Button('Reset', id='reset-button', n_clicks=0)],
             style={
                 'width': '10%',
                 'display': 'inline-block'
             }),
    dcc.Graph(id='table'),
])


@app.callback(Output("table", 'figure'), [Input('submit-button', 'n_clicks')],
              [
                  State('prom1', 'value'),
                  State('prom2', 'value'),
                  State('prom3', 'value'),
              ])
def update_graph(n_clicks, prom1, prom2, prom3):
    if n_clicks > 0: # should have better logic here
        if prom1 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom1'] = prom1
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom2 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom2'] = prom2
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom3 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom3'] = prom3
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom1 != 0 and prom2 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom1'] = prom1
            df_tmp.loc[df_tmp.month > 9, 'prom2'] = prom2
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom1 != 0 and prom3 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom1'] = prom1
            df_tmp.loc[df_tmp.month > 9, 'prom3'] = prom3
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom2 != 0 and prom3 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom2'] = prom2
            df_tmp.loc[df_tmp.month > 9, 'prom3'] = prom3
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
        if prom1 != 0 and prom2 != 0 and prom3 != 0:
            df_tmp = df_table.copy()
            df_tmp.loc[df_tmp.month > 9, 'prom1'] = prom1
            df_tmp.loc[df_tmp.month > 9, 'prom2'] = prom2
            df_tmp.loc[df_tmp.month > 9, 'prom3'] = prom3
            df_tmp.loc[df_tmp.month > 9,
                       'output'] = float(prom1) * df_tmp.prom1_coef + float(
                           prom2
                       )**df_tmp.prom2_coef + float(prom3) * df_tmp.prom3_coef
    else:
        df_tmp = df_table.copy()
    return {
        'data': [
            dict(x=df_tmp.month,
                 y=df_tmp.output,
                 color=df_tmp.type,
                 hovertemplate=hovertemplate, #type in hover not working
                 mode='lines+markers',
                 marker={
                     'color': [
                         "#1f77b4", "#1f77b4", "#1f77b4", "#1f77b4",
                         "#1f77b4", "#1f77b4", "#1f77b4", "#1f77b4",
                         "#1f77b4", "red", "red", "red"
                     ],
                     'size':
                     10,
                 }) # need split into 2 traces to set different line color
        ],
        'layout':
        dict(
            xaxis={
                'title': "Month",
                'tickmode': 'linear'
            },
            yaxis={
                'title': "TRx",
                'range': [0, 15]
            },
        )
    }


@app.callback(Output('submit-button', 'n_clicks'),
              [Input('reset-button', 'n_clicks')])
def update(reset):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)