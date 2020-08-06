from app import app
from flask import render_template, request, jsonify, make_response, redirect, url_for, session
from scipy import stats
import pandas as pd
import numpy as np
import json
from math import sqrt

player_prof = None
with open('app\player_profiles.json', 'r', encoding='utf-8') as prof_file:
    player_prof = json.load(prof_file)


def confidence_interval(data, confidence):
    n = data.count()
    mean = data.mean()
    std = data.std()
    z = abs(stats.norm.ppf((1-confidence)/2))

    return [round(mean - z*(std/sqrt(n)), 1), round(mean + z*(std/sqrt(n)), 1)]


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
    player_data = pd.read_csv('player_data/'+file)

    # some summary statistics
    appearances = sum(player_data['appearances'])
    wins = sum(player_data['wins'])
    losses = sum(player_data['losses'])

    # creating the attack_data table, adding 5 new fields.
    attack_data = player_data.loc[:,('appearances', 'goals', 'goals_per_game', 'total_scoring_att', 'ontarget_scoring_att', 'goal_assist', 'year')]
    attack_data['shooting_accuracy'] = 100*(attack_data.loc[:,('ontarget_scoring_att')].divide(attack_data.loc[:,('total_scoring_att')]))
    attack_data['conversion_rate'] = 100*(attack_data.loc[:,('goals')].divide(attack_data.loc[:,('total_scoring_att')]))
    attack_data['assists_per_match'] = attack_data.loc[:,('goal_assist')].divide(player_data.loc[:,('appearances')])
    attack_data['goal_contributions'] = attack_data.loc[:,('goals')].add(attack_data.loc[:,('goal_assist')])
    attack_data['gc_per_match'] = attack_data.loc[:,('goal_contributions')].divide(player_data.loc[:,('appearances')])
    attack_data = attack_data.replace([np.inf, -np.inf], np.nan)
    attack_data.fillna(value=0, inplace=True)
    attack_data['assists_per_match'] = pd.Series([round(val, 2) for val in attack_data['assists_per_match']])
    attack_data['gc_per_match'] = pd.Series([round(val, 2) for val in attack_data['gc_per_match']])
    attack_data['shooting_accuracy'] = pd.Series(["{0:.0f}%".format(val) for val in attack_data['shooting_accuracy']])
    attack_data['conversion_rate'] = pd.Series(["{0:.0f}%".format(val) for val in attack_data['conversion_rate']])
    
    # creating the team play table
    team_play_data = player_data[player_data.year >= "2006/07"].loc[:,('appearances', 'total_pass', 'total_pass_per_game', 'big_chance_created', 'total_cross', 'cross_accuracy',
                                    'total_through_ball', 'accurate_long_balls', 'year')]

    # creating the defense table
    defensive_data = player_data[player_data.year >= "2006/07"].loc[:,('appearances', 'total_tackle', 'tackle_success', 'blocked_scoring_att', 'interception', 'total_clearance', 'ball_recovery',
                                    'duel_won', 'duel_lost', 'won_contest', 'aerial_won', 'aerial_lost', 'error_lead_to_goal', 'year')]

    desc_stats = {
    # descriptive attack statistics
    "avg_goals": round(attack_data['goals'].mean(), 1),
    "max_goals": attack_data['goals'].max(),
    "ci_goals": confidence_interval(attack_data['goals'], 0.9),
    "avg_assists": round(attack_data['goal_assist'].mean(), 1),
    "max_assists": attack_data['goal_assist'].max(),
    "ci_assists": confidence_interval(attack_data['goal_assist'], 0.9),
    "avg_gc": round(attack_data['goal_contributions'].mean(), 1),
    "max_gc": attack_data['goal_contributions'].max(),
    "ci_gc": confidence_interval(attack_data['goal_contributions'], 0.9),
    "avg_cr": round(attack_data['conversion_rate'].str.replace('%','').astype('int').mean(), 1),
    "max_cr": attack_data['conversion_rate'].str.replace('%','').astype('int').max(),
    "ci_cr": confidence_interval(attack_data['conversion_rate'].str.replace('%','').astype('int'), 0.9),
    # descriptive team play statistics
    "avg_ppg": round(team_play_data['total_pass_per_game'].mean(), 1),
    "max_ppg": team_play_data['total_pass_per_game'].max(),
    "ci_ppg": confidence_interval(team_play_data['total_pass_per_game'], 0.9),
    "avg_ca": round(team_play_data['cross_accuracy'].str.replace('%','').astype('int').mean(), 1),
    "max_ca": team_play_data['cross_accuracy'].str.replace('%','').astype('int').max(),
    "ci_ca": confidence_interval(team_play_data['cross_accuracy'].str.replace('%','').astype('int'), 0.9),
    "avg_through":round(team_play_data['total_through_ball'].mean(), 1),
    "max_through": team_play_data['total_through_ball'].max(),
    "ci_through": confidence_interval(team_play_data['total_through_ball'], 0.9),
    "avg_long": round(team_play_data['accurate_long_balls'].mean(), 1),
    "max_long": team_play_data['accurate_long_balls'].max(),
    "ci_long": confidence_interval(team_play_data['accurate_long_balls'], 0.9),
    # descriptive defense statistics
    "avg_tackles": round(defensive_data['total_tackle'].mean(), 1),
    "max_tackles": defensive_data['total_tackle'].max(),
    "ci_tackles": confidence_interval(defensive_data['total_tackle'], 0.9),
    "avg_int": round(defensive_data['interception'].mean(), 1),
    "max_int": defensive_data['interception'].max(),
    "ci_int": confidence_interval(defensive_data['interception'], 0.9),
    "avg_clear": round(defensive_data['total_clearance'].mean(), 1),
    "max_clear": defensive_data['total_clearance'].max(),
    "ci_clear": confidence_interval(defensive_data['total_clearance'], 0.9),
    "avg_rec": round(defensive_data['ball_recovery'].mean(), 1),
    "max_rec": defensive_data['ball_recovery'].max(),
    "ci_rec": confidence_interval(defensive_data['ball_recovery'], 0.9)
    }

    return render_template('profile.html',player=player, title=title, accolades=accolades, quote=quote[0], said_it=quote[1], 
                            img=img, appearances=appearances, wins=wins, losses=losses, attack_data=attack_data.to_dict('record'),
                            team_play_data=team_play_data.to_dict('record'), defensive_data=defensive_data.to_dict('record'),
                            desc_stats=desc_stats)

@app.route('/download/<player>', methods=["GET"])
def download(player):
    file = player_prof[player][3]

    player_data = pd.read_csv('player_data/'+file)
    
    resp = make_response(player_data.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=" + player + ".csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
