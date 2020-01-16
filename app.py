import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='CCHC Dash Demo 1'),

    html.Div(children='Dash: A web application framework for Python. Dash is powered by Plotly'),

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
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)