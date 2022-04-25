This is a template Dash app.

It contains four parts:
1) app.py
2) Controls.py
3) Callbacks.py
4) Calculations.py


app.py is the hub. This is the script that runs the app (so to run the app, run
app.py). It sets the layout (set in Controls.py) and calls Callbacks (set in
Callbacks.py). The layout defines appearance of the app, and the callbacks
define how the app updates with user interaction.

Controls.py defines the initial values, appearance, and layout of the controls
(e.g. buttons) in the app. The script itself is called in the layout section of
app.py, but each separate control is also called by callbacks in app.py.

Callbacks.py defines what happens when a user interacts with the controls. The
script itself is called in the callbacks section of app.py.

Calculations.py contains all of the actual calculations behind the app. Any
calculation that needs to be called in a Callback must be inside a function so
that the calculation is re-done every time the Callback is called (by updating a
control).



There's a ton of redundancy in organizing the app this way, but I find that it
helps keep things readable as apps get large.
