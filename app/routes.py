from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session, Markup
from scipy import stats
import pandas as pd
import numpy as np
import json
from math import sqrt
from data.data_visualizations import bk_goals, bk_assists, bk_through, bk_long, bk_recover, bk_intercept, bk_gc, bk_shots_cr, bk_tackle_success, bk_duels, bk_passes
from data.data_aggregate import attack, team_play, defensive, summary_stats, descriptive, grand_df, player_df
from bokeh.server.server import Server
from bokeh.embed import server_document, components
from bokeh.resources import INLINE
from threading import Thread
from tornado.ioloop import IOLoop

player_prof = {
    "frank_lampard": [
        "Frank Lampard",
        "Premier League ×3 | FA Cup ×4 | League Cup ×2 | UEFA Champions League | UEFA Europa League",
        ["I simply cannot not pick Frank Lampard", "Ian Wright"],
        "Frank-Lampard.csv"
    ],
    "steven_gerrard": [
        "Steven Gerrard",
        "FA Cup ×2 | League Cup ×3 | UEFA Champions League",
        ["His story is one of those stories to be told, one of those fairytales – just like it happened to me – to be narrated to your children and grandchildren.", "Paolo Maldini"],
        "Steven-Gerrard.csv"
    ],
    "paul_scholes": [
        "Paul Scholes",
        "Premier League ×11 | FA Cup ×3 | League Cup ×2 | UEFA Champions League ×2",
        ["In the last 15 to 20 years the best central midfielder that I have seen — the most complete — is Scholes.", "Xavi Hernandez"],
        "Paul-Scholes.csv"
    ],
    "ngolo_kante": [
        "N'Golo Kanté",
        "Premier League ×2 | FA Cup | UEFA Europa League | FIFA World Cup",
        ["People talk about the Makélélé position, but I am old, and it is time everybody called it the Kanté position.", "Claude Makélélé"],
        "Ngolo-Kante.csv"
    ],
    "yaya_toure": [
        "Yaya Touré",
        "Premier League ×3 | FA Cup | League Cup ×2",
        ["If there's ever going to be a legend at this club then it's this man.", "Vincent Kompany"],
        "Yaya-Toure.csv"
    ],
    "xabi_alonso": [
        "Xabi Alonso",
        "FA Cup | UEFA Champions League",
        ["He was, by some distance, the best central midfielder I ever played alongside.", "Steven Gerrard"],
        "Xabi-Alonso.csv"
    ]
}
# with open(r'player_profiles.json', 'r', encoding='utf-8') as prof_file:
#     player_prof = json.load(prof_file)


@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html')

@app.route('/profile/<player>', methods=["GET"])
def profile(player):
    
    # getting all necessary player info on file
    title = player_prof[player][0]
    accolades = player_prof[player][1]
    quote = player_prof[player][2]
    file = player_prof[player][3]

    # get the img and load the dataframe
    img = 'images/' + player.split('_')[0] + '_profile.jpg'
    
    appearances, wins, losses = summary_stats(file)

    attack_data = attack(file)
    team_play_data = team_play(file)
    defensive_data = defensive(file)
    
    desc_stats = descriptive(file)

    return render_template('profile.html',player=player, title=title, accolades=accolades, quote=quote[0], said_it=quote[1], 
                            img=img, appearances=appearances, wins=wins, losses=losses, attack_data=attack_data.to_dict('record'),
                            team_play_data=team_play_data.to_dict('record'), defensive_data=defensive_data.to_dict('record'),
                            desc_stats=desc_stats)

@app.route('/vis_dash', methods=['GET'])
def vis_dash():

    apps = {'bk_goals': bk_goals(),
            'bk_assists': bk_assists(),
            'bk_through': bk_through(),
            'bk_long': bk_long(),
            'bk_recover': bk_recover(),
            'bk_intercept':bk_intercept(),
            'bk_gc':bk_gc(),
            'bk_shots_cr':bk_shots_cr(),
            'bk_tackle_success':bk_tackle_success(),
            'bk_duels':bk_duels(),
            'bk_passes':bk_passes()
            }

    script, div = components(apps)

    resources = INLINE.render()

    for key, value in div.items():
        div[key] = Markup(value)

    return render_template("vis_dash.html",  template="Flask", resources=Markup(resources), script=Markup(script), div=div)

@app.route('/download/<player>', methods=["GET"])
def download(player):
    name = player_prof[player][0].replace(' ', '-')

    player_data = player_df(name)
    
    resp = make_response(player_data.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + player + ".csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/grand_exp', methods=["GET"])
def grand_exp():
    df = grand_df()
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=grand_data_file.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


#################################################
## Previous code used for embedding bokeh server on flask 

# script_goals = server_document('http://localhost:5006/bk_goals')
# script_assists = server_document('http://localhost:5006/bk_assists')
# script_long = server_document('http://localhost:5006/bk_long')
# script_through = server_document('http://localhost:5006/bk_through')
# script_recover = server_document('http://localhost:5006/bk_recover')
# script_intercept = server_document('http://localhost:5006/bk_intercept')
# script_gc = server_document('http://localhost:5006/bk_gc')
# script_shots_cr = server_document('http://localhost:5006/bk_shots_cr')
# script_tackle_success = server_document('http://localhost:5006/bk_tackle_success')
# script_duels = server_document('http://localhost:5006/bk_duels')
# script_passes = server_document('http://localhost:5006/bk_passes')

# script_goals=Markup(script_goals),
# script_assists=Markup(script_assists), script_long=Markup(script_long),
# script_through=Markup(script_through), script_recover=Markup(script_recover),
# script_intercept=Markup(script_intercept), script_gc=Markup(script_gc),
# script_shots_cr=Markup(script_shots_cr), script_tackle_success=Markup(script_tackle_success),
# script_duels=Markup(script_duels), script_passes=Markup(script_passes),


# def bk_worker():
#     # Can't pass num_procs > 1 in this configuration. If you need to run multiple
#     # processes, see e.g. flask_gunicorn_embed.py
#     apps = {'/bk_goals': bk_goals,
#             '/bk_assists': bk_assists,
#             '/bk_through': bk_through,
#             '/bk_long': bk_long,
#             '/bk_recover': bk_recover,
#             '/bk_intercept':bk_intercept,
#             '/bk_gc':bk_gc,
#             '/bk_shots_cr':bk_shots_cr,
#             '/bk_tackle_success':bk_tackle_success,
#             '/bk_duels':bk_duels,
#             '/bk_passes':bk_passes}
#     server = Server(apps, io_loop=IOLoop(), allow_websocket_origin=["localhost:5006"])
#     server.start()
#     server.io_loop.start()

# Thread(target=bk_worker).start()
