import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df_table = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv'
)

df_chart = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv'
)

df_chart1 = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)


# generate HTML table from the dataset
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [
            html.Tr(
                [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(min(len(dataframe), max_rows))
        ])


# external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# inline css
colors = {'background': '#D5DBDB', 'text': '#1F618D'}

# app main body
app.layout = html.Div([
    html.H1(
        style={
            'backgroundColor': colors['background'],
            'color': colors['text'],
            'textAlign': 'center',
        },
        children=['Glance of Dash and What Can Dash Do'],
    ),
    html.Div([
        html.P('Dash: A web application framework for Python.'),
        html.
        P('Dash is written on top of Flask, Plotly.js and React.js but provides pure Python abstraction around HTML, CSS and JavaScript'
          ),
    ]),
    # a simple grouped cahrt
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {
                    'x': ['Jan', 'Feb', 'Mar'],
                    'y': [4, 1, 2],
                    'type': 'bar',
                    'name': 'Existing Writer',
                },
                {
                    'x': ['Jan', 'Feb', 'Mar'],
                    'y': [2, 4, 5],
                    'type': 'bar',
                    'name': u'New Writer',
                },
            ],
            'layout': {
                'title': 'Sample Data Visualization'
            },
        },
    ),
    html.Div(
        children=
        'Dash output is a web application while Plotly output is interactive plot.',
        style={'textAlign': 'center'},
    ),
    # static table
    html.Div(children=[
        html.H4(children='US Agriculture Exports (2011)'),
        generate_table(df_table),
    ]),
    html.Div(
        children=
        'Core Components example: dropdown, multi-selection, radio items, checkboxes, text input and also slideer',
        style={
            'textAlign': 'center',
            'padding': '40px'
        },
    ),
    # different html components
    html.Div(
        [
            html.Label('Dropdown'),
            dcc.Dropdown(
                options=[
                    {
                        'label': 'New York City',
                        'value': 'NYC'
                    },
                    {
                        'label': u'Montréal',
                        'value': 'MTL'
                    },
                    {
                        'label': 'San Francisco',
                        'value': 'SF'
                    },
                ],
                value='MTL',
            ),
            html.Label('Multi-Select Dropdown'),
            dcc.Dropdown(
                options=[
                    {
                        'label': 'New York City',
                        'value': 'NYC'
                    },
                    {
                        'label': u'Montréal',
                        'value': 'MTL'
                    },
                    {
                        'label': 'San Francisco',
                        'value': 'SF'
                    },
                ],
                value=['MTL', 'SF'],
                multi=True,
            ),
            html.Label('Radio Items'),
            dcc.RadioItems(
                options=[
                    {
                        'label': 'New York City',
                        'value': 'NYC'
                    },
                    {
                        'label': u'Montréal',
                        'value': 'MTL'
                    },
                    {
                        'label': 'San Francisco',
                        'value': 'SF'
                    },
                ],
                value='MTL',
            ),
            html.Label('Checkboxes'),
            dcc.Checklist(
                options=[
                    {
                        'label': 'New York City',
                        'value': 'NYC'
                    },
                    {
                        'label': u'Montréal',
                        'value': 'MTL'
                    },
                    {
                        'label': 'San Francisco',
                        'value': 'SF'
                    },
                ],
                value=['MTL', 'SF'],
            ),
            html.Label('Text Input'),
            dcc.Input(value='MTL', type='text'),
            html.Label('Slider'),
            dcc.Slider(
                min=0,
                max=9,
                marks={
                    i: 'Label {}'.format(i) if i == 1 else str(i)
                    for i in range(1, 6)
                },
                value=5,
            ),
        ],
        style={'columnCount': 2},
    ),
    html.Div(
        children='Callback, which makes the Dash app interactive',
        style={
            'textAlign': 'center',
            'padding': '40px'
        },
    ),
    # callback, which is one of the most important component in Dash
    html.Div([
        dcc.Input(id='input-value', value='null', type='number'),
        html.Div(id='input-div')
        # no need to set default children to input-div since it will be overwriter when app start
    ]),
    html.Div(
        children='Callback example - Interactive graph with slider as input',
        style={
            'textAlign': 'center',
            'padding': '40px'
        },
    ),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_chart1['year'].min(),
        max=df_chart1['year'].max(),
        value=df_chart1['year'].min(),
        marks={str(year): str(year)
               for year in df_chart1['year'].unique()},
        step=None,
    ),
])


@app.callback(
    Output(component_id='input-div', component_property='children'),
    # use id anc property to identify the callback input/output component
    # the keywords can by omit but make sure the sequence is id frist and property after
    [Input(component_id='input-value', component_property='value')],
)
# the simple callback function output
def update_output_div(input):
    return 'Input value is "{}"'.format(input)


@app.callback(Output('graph-with-slider', 'figure'),
              [Input('year-slider', 'value')])
def update_figure(selected_years):
    filtered_df = df_chart1[df_chart1.year == selected_years]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(
            dict(
                x=df_by_continent['gdpPercap'],
                y=df_by_continent['lifeExp'],
                text=df_by_continent['country'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 10,
                    'line': {
                        'width': 0.7,
                        'color': 'white'
                    }
                },
                name=i,
            ))

    return {
        'data':
        traces,
        'layout':
        dict(
            xaxis={
                'type': 'log',
                'title': 'Interactive GPD Per Capital',
                'range': [2, 5],
            },
            yaxis={
                'title': 'Life Expentacy',
                'range': [10, 90]
            },
            margin={
                'l': 40,
                'b': 40,
                't': 10,
                'r': 10
            },
            legend={
                'x': 0,
                'y': 1
            },
            transition={'duration': 500},
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)
