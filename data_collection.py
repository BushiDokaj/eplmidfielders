from bs4 import BeautifulSoup
import pandas as pd
import time
import selenium
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(chrome_options=options)

# list of all stats to pull
stats = ['appearances', 'goals', 'wins', 'losses', 'goals_per_game', 'att_pen_goal', 'att_freekick_goal',
 'total_scoring_att', 'ontarget_scoring_att', 'goal_assist', 'total_pass', 'total_pass_per_game', 'big_chance_created',
 'total_cross', 'cross_accuracy', 'total_through_ball', 'accurate_long_balls', 'tackle_success', 'total_tackle',
 'blocked_scoring_att', 'interception', 'total_clearance', 'ball_recovery', 'duel_won', 'duel_lost', 'won_contest',
 'aerial_won', 'aerial_lost', 'error_lead_to_goal']

# dict of all players and the years they played
players = {'Frank-Lampard':['1995/96', '1996/97', '1997/98', '1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15'],
            'Steven-Gerrard':['1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15'],
            'Paul-Scholes':['1994/95', '1995/96', '1996/97', '1997/98', '1998/99', '1999/00', '2000/01', '2001/02', '2002/03', '2003/04', '2004/05', '2005/06', '2006/07', '2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13'],
            'Xabi-Alonso':['2004/05', '2005/06', '2006/07', '2007/08', '2008/09'],
            'Yaya-Toure':[ '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18'],
            'Ngolo-Kante':['2015/16', '2016/17', '2017/18', '2018/19', '2019/20']
            }

# dict of players to their player id number for the url
player_to_id = {'Frank-Lampard': '800',
                'Steven-Gerrard': '1575',
                'Paul-Scholes': '336',
                'Xabi-Alonso': '2719',
                'Yaya-Toure': '4148',
                'Ngolo-Kante': '13492'
                }

# dict to convert the year in to the prem season number to complete the url
year_to_number = {'1992/93':'1',
                '1993/94':'2',
                '1994/95':'3', 
                '1995/96':'4', 
                '1996/97':'5', 
                '1997/98':'6', 
                '1998/99':'7', 
                '1999/00':'8', 
                '2000/01':'9', 
                '2001/02':'10', 
                '2002/03':'11', 
                '2003/04':'12', 
                '2004/05':'13', 
                '2005/06':'14', 
                '2006/07':'15', 
                '2007/08':'16', 
                '2008/09':'17', 
                '2009/10':'18', 
                '2010/11':'19', 
                '2011/12':'20', 
                '2012/13':'21',
                '2013/14':'22', 
                '2014/15':'27', 
                '2015/16':'42', 
                '2016/17':'54', 
                '2017/18':'79', 
                '2018/19':'210',
                '2019/20':'274'
                }

for player, years in players.items():
    pid = player_to_id[player]

    data = []
    for year in years:
        
        yid = year_to_number[year]
        
        url = 'https://www.premierleague.com/players/'+pid+'/'+player+'/stats?co=1&se='+yid
        
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        row = []
        for stat in stats:
            row.append(soup.find_all('span', attrs={'class':'stat'+stat})[0].getText().strip())
        
        data.append(row)

    table = pd.DataFrame(data, columns=stats)
    table['year'] = years
    table.to_csv(r'player_data\\'+player+'.csv', index=False)

