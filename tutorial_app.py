import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

df_table = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv'
)

df_chart = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv'
)

df_chart1 = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)

# data for multi input chart
df_multi = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df_multi['Indicator Name'].unique()

# options for chained callback
all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}

# sample data for cross filter
np.random.seed(0)
df_cross = pd.DataFrame({"Col " + str(i+1): np.random.rand(30) for i in range(6)})

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

# can still use inline css
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
          # might not all html tags work with in dash html component, like <br>
    ]),
    # a grouped chart but the code is slightly different from pure plotly
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
            # it seems in dash a chart title will be automaticly centered
        },
    ),
    html.Div(
        children=
        'Dash output is a web application while Plotly output is interactive plot.',
        style={'textAlign': 'center'},
    ),
    # static table, which is not that useful. Need stylesheet to change the look since the plain one is not good
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
    # different html components, combined with callback which can provide interactions
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
                # set default value
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
                # multi checkbox, default dropdown will be a single selection
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
        # not sure what this columnCount does here
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
        dcc.Input(id='input-value', value='None', type='number'),
        # use different ID to locate different callback input and output
        html.Div(id='input-div')
        # no need to set default children to input-div since it will be overwritten when app start
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

    html.Div(
        children=
        'Multiple input and output are also available',
        style={
            'padding-top': '40px',
            'padding-bottom': '40px',
            'color': 'red',
        },
    ),

    html.Div([
    # chart with multiple input
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df_multi['Year'].min(),
        max=df_multi['Year'].max(),
        value=df_multi['Year'].max(),
        marks={str(year): str(year) for year in df_multi['Year'].unique()},
        step=None
    ),

    html.Div(
        children=
        'Callbacks can be chained to make multi level selection/filter',
        style={
            'padding-top': '40px',
            'padding-bottom': '40px',
        },
    ),

    dcc.RadioItems(
        id='countries-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),

    html.Hr(),
    # horizontal rule

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    html.Div(id='display-selected-values'),

    html.Div(
        children=
        'Right 2 charts will change based on the hover position on the left scatter plot. The basic alignment based on page width, need better CSS to avoid any overlay.',
        style={
            'padding-top': '40px',
            'padding-bottom': '40px',
        },
    ),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata':'Japan'}]}
            # hover item setting
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    # use width only to align 3 different chart, increase padding should remove the overlay

    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=df_multi['Year'].min(),
        max=df_multi['Year'].max(),
        value=df_multi['Year'].max(),
        marks={str(year): str(year) for year in df_multi['Year'].unique()},
        step=None
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),


    html.Div(
        children=
        'Cross filter among different charts',
        style={
            'padding-top': '40px',
            'padding-bottom': '40px',
        },
    ),

])


@app.callback(
    Output(component_id='input-div', component_property='children'),
    # use id anc property to identify the callback input/output component
    [Input(component_id='input-value', component_property='value')],
    # the keywords can by omit but make sure the sequence is id frist and property after
)
# the simple input box callback function
def update_output_div(input):
    return 'Input value is "{}"'.format(input)

# the main body of a callback is the function behind it


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

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    df_year = df_multi[df_multi['Year'] == year_value]

    return {
        'data': [dict(
            x=df_year[df_year['Indicator Name'] == xaxis_column_name]['Value'],
            y=df_year[df_year['Indicator Name'] == yaxis_column_name]['Value'],
            text=df_year[df_year['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            # default is closet, if clickmode lacks the select flag it will be set to 'x' or 'y' depends on the orientation value
        )
    }

# 3 callbacks to make the chain
@app.callback(
    Output('cities-radio', 'options'),
    [Input('countries-radio', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-radio', 'value'),
    [Input('cities-radio', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [Input('countries-radio', 'value'),
     Input('cities-radio', 'value')])
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )

# similer to the one at line 450
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph_multi(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    df_year = df_multi[df_multi['Year'] == year_value]

    return {
        'data': [dict(
            x=df_year[df_year['Indicator Name'] == xaxis_column_name]['Value'],
            y=df_year[df_year['Indicator Name'] == yaxis_column_name]['Value'],
            text=df_year[df_year['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=df_year[df_year['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(df_tmp, axis_type, title):
    return {
        'data': [dict(
            x=df_tmp['Year'],
            y=df_tmp['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }

# following two callbacks will update right two charts based on mouse hover
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    df_tmp = df_multi[df_multi['Country Name'] == country_name]
    df_tmp = df_tmp[df_tmp['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(df_tmp, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
    df_tmp = df_multi[df_multi['Country Name'] == hoverData['points'][0]['customdata']]
    df_tmp = df_tmp[df_tmp['Indicator Name'] == yaxis_column_name]
    return create_time_series(df_tmp, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server(debug=True)
