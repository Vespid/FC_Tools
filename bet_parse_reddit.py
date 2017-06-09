# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 01:05:44 2017

@author: Vincent
"""

#retrieves all reddit bets and compares results
import food_tools as ft
import requests, bs4
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

##############################
rnd=6607
url="https://www.reddit.com/r/neopets/comments/6fx3qd/food_club_bets_june_08_2017/"
##############################
#retrives round winners
#a,o,p,w=ft.get_past_data(rnd)
#winners=[ft.nicknames[x] for x in w]
#
##retrieves all reddit bets
#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#res=requests.get(url, headers=headers)
#res.raise_for_status()
#soup=bs4.BeautifulSoup(res.text, "lxml")

##Comment above to use cached data
bettors_soup=soup.select('div[data-type="comment"]')
bettors=[]; bet_sets=[]; nonbettors=[]
for x in range(len(bettors_soup)):
    bettors.append(bettors_soup[x].get('data-author'))
    try:
        bet_df=pd.read_html(str(bettors_soup[x].select('table')),index_col=0)
#        bet_df[0].drop(bet_df[0].index[0],inplace=True)
        bet_df[0].fillna("", inplace=True)
        bet_df[0]["Odds"]=bet_df[0]["Odds"].str[:-2].astype(int)
        bet_sets.append(bet_df[0])
    except ValueError:
        bet_sets.append(None)
        nonbettors.append(x)
        
new_sets = [v for i, v in enumerate(bet_sets) if i not in nonbettors]
new_bettors = [v for i, v in enumerate(bettors) if i not in nonbettors]

payout=[]
for bets in new_sets:
    payout.append(ft.calc_winnings(bets,winners))

for x in range(len(new_bettors)):
    print(new_bettors[x],"%d:10" % payout[x])
 
#displays results in table
tble=pd.DataFrame(payout,new_bettors)
tarray=np.array([new_bettors,payout]).transpose()
asscheeks=pd.DataFrame(tarray)
asscheeks.columns=["Bettor","Payout"]
render_mpl_table(asscheeks, header_columns=0, col_width=2.0)

#pickles result
reddit_file=open("reddit_bets.pickle","rb")
reddit_results = pickle.load(reddit_file)
reddit_file.close()
reddit_results[rnd]=tble
reddit_file=open("reddit_bets.pickle","wb")
pickle.dump(reddit_results, reddit_file)
reddit_file.close()