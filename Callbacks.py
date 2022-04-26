import plotly.graph_objects as go
import Calculations
import dash

def fig(seq_data, which_seq):
    print('Getting x y z for figure')
    dream_x, dream_y, dream_z = Calculations.make_dreams(seq_data, which_seq)
    print('Making figure')
    # Create figure
    fig = go.Figure(go.Scatter3d(x=[], y=[], z=[],
                                    mode='lines', 
                                    line_width=3, 
                                    line_color='blue',
                                )
                    )  

    # Frames
    a=1.7
    frames = [go.Frame(data= [go.Scatter3d(x=a*dream_x[k+1],
                                        y=a*dream_y[k+1],
                                        z=a*dream_z[k+1],)
                                        
                            ],
                    traces= [0],
                    name=f'frame{k}'      
                    )for k  in  range(len(dream_x)-1)
            ]

    fig.update(frames=frames)



    fig.update(frames=frames)

    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
                }


    sliders = [
        {"pad": {"b": 10, "t": 60},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        
        "steps": [
                    {"args": [[f.name], frame_args(0)],
                    "label": str(k),
                    "method": "animate",
                    } for k, f in enumerate(fig.frames)
                ]
        }
            ]

    fig.update_layout(

        updatemenus = [{"buttons":[
                        {
                            "args": [None, frame_args(50)],
                            "label": "Play", 
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "Pause", 
                            "method": "animate",
                    }],
                        
                    "direction": "left",
                    "pad": {"r": 70, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0.5,
                }
            ],
            sliders=sliders
        )

    # dream_x_num = list(filter(None, dream_x))
    # dream_y_num = list(filter(None, dream_y))
    # dream_z_num = list(filter(None, dream_z))

    fig.update_layout(scene = dict(xaxis=dict(range=[0.4, 0.4], autorange=False),
                            yaxis=dict(range=[0.4, 0.4], autorange=False),
                            zaxis=dict(range=[0.4, 0.4], autorange=False),
                            aspectratio=dict(x=1, y=1, z=1)
                            )
                )


    # fig.update_layout(scene = dict(xaxis=dict(range=[min(all(dream_x))*1.2, max(all(dream_x))*2], autorange=False),
    #                             yaxis=dict(range=[min(all(dream_y))*1.2, max(all(dream_y))*2], autorange=False),
    #                             zaxis=dict(range=[min(all(dream_z))*1.2, max(all(dream_z))*2], autorange=False),
    #                             aspectratio=dict(x=1, y=1, z=1)
    #                             )
    #                 )

    fig.update_layout(sliders=sliders)
    return fig
