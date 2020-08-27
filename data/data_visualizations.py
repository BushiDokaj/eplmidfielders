import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import layout, column
from bokeh.themes import Theme
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Select, Legend, CategoricalColorMapper, CheckboxButtonGroup, CustomJS
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.document import Document
from math import exp
from .data_aggregate import attack, team_play, defensive, combined

players = ["Frank-Lampard", "Ngolo-Kante", "Paul-Scholes", "Steven-Gerrard", "Xabi-Alonso", "Yaya-Toure"]
colours={'Frank Lampard': '#496cc3',
            'Steven Gerrard': '#00a499',
            'Xabi Alonso':'#4b3291',
            'Ngolo Kante': '#fcb50b',
            'Paul Scholes': '#db0006',
            'Yaya Toure':'#98c2e8'
}

def bk_scatter(stat_one, stat_one_name, stat_two, stat_two_name, stat='goal_contributions', stat_name='Goal Contributions'):

    mapper = CategoricalColorMapper(
        palette=['#496cc3', '#00a499', '#4b3291', '#fcb50b', '#db0006', '#98c2e8'],
        factors=["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"]
        )

    LABELS = ["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"]
    checkbox_button_group = CheckboxButtonGroup(labels=LABELS)

    TOOLTIPS = [
        ('Player', '@name'),
        ('Season', '@year'),
        ('Appearances', '@appearances'),
        (stat_one_name, '@'+stat_one),
        (stat_two_name, '@'+stat_two)
    ]

    if stat_name == 'Goal Contributions':
        TOOLTIPS.append((stat_name, '@'+stat))

    PLOT_OPTIONS = dict(plot_width=950, plot_height=450)

    p = figure(
        title="Comparison of " + stat_name + " Recorded in a Season",
        x_axis_label=stat_one_name,
        y_axis_label=stat_two_name,
        tools='pan,zoom_in,zoom_out,save,reset',
        tooltips=TOOLTIPS,
        **PLOT_OPTIONS
    )

    p.add_layout(Legend(), 'right')

    # for player in players:   
    if stat_one_name in ['Assists', 'Total Shots']:
        df = combined('attack')
    if stat_one_name=='Total Passes':
        df = combined('team_play')
    if stat_one_name in ['Total Tackles', 'Duels Won']:
        df = combined('defensive')

    if stat_one_name=='Total Shots':
        df = df[df.year >= '2006/07']

    df['size'] = [1.3*exp(0.09*val) for val in df['appearances']]
    df['fill'] = 0.8
    df['line'] = 1

    if stat_one_name in ['Total Shots', 'Total Tackles']:
        df[stat_two] = df[stat_two].str.replace('%','').astype('int')

    if stat_one_name=='Total Passes':
        df['total_pass'] = df['total_pass'].str.replace(',','').astype('int')

    source = ColumnDataSource(df)
    
    p.circle(
        x=stat_one,
        y=stat_two,
        source=source,
        legend_group='name',
        size='size',
        fill_alpha='fill',
        line_color='#7c7e71',
        line_width=0.5,
        line_alpha='line',
        color={'field':'name', 'transform': mapper}
    )

    # p.legend.click_policy = 'mute' 
    p.grid.grid_line_dash = [6, 4]

    checkbox_button_group.js_on_click(CustomJS(args=dict(source=source), code="""
            var labels = ["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"];
            
            var ind;
            var act = [];
            var t = this.active
            console.log(t);
            for (ind in t) {
                console.log(t[ind])
                act.push(labels[t[ind]]);
            }
            var data=source.data;
            var name = data['name'];
            var fill = data['fill'];
            var line = data['line'];

            for (var i = 0; i < name.length; i++) {   
                if (act.includes(name[i]))  {
                    fill[i] = 0.1;
                    line[i] = 0.1;
                } else {
                    fill[i] = 0.8;
                    line[i] = 1;
                }
            }
            source.change.emit();    
        """))

    l = layout(column(p,checkbox_button_group))

    return l

def bk_gc():
    return bk_scatter('goal_assist', 'Assists', 'goals', 'Goals')

