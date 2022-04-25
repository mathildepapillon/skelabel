import plotly.graph_objects as go
import Calculations

# def when_button_clicked(seq_data, which_seq, button):

#    #This array registers the ids of clicked buttons
#    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
   
#    if 'button' in changed_id: #equivalent of saying "if button is clicked:"

#       #Perform task to make figure, as defined in Calculations.py
#       return_msg_env = Calculations.SetUpEnv(type_of_run, base_name, button_env, hx_min,hx_max,delta_hx,htip,a,qdrad,trad,cone_angle,  dielectric_thic,rad_container,background_mesh,semi_important_mesh,important_mesh,xpoint,ypoint,zpoint,tol,qd_eps,material_eps,vb, T, noise, Ecb, Els, x_size_of_image, y_size_of_image)

#       #return_msg_env will indicate that the directory was successfully made
#       #this message is the Output in the callback  when the task is completed
#       #the callback will print it in the App (as indicated in controls defined in Content.py)
#    else:
#       return_msg_env = ' '

#    return return_msg_env

def fig(chosen_seq_len, which_seq):

    dream_x, dream_y, dream_z = Calculations.make_dreams(chosen_seq_len, which_seq)

    # Create figure
    fig = go.Figure(go.Scatter3d(x=[], y=[], z=[],
                                    mode='lines', 
                                    line_width=3, 
                                    line_color='blue',
                                )
                    )  

    # Frames
    a=2
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
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
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
