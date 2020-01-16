import plotly.graph_objects as go
date=['Jan', 'Feb', 'Mar']

fig = go.Figure(data=[
    go.Bar(name='Existing Writer', x=date, y=[4, 1, 2]),
    go.Bar(name='New Writer', x=date, y=[2, 4, 5])
])
# Change the bar mode
fig.update_layout(
    barmode='group', 
    title={
    'text':"Sample Data Visualization", 
    'y':0.9,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})
fig.show()