def bk_shots_cr():
    return bk_scatter('total_scoring_att', 'Total Shots', 'conversion_rate', 'Conversion Rate (%)', stat_name='Total Shots Taken by Converson Rate')

def bk_tackle_success():
    return bk_scatter('total_tackle', 'Total Tackles', 'tackle_success', 'Tackle Success (%)', stat_name='Total Tackles by Tackle Success')

def bk_duels():
    return bk_scatter('duel_won', 'Duels Won', 'duel_lost', 'Duels Lost', stat_name='Duels Won by Duels Lost')

def bk_passes():
    return bk_scatter('total_pass', 'Total Passes','total_pass_per_game','Passes per Match', stat_name="Passes by Passes/Match")



def bk_line(stat, stat_name):
    mapper = CategoricalColorMapper(
        palette=['#496cc3', '#00a499', '#4b3291', '#fcb50b', '#db0006', '#98c2e8'],
        factors=["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"]
        )

    LABELS = ["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"]
    checkbox_button_group = CheckboxButtonGroup(labels=LABELS)

    year = ['1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18',  '2018/19', '2019/20']
    if stat_name=='Through Balls' or stat_name=='Recoveries':
        year = year[13:]
    elif stat_name=='Long Balls' or stat_name=='Interceptions':
        year = year[12:]

    TOOLTIPS = [
        ('Player', '@name'),
        ('Season', '@year'),
        ('Appearances', '@appearances'),
        (stat_name, '@'+stat)
    ]

    PLOT_OPTIONS = dict(plot_width=950, plot_height=450)

    p = figure(
        x_range=year,
        title="Comparison of " + stat_name + " Recorded in a Season",
        x_axis_label="Season",
        y_axis_label=stat_name,
        tools='pan,zoom_in,zoom_out,save,reset',
        tooltips=TOOLTIPS,
        **PLOT_OPTIONS
    )

    p.add_layout(Legend(), 'right')

    if stat in ['goals', 'goal_assist']:
        df = combined('attack')
    if stat in ['total_through_ball', 'accurate_long_balls']:
        df = combined('team_play')
    if stat in ['ball_recovery', 'interception']:
        df = combined('defensive')

    df['size'] = [1.3*exp(0.09*val) for val in df['appearances']]
    df['fill'] = 0.8
    df['line'] = 1


    source = ColumnDataSource(df)

    p.circle(
        x='year',
        y=stat,
        source=source,
        legend_group='name',
        size='size',
        fill_alpha='fill',
        line_color='#7c7e71',
        line_width=0.5,
        line_alpha='line',
        color={'field':'name', 'transform': mapper}
    )

    p.xaxis.major_label_orientation = 1.5
    p.grid.grid_line_dash = [6, 4]

    checkbox_button_group.js_on_click(CustomJS(args=dict(source=source), code="""
            var labels = ["Frank Lampard", "Steven Gerrard", "Xabi Alonso", "Ngolo Kante", "Paul Scholes", "Yaya Toure"];
            
            var ind;
            var act = [];
            var t = this.active
            console.log(t);
            for (ind in t) {
                console.log(t[ind])
                act.push(labels[t[ind]]);
            }
            var data=source.data;
            var name = data['name'];
            var fill = data['fill'];
            var line = data['line'];

            for (var i = 0; i < name.length; i++) {   
                if (act.includes(name[i]))  {
                    fill[i] = 0.1;
                    line[i] = 0.1;
                } else {
                    fill[i] = 0.8;
                    line[i] = 1;
                }
            }
            source.change.emit();    
        """))

    l = layout(column(p,checkbox_button_group)) 

    return l

def bk_goals():
    return bk_line('goals', 'Goals')

def bk_assists():
    return bk_line('goal_assist', 'Assists')

def bk_through():
    return bk_line('total_through_ball', 'Through Balls')

def bk_long():
    return bk_line('accurate_long_balls', 'Long Balls')

def bk_recover():
    return bk_line('ball_recovery', 'Recoveries')

def bk_intercept():
    return bk_line('interception', 'Interceptions')
