import dash
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd

df_table = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

df_chart = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

#generate HTML table from the dataset
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#external stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#inline css
colors = {
    'background': '#D5DBDB',
    'text': '#1F618D'
}

app.layout = html.Div([
    html.H1(style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'textAlign': 'center'
    },
    children=['Glance of Dash and What Can Dash Do']),

    html.Div([
        html.P('Dash: A web application framework for Python.'),
        html.P('Dash is written on top of Flask, Plotly.js and React.js but provides pure Python abstraction around HTML, CSS and JavaScript')
        ]),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': ['Jan', 'Feb', 'Mar'], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Existing Writer'},
                {'x': ['Jan', 'Feb', 'Mar'], 'y': [2, 4, 5], 'type': 'bar', 'name': u'New Writer'},
            ],
            'layout': {
                'title': 'Sample Data Visualization'
            }
        }
    ),

    html.Div(
        children='Dash output is a web application while Plotly output is interactive plot.', style={
        'textAlign': 'center'
    }),

    html.Div(children=[
    html.H4(children='US Agriculture Exports (2011)'),
    generate_table(df_table)]),

    html.Div(
        children='Using Graph to render chart using plotly.js', style={
        'textAlign': 'center',
        'padding': '40px'
    }),

    html.Div([
        dcc.Graph(
        id='life-exp-vs-gdp',
            figure={
            'data': [
                dict(
                    x=df_chart[df_chart['continent'] == i]['gdp per capita'],
                    y=df_chart[df_chart['continent'] == i]['life expectancy'],
                    text=df_chart[df_chart['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df_chart.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
                )
            }
        )
    ]),

    html.Div(
        children='Core Components example: dropdown, multi-selection, radio items, checkboxes, text input and also slideer', style={
        'textAlign': 'center',
        'padding': '40px'
    }),

    html.Div([
        html.Label('Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        ),

        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value=['MTL', 'SF'],
            multi=True
        ),

        html.Label('Radio Items'),
        dcc.RadioItems(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        ),

        html.Label('Checkboxes'),
        dcc.Checklist(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value=['MTL', 'SF']
        ),

        html.Label('Text Input'),
        dcc.Input(value='MTL', type='text'),

        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
            value=5,
        ),
        ], style={'columnCount': 2
    })

])

if __name__ == '__main__':
    app.run_server(debug=True)