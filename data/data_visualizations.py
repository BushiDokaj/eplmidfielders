import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.themes import Theme
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.document import Document
from math import exp
from .data_aggregate import attack, team_play, defensive

players = ["Frank-Lampard", "Ngolo-Kante", "Paul-Scholes", "Steven-Gerrard", "Xabi-Alonso", "Yaya-Toure"]
colours={'Frank Lampard': '#496cc3',
            'Steven Gerrard': '#00a499',
            'Xabi Alonso':'#4b3291',
            'Ngolo Kante': '#fcb50b',
            'Paul Scholes': '#db0006',
            'Yaya Toure':'#98c2e8'
}

def bk_scatter(doc, stat_one, stat_one_name, stat_two, stat_two_name, stat='goal_contributions', stat_name='Goal Contributions'):
    p_select = Select(
        title="Select Player",
        value="All",
        options=['All', 'Frank Lampard', 'Steven Gerrard', 'Ngolo Kante', 'Paul Scholes', 'Xabi Alonso', 'Yaya Toure']
    )

    TOOLTIPS = [
        ('Player', '@name'),
        ('Season', '@year'),
        ('Appearances', '@appearances'),
        (stat_one_name, '@'+stat_one),
        (stat_two_name, '@'+stat_two)
    ]

    if stat_name == 'Goal Contributions':
        TOOLTIPS.append((stat_name, '@'+stat))

    PLOT_OPTIONS = dict(plot_width=800, plot_height=400)

    p = figure(
        title="Comparison of " + stat_name + " Recorded in a Season",
        x_axis_label=stat_one_name,
        y_axis_label=stat_two_name,
        tools='pan,zoom_in,zoom_out,reset',
        tooltips=TOOLTIPS,
        **PLOT_OPTIONS
    ) 
    
    player_circles = {}

    for player in players:   
        if stat_one_name in ['Assists', 'Total Shots']:
            df = attack(player+'.csv')
        if stat_one_name in ['Total Tackles', 'Duels Won']:
            df = defensive(player+'.csv')

        if stat_one_name=='Total Shots':
            df = df[df.year >= '2006/07']

        df['size'] = [exp(0.09*val) for val in df['appearances']]

        name = player.replace('-', ' ')
        df['name'] = name

        if stat_one_name in ['Total Shots', 'Total Tackles']:
            df[stat_two] = df[stat_two].str.replace('%','').astype('int')

        source = ColumnDataSource(df)
        
        player_circles[player] = p.circle(
            x=stat_one,
            y=stat_two,
            source=source,
            legend_label=name,
            size='size',
            fill_alpha=0.8,
            line_color='#7c7e71',
            line_width=0.5,
            line_alpha=1,
            color=colours[name]
        )

    def select_update(attrname, old, new):
        players = ["Frank-Lampard", "Ngolo-Kante", "Paul-Scholes", "Steven-Gerrard", "Xabi-Alonso", "Yaya-Toure"]
        player_select = p_select.value

        if player_select == "All":
            for player in players:
                player_circles[player].glyph.fill_alpha=0.8
                player_circles[player].glyph.line_alpha=1
        else:
            if old=="All":
                player_select = player_select.replace(' ', '-')
                players.remove(player_select)
                for player in players:
                    player_circles[player].glyph.fill_alpha=0.1
                    player_circles[player].glyph.line_alpha=0.1
            else:
                player_select = player_select.replace(' ', '-')
                player_circles[player_select].glyph.fill_alpha=0.8
                player_circles[player_select].glyph.line_alpha=1

                old = old.replace(' ', '-')
                player_circles[old].glyph.fill_alpha=0.1
                player_circles[old].glyph.line_alpha=0.1

    p_select.on_change('value', select_update)

    doc.add_root(layout([p], sizing_mode='scale_both'))
    doc.add_root(layout([[p_select]]))
    doc.theme = Theme(filename="theme.yaml")

def bk_gc(doc):
    bk_scatter(doc, 'goal_assist', 'Assists', 'goals', 'Goals')

