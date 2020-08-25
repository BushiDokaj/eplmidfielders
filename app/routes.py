from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session, Markup
from scipy import stats
import pandas as pd
import numpy as np
import json
from math import sqrt
from data.data_visualizations import bk_goals, bk_assists, bk_through, bk_long, bk_recover, bk_intercept, bk_gc, bk_shots_cr, bk_tackle_success, bk_duels
from data.data_aggregate import attack, team_play, defensive, summary_stats, descriptive
from bokeh.server.server import Server
from bokeh.embed import server_document
from bokeh.resources import INLINE
from threading import Thread
from tornado.ioloop import IOLoop

player_prof = None
with open('app\player_profiles.json', 'r', encoding='utf-8') as prof_file:
    player_prof = json.load(prof_file)


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

@app.route('/statistical_analysis', methods=['GET'])
def statistical_analysis():
    script_goals = server_document('http://localhost:5006/bk_goals')
    script_assists = server_document('http://localhost:5006/bk_assists')
    script_long = server_document('http://localhost:5006/bk_long')
    script_through = server_document('http://localhost:5006/bk_through')
    script_recover = server_document('http://localhost:5006/bk_recover')
    script_intercept = server_document('http://localhost:5006/bk_intercept')
    script_gc = server_document('http://localhost:5006/bk_gc')
    script_shots_cr = server_document('http://localhost:5006/bk_shots_cr')
    script_tackle_success = server_document('http://localhost:5006/bk_tackle_success')
    script_duels = server_document('http://localhost:5006/bk_duels')
    resources = INLINE.render()
    return render_template("stats_analysis.html", script_goals=Markup(script_goals),
                            script_assists=Markup(script_assists), script_long=Markup(script_long),
                            script_through=Markup(script_through), script_recover=Markup(script_recover),
                            script_intercept=Markup(script_intercept), script_gc=Markup(script_gc),
                            script_shots_cr=Markup(script_shots_cr), script_tackle_success=Markup(script_tackle_success),
                            script_duels=Markup(script_duels), template="Flask", resources=Markup(resources))

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    apps = {'/bk_goals': bk_goals,
            '/bk_assists': bk_assists,
            '/bk_through': bk_through,
            '/bk_long': bk_long,
            '/bk_recover': bk_recover,
            '/bk_intercept':bk_intercept,
            '/bk_gc':bk_gc,
            '/bk_shots_cr':bk_shots_cr,
            '/bk_tackle_success':bk_tackle_success,
            '/bk_duels':bk_duels}
    server = Server(apps, io_loop=IOLoop(), allow_websocket_origin=["localhost:5006"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

@app.route('/download/<player>', methods=["GET"])
def download(player):
    file = player_prof[player][3]

    player_data = pd.read_csv('player_data/'+file)
    
    resp = make_response(player_data.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + player + ".csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
