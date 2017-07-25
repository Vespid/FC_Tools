# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 01:05:44 2017
 
@author: Dogboy
"""
#Objective: retrieves all reddit bets and compares results
 
#####To-Do#####
#1. get payouts from daqtools instead of from user tables
#2. handle alternate names (eg. Pip vs Bonnie)
 
import requests, bs4 #for retrieving site data
import pickle #for storing data
import pandas as pd #for creating dataframes to analyze data
import numpy as np
import matplotlib.pyplot as plt #for visualizing data
import six #part of table function
 
#pirate nicknames per diceroll's userscript
nicknames={
    "Federismo Corvallio": 'Federismo',
    "Bonnie Pip Culliford": 'Bonnie',
    "Puffo the Waister": 'Puffo',
    "Orvinn the First Mate": 'Orvinn',
    "Scurvy Dan the Blade": 'Dan',
    "Young Sproggie": 'Sproggie',
    "Squire Venable": 'Squire',
    "Ol' Stripey": 'Stripey',
    "Captain Crossblades": 'Crossblades',
    "Franchisco Corvallio": 'Franchisco',
    "Admiral Blackbeard": 'Blackbeard',
    "Gooblah the Grarrl": 'Gooblah',
    "Lucky McKyriggan": 'Lucky',
    "Fairfax the Deckhand": 'Fairfax',
    "Sir Edmund Ogletree": 'Edmund',
    "The Tailhook Kid": 'Tailhook',
    "Stuff-A-Roo": 'Stuff',
    "Buck Cutlass": 'Buck',
    "Peg Leg Percival": 'Peg Leg',
    "Ned the Skipper": 'Ned',
}
 
#function makes a pretty table copied from stackoverflow
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
 
def get_winners(rnd):
    res=requests.get("http://foodclub.daqtools.info/History.php?round=%d" % rnd)
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'lxml')
    if "No Data" in soup.select("div[id='body']")[0].text:
        return  
    winElems=soup.select('.winner')
    if len(winElems)!=0:
        winners=[x.text for x in winElems]
    else:
        winners=[]
    return winners
 
def calc_winnings(bets,winners):    
    winnings=[]
    result=winners
    for y in range(0,len(bets)):
        bet = list(filter(None, list(bets.iloc[y,0:5])))
        if set(bet).issubset(set(result)):
            winnings.append(bets.iloc[y,5])
    pay=sum(winnings)
    return pay
 
###############################################
#####User Input - Modify for daily results#####
rnd=6623
url="https://www.reddit.com/r/neopets/comments/6j4qz7/food_club_bets_june_24_2017/"
###############################################
#retrives round winners
w=get_winners(rnd) #retrieve arenas, odds, payouts, winners from daqtools
winners=[nicknames[x] for x in w] #converts pirate full names to shorthand names
 
#retrieves all reddit bets
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res=requests.get(url, headers=headers)  #request reddit page
res.raise_for_status()  #verify web page
soup=bs4.BeautifulSoup(res.text, "lxml") #convert to html source code
 
##Comment above to use cached data
 
#Finds all reddit comments with bets
bettors_soup=soup.select('div[data-type="comment"]') #find and create list of all reddit comments
bettors=[]; bet_sets=[]; nonbettors=[] #bettors- reddit commentors, bet_sets=bet tables, nonbettors-indices with no table/invalid bet format
for x in range(len(bettors_soup)): #loop through all reddit comments
    bettors.append(bettors_soup[x].get('data-author')) #save name of all commentors
    try: #try to find table in comment - extract pirates and payouts
        bet_df=pd.read_html(str(bettors_soup[x].select('table')),index_col=0)
        bet_df[0].fillna("", inplace=True)
        bet_df[0]["Odds"]=bet_df[0]["Odds"].str[:-2].astype(int)
        bet_sets.append(bet_df[0])
    except ValueError: #stores None in bet_set addes index to nonbettors if invalid format
        bet_sets.append(None)
        nonbettors.append(x)
 
#create new lists with only valid bet tables        
new_sets = [v for i, v in enumerate(bet_sets) if i not in nonbettors]
new_bettors = [v for i, v in enumerate(bettors) if i not in nonbettors]
 
#calculates payout based on payouts column in reddit table
payout=[]
for bets in new_sets:
    payout.append(calc_winnings(bets,winners))
 
#print total payout of all bettors in text
for x in range(len(new_bettors)):
    print(new_bettors[x],"%d:10" % payout[x])
 
#displays results in table
tble=pd.DataFrame(payout,new_bettors)
tarray=np.array([new_bettors,payout]).transpose()
asscheeks=pd.DataFrame(tarray)
asscheeks.columns=["Bettor","Payout"]
render_mpl_table(asscheeks, header_columns=0, col_width=2.0)
 
#saves result - work in progress
#reddit_file=open("reddit_bets.pickle","rb")
#reddit_results = pickle.load(reddit_file)
#reddit_file.close()
#reddit_results[rnd]=tble
#reddit_file=open("reddit_bets.pickle","wb")
#pickle.dump(reddit_results, reddit_file)
#reddit_file.close()