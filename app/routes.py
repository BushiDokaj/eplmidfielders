from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session
import pandas as pd
import numpy as np
import json

player_prof = None
with open('app\player_profiles.json', 'r', encoding='utf-8') as prof_file:
    player_prof = json.load(prof_file)

@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    return render_template('home.html')

@app.route('/profile/<player>', methods=["GET"])
def profile(player):
    
    title = player_prof[player][0]
    accolades = player_prof[player][1]
    quote = player_prof[player][2]
    file = player_prof[player][3]

    img = 'images/' + player.split('_')[0] + '_profile.jpg'

    player_data = pd.read_csv('player_data/'+file)

    appearances = sum(player_data['appearances'])
    wins = sum(player_data['wins'])
    losses = sum(player_data['losses'])

    attack_data = player_data.loc[:,('appearances', 'goals', 'goals_per_game', 'total_scoring_att', 'ontarget_scoring_att', 'goal_assist', 'year')]
    attack_data['shooting_accuracy'] = 100*(attack_data.loc[:,('ontarget_scoring_att')].divide(attack_data.loc[:,('total_scoring_att')]))
    attack_data['conversion_rate'] = 100*(attack_data.loc[:,('goals')].divide(attack_data.loc[:,('total_scoring_att')]))
    attack_data['assists_per_match'] = attack_data.loc[:,('goal_assist')].divide(player_data.loc[:,('appearances')])
    attack_data['goal_contributions'] = attack_data.loc[:,('goals')].add(attack_data.loc[:,('goal_assist')])
    attack_data['gc_per_match'] = attack_data.loc[:,('goal_contributions')].divide(player_data.loc[:,('appearances')])
    attack_data = attack_data.replace([np.inf, -np.inf], np.nan)
    attack_data.fillna(value=0, inplace=True)
    
    team_play_data = player_data.loc[:,('appearances', 'total_pass', 'total_pass_per_game', 'big_chance_created', 'total_cross', 'cross_accuracy',
                                    'total_through_ball', 'accurate_long_balls', 'year')]

    defensive_data = player_data.loc[:,('appearances', 'total_tackle', 'tackle_success', 'blocked_scoring_att', 'interception', 'total_clearance', 'ball_recovery',
                                    'duel_won', 'duel_lost', 'won_contest', 'aerial_won', 'aerial_lost', 'error_lead_to_goal', 'year')]


    return render_template('profile.html',player=player, title=title, accolades=accolades, quote=quote[0], said_it=quote[1], 
                            img=img, appearances=appearances, wins=wins, losses=losses, attack_data=attack_data.to_dict('record'),
                            team_play_data=team_play_data.to_dict('record'), defensive_data=defensive_data.to_dict('record'))
