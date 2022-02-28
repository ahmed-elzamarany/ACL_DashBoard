# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc,html
from dash.dependencies import Input, Output
import pandas as pd
import pathlib
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash
# get relative data folder
PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../datasets").resolve()

df = pd.read_csv(DATA_PATH.joinpath("statistics.csv"))  # GregorySmith Kaggle
df.index = pd.to_datetime(df['month'])

features=list(df.columns)
features.remove("count")
features.remove("author")
features.remove("month")
keys = [  "Avg. of Confidence Score",
          "Avg. of Charaters in Paper Summary",
          "Avg. of Charaters in Summary Of Strengths",
          "Avg. of Charaters in Summary Of Weaknesses",
          "Avg. of Charaters in Comments",
          "Avg. of Overall Assessment Score",
          "Avg. of the Datasets Score",
          "Avg. of the Software Score",
          "Avg. of the Author Identity Guess Score",
          "No. of missed Assignments"]
featuresdic = dict(zip(keys, features))
def get_options(list_authors):
    dict_list = []
    for i in list_authors:
        dict_list.append({'label': i, 'value': i})
    return dict_list

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.CYBORG])
server = app.server           
app.layout = html.Div([
   dbc.Row(
            dbc.Col(
                
                html.H2(dbc.Badge("Loading...", 
                                  pill=True,color="light",id='my-output'))
                 
            ,align="center")
        )
    ,
    html.Div([
        dbc.Row(
            [dbc.Col(
                html.Div(dcc.Dropdown(
            id='authorselector', value=[df['author'].sort_values()[0],
                                        df['author'].sort_values()[1],
                                        df['author'].sort_values()[2]]
            ,multi=True,style={'backgroundColor': '#1E1E1E'},
            options=get_options(df['author'].unique())
        )), width=6),
        
        dbc.Col( html.Div(dcc.Dropdown(
            id='featureselector', value="Select", clearable=False,
            persistence=True, persistence_type='memory',
            style={'backgroundColor': '#1E1E1E'},
            options=keys
        ), className='six columns'))]  ),
        

        
    ], className='row'),

    dcc.Graph(id='my-bar', figure={}),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
   Input(component_id='featureselector', component_property='value')
)
def update_output_div(input_value):
    if input_value=="Select":
        return "Reviewers Statistics"
    return input_value

@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='authorselector', component_property='value'),
     Input(component_id='featureselector', component_property='value')]
)
def display_value(selected_author,selected_feature):
    if selected_feature=="Select":
        selected_feature="confidence"
    else:
        selected_feature=featuresdic[selected_feature]
        
     # STEP 1
    trace = []
    df_sub = df
    # STEP 2
    for author in selected_author:
        trace.append(go.Bar(x=df_sub[df_sub['author'] == author].index,
                                  y=df_sub[df_sub['author'] == author][selected_feature],
                                  # mode='markers',
                                  opacity=0.6,
                                  name=author,
                                  text=df_sub[df_sub['author'] == author]['count'],
                                  textposition='auto'))
        
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    print(df_sub.index.min())
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                   template='plotly_dark',
                   paper_bgcolor='rgba(0, 0, 0, 0)',
                   plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 30},
                  hovermode='x',
                  autosize=True,
                  # title={'text': [selected_feature], 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': ["2021-04-01 00:00:00", "2022-02-01 00:00:00"]},
              ),
              }

    return figure

if __name__ == '__main__':
    app.run_server(debug=False)