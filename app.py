import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Connect to main app.py file
import dash_bootstrap_components as dbc
# import data

from apps import mainapp

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.CYBORG])
           
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False)
    
    ,html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Statistics':
        return mainapp.layout
    else:
        return dbc.Button("Reviewers Statistics", href='/apps/Statistics', color="primary")


if __name__ == '__main__':
    app.run_server(debug=False)