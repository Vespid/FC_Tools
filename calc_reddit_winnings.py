import requests, bs4 #for retrieving site data
import pickle #for storing data
import pandas as pd #for creating dataframes to analyze data
import numpy as np
import matplotlib.pyplot as plt #for visualizing data
import food_tools as ft

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

real_names={'Blackbeard': 'Admiral Blackbeard',
 'Bonnie': 'Bonnie Pip Culliford',
 'Buck': 'Buck Cutlass',
 'Crossblades': 'Captain Crossblades',
 'Dan': 'Scurvy Dan the Blade',
 'Edmund': 'Sir Edmund Ogletree',
 'Fairfax': 'Fairfax the Deckhand',
 'Federismo': 'Federismo Corvallio',
 'Franchisco': 'Franchisco Corvallio',
 'Gooblah': 'Gooblah the Grarrl',
 'Lucky': 'Lucky McKyriggan',
 'Ned': 'Ned the Skipper',
 'Orvinn': 'Orvinn the First Mate',
 'Peg Leg': 'Peg Leg Percival',
 'Puffo': 'Puffo the Waister',
 'Sproggie': 'Young Sproggie',
 'Squire': 'Squire Venable',
 'Stripey': "Ol' Stripey",
 'Stuff': 'Stuff-A-Roo',
 'Tailhook': 'The Tailhook Kid'}

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
    a,o,p,oo,r,fa,win_data,f,alg,est=ft.load_all_data(rnd)
    winnings=[]
    result=winners
    for y in range(0,len(bets)):
        bet = list(filter(None, list(bets.iloc[y,0:5])))
        if set(bet).issubset(set(result)):
            lol=1
            for x in bet:
                lol*=p[x]
            winnings.append(lol)
    pay=sum(winnings)
    return pay

#for rnd in range(6657,6658):
#    ft.get_past_data(rnd)


url="https://www.reddit.com/user/Dwindleman/"
url="https://www.reddit.com/user/Dwindleman/?count=25&after=t1_djyjgfh"


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
res=requests.get(url, headers=headers)  #request reddit page
res.raise_for_status()  #verify web page
soup=bs4.BeautifulSoup(res.text, "lxml") #convert to html source code

bet_df=pd.read_html(str(soup),index_col=0)
#copy=bet_df.copy()

for x in range(len(bet_df)):
    bet_df[x].fillna("", inplace=True)
    try:
        bet_df[x]["Odds"]=bet_df[x]["Odds"].str[:-2].astype(int)
    except KeyError:
        continue
    for y in bet_df[x].columns[0:5]:
        bet_df[x].replace({y: real_names}, inplace=True)
    rnd=int(bet_df[x].index.name)
    w=get_winners(rnd) #retrieve arenas, odds, payouts, winners from daqtools
#    winners=[nicknames[x] for x in w] #converts pirate full names to shorthand names          
    payout=calc_winnings(bet_df[x], w)
    print(rnd, payout)          