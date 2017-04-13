import pickle, bs4, requests
import pandas as pd
import numpy as np

import time


#Downloads data from daqtools and writes to pickle
def get_past_data(rnd):
    win_file=open("fcwin_data.pickle","rb")
    win_data = pickle.load(win_file)
    if rnd in list(win_data.keys()):
        win_file.close()
        return
    win_file.close()
    res=requests.get("http://foodclub.daqtools.info/History.php?round=%d" % rnd)
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'lxml')
    if "No Data" in soup.select("div[id='body']")[0].text:
        return   
    winElems=soup.select('.winner')
    winners=[x.text for x in winElems]
    test=soup.select("td")
    names=[1,11,20,29,40,50,59,68,79,89,98,107,118,128,137,146,157,167,176,185]
    opening_odds=[x+5 for x in names]
    current_odds=[x+6 for x in names]
    
    Pirates=[test[x].text for x in names]
    Percent=[int(test[x].text[:-2]) for x in opening_odds]
    Payout=[int(test[x].text[:-2]) for x in current_odds]
    
    Shipwreck=Pirates[0:4]
    Lagoon=Pirates[4:8]
    Treasure_Island=Pirates[8:12]
    Hidden_Cove=Pirates[12:16]
    Harpoon_Harry=Pirates[16:20]
    
    roundData=[Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]
    OddsData={}; PayoutData={}
    for x in range(len(Pirates)):
        OddsData[Pirates[x]]=Percent[x]
        PayoutData[Pirates[x]]=Payout[x]

    Arena_file=open("ArenaData.pickle","rb")
    Arenas = pickle.load(Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","rb")
    Odds = pickle.load(Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","rb")
    Payouts = pickle.load(Payouts_file)
    Payouts_file.close()
    
    Arenas[rnd]=roundData
    Payouts[rnd]=PayoutData
    Odds[rnd]=OddsData
    win_data[rnd]=winners  
           
    Arena_file=open("ArenaData.pickle","wb")
    pickle.dump(Arenas, Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","wb")
    pickle.dump(Odds, Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","wb")
    pickle.dump(Payouts, Payouts_file)
    Payouts_file.close()
    
    win_file=open("fcwin_data.pickle","wb")
    pickle.dump(win_data, win_file)
    win_file.close()
    return Arenas[rnd], Odds[rnd], Payouts[rnd], winners

def load_past_data(rnd):
    Arena_file=open("ArenaData.pickle","rb")
    Arenas = pickle.load(Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","rb")
    Odds = pickle.load(Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","rb")
    Payouts = pickle.load(Payouts_file)
    Payouts_file.close()
    
    win_file=open("fcwin_data.pickle","rb")
    win_data = pickle.load(win_file)
    win_file.close()

    return Arenas[rnd], Odds[rnd], Payouts[rnd], win_data[rnd]

def get_todays_data():
    res=requests.get("http://foodclub.daqtools.info/History.php")
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'lxml')

    test=soup.select("td")
    names=[1,11,20,29,40,50,59,68,79,89,98,107,118,128,137,146,157,167,176,185]
    opening_odds=[x+5 for x in names]
    current_odds=[x+6 for x in names]
    
    Pirates=[test[x].text for x in names]
    Percent=[int(test[x].text[:-2]) for x in opening_odds]
    Payout=[int(test[x].text[:-2]) for x in current_odds]
    
    Shipwreck=Pirates[0:4]
    Lagoon=Pirates[4:8]
    Treasure_Island=Pirates[8:12]
    Hidden_Cove=Pirates[12:16]
    Harpoon_Harry=Pirates[16:20]
    
    OddsData={}; PayoutData={}
    for x in range(len(Pirates)):
        OddsData[Pirates[x]]=Percent[x]
        PayoutData[Pirates[x]]=Payout[x]
    
    return [Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry], OddsData, PayoutData

def calc_combos(Arenas, Odds, Payouts):
    Odds['']=1; Payouts['']=1;
    for n in range(len(Arenas)):
        Arenas[n].append('')
    output=[]
    for a in Arenas[0]:
        for b in Arenas[1]:
            for c in Arenas[2]:
                for d in Arenas[3]:
                    for e in Arenas[4]:
                        o=Odds[a]*Odds[b]*Odds[c]*Odds[d]*Odds[e]
                        p=Payouts[a]*Payouts[b]*Payouts[c]*Payouts[d]*Payouts[e]
                        er=o*p
                        output.append([a,b,c,d,e,p,o,er])
    combo_df=pd.DataFrame(output)
    combo_df.columns=["Shipwreck","Lagoon","Treasure Island","Hidden Cove","Harpoon Harry","Payout","Percent","Expected Ratio"]
    return combo_df

def calc_bets(combos, max_bet, risk):
    limit=1000000/max_bet
    combos.ix[combos.Payout > limit, 'Payout'] = limit
    combos["NP"]=17.63*np.log(combos["Percent"])+105.35
    combos["NER"]=np.where(combos["Expected Ratio"]>.95, 5*np.log(combos["Expected Ratio"]-.95)+90.5, 61.09*combos["Expected Ratio"]**2+13.507*combos["Expected Ratio"]-.3187) 
    combos["Raw"]=((1-risk)*combos.NP+risk*combos.NER)
    combos.sort_values("Raw",ascending=False,inplace=True)
    combos.index=range(1,len(combos)+1)
    bets=combos.head(10)         
    return bets

def calc_cumulative(bets, Odds):
    
    bet_list=[bets[n].tolist() for n in list(bets)[0:5]]
    for n in range(len(bet_list)):
         bet_list[n].append(' ')
    reduced_outcomes=[list(set(n)) for n in bet_list]
    reduced_odds=[]
    for tavern in reduced_outcomes:
        tavern.sort(reverse=True)
        total=0
        for pirate in tavern:
            if pirate != '':
                reduced_odds.append([pirate,Odds[pirate]])
                total+=Odds[pirate]
            else:
                reduced_odds.append([pirate,1-total])
    
    OddsList=[]
    for a in reduced_odds[0]:
        for b in reduced_odds[1]:
            for c in reduced_odds[2]:
                for d in reduced_odds[3]:
                    for e in reduced_odds[4]:
                        o=0
                        OddsList.append([a,b,c,d,e,o])
                        
    OddsDF=pd.DataFrame(OddsList)
    return OddsDF







a,o,p,w=load_past_data(4000)

t1=time.time()
allcombos=calc_combos(a,o,p)
print("New:",time.time()-t1)

t1=time.time()
mybets=calc_bets(allcombos,10000,.95)
print("Calc Bets:",time.time()-t1)

import food_tools as ft
t1=time.time()
ft.calc_bet(.95)
print("Old:", time.time()-t1)

t1=time.time()
ft.calc_cumulative(mybets)
print("cumulative:", time.time()-t1)