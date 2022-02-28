import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Connect to main app.py file
from app import app
from app import server
import dash_bootstrap_components as dbc
# import data

# Connect to your app pages
from apps import mainapp


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
