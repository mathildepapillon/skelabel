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
import numpy as np
import base64
import csv

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

##################################################################
##################################################################
# LAYOUT
laban_encoded_image = base64.b64encode(open('./laban.png', 'rb').read())
laban_image = 'data:image/png;base64,{}'.format(laban_encoded_image.decode())

app.layout = dbc.Container(
    [
        html.H1(children='Laban Labels'),
        dbc.Row([
            dbc.Col([Controls.Card_play, Controls.Card_label, dbc.Row(html.Img(src=laban_image,style={'height':'100%', 'width':'100%'})),], md=3),
            dbc.Col(dcc.Graph(id="OneDanceGraph",style={'width': '140vh', 'height': '100vh'}), md=8),
        ], align="center",),
        
        dcc.Store(id='current_seq', storage_type='local'),
        dcc.Store(id='current_index', storage_type='local')
    ],
    fluid=True,
)
##################################################################
##################################################################
# CALLBACKS


@app.callback(
    Output('OneDanceGraph', 'figure'),
    Output('current_index', 'data'),
    Output('current_seq', 'data'),
    Output('current_seq_to_print', 'children'),
    Output('current_index_to_print', 'children'),
    [Input('chosen_seq_len', 'value'),
    Input('which_seq', 'value'),
    Input('button_dance', 'n_clicks')])
    

def get_figure(chosen_seq_len, which_seq, n_clicks):
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if n_clicks is not None:
        seq_data = Calculations.get_seq_data(chosen_seq_len)
        print(seq_data.shape)

        if n_clicks==1:
            OneDanceGraph = Callbacks.fig(seq_data, which_seq)
            current_index = which_seq
            current_seq = 1
            current_seq_to_print = 1
            current_index_to_print = current_index
        if n_clicks > 1:
            next_which_seq = which_seq + n_clicks*chosen_seq_len    
            OneDanceGraph = Callbacks.fig(seq_data, next_which_seq)
            current_index = next_which_seq
            current_seq = n_clicks
            current_seq_to_print = current_seq
            current_index_to_print = current_index

    return OneDanceGraph, current_index, current_seq, current_seq_to_print, current_index_to_print


@app.callback(
    Output('msg_label_saved', 'children'),
    [Input('current_seq', 'data'),
    Input('current_index', 'data'),
    Input('space', 'value'),
    Input('time', 'value'),
    Input('button_label', 'n_clicks')
    ])

def save_label(current_seq, current_index, space, time, n_clicks):
    msg_label_saved=' '
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    if n_clicks==current_seq:
        label = np.array((current_index, space, time))
        print('made label space, time')
        print(label)
        #save the label
        label_file = open('labels.csv', 'a', newline='') #open new csv
        with label_file:
            writer = csv.writer(label_file) #open for writing
            writer.writerow(label) #record parameters

        msg_label_saved = 'Label for seq #{} saved'.format(current_seq)

    return msg_label_saved




#############################################################################
# RUN ON SERVER, make accessible on external browser
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8050)