def bk_shots_cr(doc):
    bk_scatter(doc, 'total_scoring_att', 'Total Shots', 'conversion_rate', 'Conversion Rate (%)', stat_name='Total Shots Taken by Converson Rate')

def bk_tackle_success(doc):
    bk_scatter(doc, 'total_tackle', 'Total Tackles', 'tackle_success', 'Tackle Success', stat_name='Total Tackles by Tackle Success')

def bk_duels(doc):
    bk_scatter(doc, 'duel_won', 'Duels Won', 'duel_lost', 'Duels Lost', stat_name='Duels Won by Duels Lost')




def bk_line(doc, stat, stat_name):
    year = ['1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18',  '2018/19', '2019/20']
    if stat_name=='Through Balls' or stat_name=='Recoveries':
        year = year[13:]
    elif stat_name=='Long Balls' or stat_name=='Interceptions':
        year = year[12:]

    p_select = Select(
        title="Select Player",
        value="All",
        options=['All', 'Frank Lampard', 'Steven Gerrard', 'Ngolo Kante', 'Paul Scholes', 'Xabi Alonso', 'Yaya Toure']
    )

    TOOLTIPS = [
        ('Player', '@name'),
        ('Season', '@year'),
        ('Appearances', '@appearances'),
        (stat_name, '@'+stat)
    ]

    PLOT_OPTIONS = dict(plot_width=800, plot_height=400)

    p = figure(
        x_range=year,
        title="Comparison of " + stat_name + " Recorded in a Season",
        x_axis_label="Season",
        y_axis_label=stat_name,
        tools='pan,zoom_in,zoom_out,reset',
        tooltips=TOOLTIPS,
        **PLOT_OPTIONS
    )

    player_lines = {}
    player_circles = {}

    for player in players:
        df = pd.read_csv('player_data/' + player + '.csv')
        
        df['size'] = pd.Series([exp(0.09*val) for val in df['appearances']])

        name = player.replace('-', ' ')
        df['name'] = name

        source = ColumnDataSource(df)

        player_circles[player] = p.circle(
            x='year',
            y=stat,
            source=source,
            legend_label=name,
            size='size',
            fill_alpha=0.8,
            line_color='#7c7e71',
            line_width=0.5,
            line_alpha=1,
            color=colours[name]
        )

    def select_update(attrname, old, new):
        players = ["Frank-Lampard", "Ngolo-Kante", "Paul-Scholes", "Steven-Gerrard", "Xabi-Alonso", "Yaya-Toure"]
        player_select = p_select.value

        if player_select == "All":
            for player in players:
                player_circles[player].glyph.fill_alpha=0.8
                player_circles[player].glyph.line_alpha=1
        else:
            if old=="All":
                player_select = player_select.replace(' ', '-')
                players.remove(player_select)
                for player in players:
                    player_circles[player].glyph.fill_alpha=0.1
                    player_circles[player].glyph.line_alpha=0.1
            else:
                player_select = player_select.replace(' ', '-')
                player_circles[player_select].glyph.fill_alpha=0.8
                player_circles[player_select].glyph.line_alpha=1

                old = old.replace(' ', '-')
                player_circles[old].glyph.fill_alpha=0.1
                player_circles[old].glyph.line_alpha=0.1

    p.xaxis.major_label_orientation = 1.5
    p_select.on_change('value', select_update)

    doc.add_root(layout([p], sizing_mode='scale_both'))
    doc.add_root(layout([[p_select]]))
    doc.theme = Theme(filename="theme.yaml")


def bk_goals(doc):
    bk_line(doc, 'goals', 'Goals')

def bk_assists(doc):
    bk_line(doc, 'goal_assist', 'Assists')

def bk_through(doc):
    bk_line(doc, 'total_through_ball', 'Through Balls')

def bk_long(doc):
    bk_line(doc, 'accurate_long_balls', 'Long Balls')

def bk_recover(doc):
    bk_line(doc, 'ball_recovery', 'Recoveries')

def bk_intercept(doc):
    bk_line(doc, 'interception', 'Interceptions')



