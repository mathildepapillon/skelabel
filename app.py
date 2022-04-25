import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from __main__ import *
import Calculations
import Controls
import Callbacks
import pandas as pd

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

##################################################################
##################################################################
# LAYOUT

app.layout = dbc.Container(
    [
        html.H1(children='Dash App for Plotting One Dance'),
        html.Hr(),

        dbc.Row([
            dbc.Col(Controls.Card, md=3),
            dbc.Col(dcc.Graph(id="OneDanceGraph",style={'width': '140vh', 'height': '120vh'}), md=8),
        ], align="center",),
        
        #dcc.Store(id='seq_dataj', storage_type='local')
    ],
    fluid=True,
)
##################################################################
##################################################################
# CALLBACKS

#What happens when the Environment button is clicked
#start by listing every single input and output parameter neccessary to the callback
# @app.callback(

#      Output('button_output', 'children'),
#      [Input('chosen_seq_len', 'value'),
#      Input('which_seq', 'value'),
#      Input('button', 'n_clicks'),
#      ], prevent_initial_call=True)

# #Function that the app performs
# def when_button_clicked(chosen_seq_len, which_seq, button):

#     button_output=Callbacks.when_button_clicked(chosen_seq_len, which_seq, button)

#     return button_output
# #########################


@app.callback(
    Output('OneDanceGraph', 'figure'),
    [Input('chosen_seq_len', 'value'),
    Input('which_seq', 'value'),
    Input('button', 'n_clicks')
    ])

def get_figure(chosen_seq_len, which_seq, n_clicks):
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if n_clicks is not None:
        seq_data = Calculations.get_seq_data(chosen_seq_len)

        if n_clicks==1:
            OneDanceGraph = Callbacks.fig(seq_data, which_seq)
        if n_clicks > 1:
            next_which_seq = which_seq + n_clicks*chosen_seq_len    
            OneDanceGraph = Callbacks.fig(seq_data, next_which_seq)

    return OneDanceGraph

# @app.callback(
#     Output('OneDanceGraph', 'figure'),
#     [Input('chosen_seq_len', 'value'),
#     Input('which_seq', 'value'),
#     Input('button_next', 'n_clicks'),
#     ])

# def update_which_seq(chosen_seq_len, which_seq, n_clicks):
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate

#     if n_clicks is not None:
#         next_which_seq = which_seq + n_clicks*chosen_seq_len
#         seq_data = Calculations.get_seq_data(chosen_seq_len)
#         OneDanceGraph = Callbacks.fig(seq_data, next_which_seq)

#     #seq_dataj = (seq_data.tolist()).to_json(date_format='iso', orient='split')

#     return OneDanceGraph






# @app.callback(
#     Output('OneDanceGraph', 'figure'),
#     [Input('seq_dataj', 'data'),
#      Input('which_seq', 'value'),
#      Input('button2', 'n_clicks')
#      ])

# def update_graph(seq_dataj, which_seq, n_clicks):

    
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate

#     if n_clicks is not None:
#         print('gonna get seq_data')
#         seq_data = pd.read_json(seq_dataj, orient='split')
#         print('got it')
#         OneDanceGraph = Callbacks.fig(seq_data, which_seq)

#     return OneDanceGraph


#############################################################################
# RUN ON SERVER
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8080)
