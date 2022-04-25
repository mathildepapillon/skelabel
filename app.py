import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

from __main__ import *
import Calculations
import Controls
import Callbacks

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

##################################################################
##################################################################
# LAYOUT

app.layout = dbc.Container(
    [
        html.H1(children='Dash App for Plotting One Dance'),
        html.Hr(),

        dbc.Row([
            dbc.Col(Controls.Card, md=4),
            dbc.Col(dcc.Graph(id="OneDanceGraph",style={'width': '140vh', 'height': '120vh'}), md=20),
        ], align="center",),
        html.Hr(),
        html.Button('Submit', id='button'),
        html.H3(id='button-clicks'),
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
     ], prevent_initial_call=True)

def update_output(chosen_seq_len, which_seq):

    fig = Callbacks.fig(chosen_seq_len, which_seq)

    return fig


#############################################################################
# RUN ON SERVER
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8080)
