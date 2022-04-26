from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

###########################################################

Card_play = dbc.Card([
    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Label("Chosen sequence length", id="chosen_seq_len_label"), md=12)], justify="between"), 
            
        dbc.Row([
            dbc.Col(dcc.Input(id='chosen_seq_len', type='number'),style={"margin-bottom": "10px"}, md=8),
        ]),

       
    ]),

    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Label("Starting index of sequence", id="which_seq_label"), md=12)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='which_seq', type='number'), style={"margin-bottom": "15px"},md=8),
        ]),

        dbc.Row([
            dbc.Col(html.Button('Get dance',style={"margin-bottom": "15px"}, id='button_dance')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Current index of sequence", id="current_index_label"), md=12)], justify="center"),
        dbc.Row([
        dbc.Col(html.Div(id='current_index_to_print')),
        ]),
        dbc.Row([
        dbc.Col(dbc.Label("It is sequence number", id="current_seq_label"), md=12)], justify="center"),
        dbc.Row([
        dbc.Col(html.Div(id='current_seq_to_print')),
        ]),
    ]),

], body=True,)

Card_label = dbc.Card([
    dbc.Form([
       dbc.Row([
            dbc.Col(dbc.Label("Time effort", id="time_label"), md=12)], justify="center"),
        dbc.Row([
            dbc.Col(dcc.Input(id='time', type='number'), style={"margin-bottom": "15px"},md=8),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Space effort", id="space_label"), md=12)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='space', type='number'), style={"margin-bottom": "15px"},md=8),
        ]),
        dbc.Row([
        dbc.Col(html.Button('Save label',style={"margin-bottom": "15px"}, id='button_label')),
        ]),
        dbc.Row([
        dbc.Col(html.Div(id='msg_label_saved')),
        ]),
    ]),

], body=True,)

