import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.themes import Theme
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.embed import components
from bokeh.resources import INLINE
from math import exp

players = ["Frank-Lampard", "Ngolo-Kante", "Paul-Scholes", "Steven-Gerrard", "Xabi-Alonso", "Yaya-Toure"]
colours={'Frank Lampard': '#496cc3',
            'Steven Gerrard': '#00a499',
            'Xabi Alonso':'#4b3291',
            'Ngolo Kante': '#fcb50b',
            'Paul Scholes': '#db0006',
            'Yaya Toure':'#98c2e8'
}
year = ['1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18',  '2018/19', '2019/20']

def bk_goals(doc):
    p_select = Select(
        title="Select Player",
        value="All",
        options=['All', 'Frank Lampard', 'Steven Gerrard', 'Ngolo Kante', 'Paul Scholes', 'Xabi Alonso', 'Yaya Toure']
    )

    TOOLTIPS = [
        ('Player', '@name'),
        ('Season', '@year'),
        ('Appearances', '@appearances'),
        ('Goals', '@goals')
    ]

    p = figure(
        x_range=year,
        title="Comparison of Goals Scored in a Season",
        x_axis_label="Season",
        y_axis_label="Goals Scored",
        tools='pan,box_select,zoom_in,zoom_out,save,reset',
        tooltips=TOOLTIPS
    )

    player_lines = {}
    player_circles = {}

    for player in players:
        df = pd.read_csv('player_data/' + player + '.csv')
        df['size'] = pd.Series([exp(0.09*val) for val in df['appearances']])

        name = player.replace('-', ' ')
        df['name'] = name
        source = ColumnDataSource(df)

        player_lines[player] = p.line(
            x='year', 
            y='goals',
            source=source,
            legend_label=name, 
            line_width=3,
            line_alpha=0.5,
            color=colours[name]
        )

        player_circles[player] = p.circle(
            x='year',
            y='goals',
            source=source,
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
                player_lines[player].glyph.line_alpha=0.5
                player_circles[player].glyph.fill_alpha=0.8
                player_circles[player].glyph.line_alpha=1
        else:
            if old=="All":
                player_select = player_select.replace(' ', '-')
                players.remove(player_select)
                for player in players:
                    player_lines[player].glyph.line_alpha=0.1
                    player_circles[player].glyph.fill_alpha=0.1
                    player_circles[player].glyph.line_alpha=0.1
            else:
                player_select = player_select.replace(' ', '-')
                player_lines[player_select].glyph.line_alpha=0.5
                player_circles[player_select].glyph.fill_alpha=0.8
                player_circles[player_select].glyph.line_alpha=1

                old = old.replace(' ', '-')
                player_lines[old].glyph.line_alpha=0.1
                player_circles[old].glyph.fill_alpha=0.1
                player_circles[old].glyph.line_alpha=0.1

    p.xaxis.major_label_orientation = 1/3
    p_select.on_change('value', select_update)

    doc.add_root(column(p_select, p))
    doc.theme = Theme(filename="theme.yaml")