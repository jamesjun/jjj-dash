import os, dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv'
)

markdown_text = '''
### Data selection scatter plot example
[Source](https://www.datacamp.com/community/tutorials/learn-build-dash-python)
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text)
])

def make_fig(list_continent):
    fig = go.Figure()
    #for i in df.continent.unique():
    for i in list_continent:
        fig.add_trace(
            go.Scatter(
                x=df[df['continent'] == i]['gdp per capita'],
                y=df[df['continent'] == i]['life expectancy'],
                text=df[df['continent'] == i]['country'],
                mode='markers',
                opacity=0.8,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            )
        )

    fig.layout = go.Layout(
            xaxis=dict(type='log', title='GDP Per Capita'),
            yaxis=dict(title='Life Expectancy'),
            margin=dict(l=40, b=40, t=10, r=10),
            legend=dict(x=0, y=1),
            hovermode='closest'
        )
    return fig

list_continent = [df.continent.unique()[0]]
#print(list_continent)

app.layout = html.Div([
    dcc.Markdown(children=markdown_text),
    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': i, 'value': i} for i in df.continent.unique()],
        value=list_continent,
        multi=True
    ),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=make_fig(list_continent)
    ),
    html.Div(id='my-div')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-dropdown', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

@app.callback(
    Output(component_id='life-exp-vs-gdp', component_property='figure'),
    [Input(component_id='my-dropdown', component_property='value')]
)
def update_fig(input_value):
    return make_fig(input_value)


if __name__ == '__main__':
    #fig.write_image("fig1.svg")
    app.run_server(debug=True)
    
