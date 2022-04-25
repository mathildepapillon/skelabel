from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

###########################################################

Card = dbc.Card([
    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Label("Chosen sequence length", id="chosen_seq_len_label"), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='chosen_seq_len', type='number'), md=12),
        ]),
    ]),

    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Label("Index of sequence", id="which_seq_label"), md=8)], justify="between"),
        dbc.Row([
            dbc.Col(dcc.Input(id='which_seq', type='number'), md=12),
        ]),
    ]),

], body=True,)
