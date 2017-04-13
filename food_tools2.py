import pickle, bs4, requests, time
import pandas as pd
import numpy as np
from selenium import webdriver

realodds={2:0.523,
        3:0.285,
        4:0.225,
        5:0.182,
        6:0.154,
        7:0.133,
        8:0.118,
        9:0.105,
        10:0.095,
        11:0.087,
        12:0.080,
        13:0.04,
        }

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
    Percent=[realodds[int(test[x].text[:-2])] for x in opening_odds]
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

    for tavern in roundData:
        OddsSum=0
        for pirate in tavern:
            OddsSum+=OddsData[pirate]
        for pirate in tavern:
            OddsData[pirate]=OddsData[pirate]/OddsSum

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
                        output.append([a,b,c,d,e,p,o])
    combo_df=pd.DataFrame(output)
    combo_df.columns=["Shipwreck","Lagoon","Treasure Island","Hidden Cove","Harpoon Harry","Payout","Percent"]
    return combo_df

def calc_bets(combos, max_bet, risk):
    limit=1000000/max_bet
    combos.ix[combos.Payout > limit, 'Payout'] = limit
    combos["Expected Ratio"]=combos["Percent"]*combos["Payout"]
    combos["NP"]=17.63*np.log(combos["Percent"])+105.35
    combos["NER"]=np.where(combos["Expected Ratio"]>.95, 5*np.log(combos["Expected Ratio"]-.95)+90.5, 61.09*combos["Expected Ratio"]**2+13.507*combos["Expected Ratio"]-.3187) 
    combos["Raw"]=((1-risk)*combos.NP+risk*combos.NER)
    combos.sort_values("Raw",ascending=False,inplace=True)
    combos.index=range(1,len(combos)+1)
    bets=combos.head(10)
    TER=bets["Expected Ratio"].sum()         
    return bets

def calc_oddsdf(bets, Odds):
    bet_list=[bets[n].tolist() for n in list(bets)[0:5]]
    for n in range(len(bet_list)):
         bet_list[n].append('')
    reduced_outcomes=[list(set(n)) for n in bet_list]
    reduced_odds=[]
    for tavern in reduced_outcomes:
        tavern.sort(reverse=True)
        total=0
        reduced=[]
        for pirate in tavern:
            if pirate != '':
                reduced.append([pirate,Odds[pirate]])
                total+=Odds[pirate]
            else:
                reduced.append([pirate,1-total])
        reduced_odds.append(reduced)
           
    OddsList=[]
    for a in reduced_odds[0]:
        for b in reduced_odds[1]:
            for c in reduced_odds[2]:
                for d in reduced_odds[3]:
                    for e in reduced_odds[4]:
                        o=a[1]*b[1]*c[1]*d[1]*e[1]
                        OddsList.append([a[0],b[0],c[0],d[0],e[0],o])
                        
    OddsDF=pd.DataFrame(OddsList)
    return OddsDF

def calc_cumulative(bets, outcomes):
    #needs optimization, working with dataframes is slow
    localdf=pd.DataFrame()
    for x in range(len(outcomes)):
        local=pd.DataFrame()
        result=list(outcomes.ix[x,0:5])
        for y in range(1,len(bets)+1):
            bet = list(filter(None, list(bets.ix[y,0:5])))
            if set(bet).issubset(set(result)):
                local=local.append([[bets.ix[y,5],outcomes.ix[x,5]]])
            else:
                local=local.append([[0,outcomes.ix[x,5]]])
        localdf=localdf.append([[local[0].sum(),local[1].sum()]])
      
    localdf.columns=["Odds","Percent"]
    localdf["Percent"]/=len(bets)
    localdf=localdf.groupby("Odds").sum()
    localdf["Cumulative"]=localdf.Percent.cumsum()
    print(localdf)
    return localdf

def calc_bust(localdf,bets,rnd,risk):
    #needs cleanup
    splitdf=localdf.reset_index()
    try:
        bust=splitdf[splitdf.Odds == 0]["Percent"].sum()*100
    except ValueError:
        bust=0
    try:
        partial=splitdf[(splitdf['Odds'] > 0) & (splitdf['Odds'] <= 10)]["Percent"].sum()*100
    except ValueError:
        partial=0
    try:
        jackpot=splitdf[splitdf.Odds >= 10]["Percent"].sum()*100
    except ValueError:
        jackpot=0
    print("Bust: %.2f%% \nPartial: %.2f%% \nGain %.2f%% \n" % (bust,partial,jackpot))
    
    TER=bets["Expected Ratio"].sum()
    plot=localdf.reset_index().plot(x="Cumulative", y="Odds",drawstyle="steps", linewidth=2,legend=False,xlim=(0,1),title=str(rnd)+"  Risk:"+str(risk))
    fig = plot.get_figure()
    fig.savefig("daybet.png",dpi=200)
    htmloutput=open("food_club.html","w")
    htmloutput.write("""<table border='1'>
    	<tr>
    		<th colspan='3'>Risk: %.2f</th>
    	</tr>
    	<tr>
    		<td colspan='3'>%s</td>
    	</tr>
    	<tr>
    		<td>
            <center>
    			<table border='1'>
    				<tr>
    					<th>TER</th>
    					<td>%.3f</td>
    				</tr>
    				<tr>
    					<th>Bust</th>
    					<td>%.3f</td>
    				</tr>
    				<tr>
    					<th>Partial</th>
    					<td>%.3f</td>
    				</tr>
    				<tr>
    					<th>Gain</th>
    					<td>%.3f</td>
    				</tr>
    			</table>
            </center>
    		</td>
    		<td><center>%s</center></td>
    		<td><center><img src=\'daybet.png\' style='width:500px;'></center></td>
    	</tr>
    </table><br><br>
    """ % (risk, bets.to_html(), TER, bust, partial, jackpot, localdf.to_html()))
    htmloutput.close()
    
def calc_winnings(bets,winners):    
    winnings=[]
    result=winners
    for y in range(1,len(bets)+1):
        bet = list(filter(None, list(bets.ix[y,0:5])))
        if set(bet).issubset(set(result)):
            winnings.append(bets.ix[y,5])
    pay=sum(winnings)
    return pay

def test_model(risks,rounds,max_bet):
    for risk in risks:
        total_win=[]; bets=0;
        for rnd in rounds:
            Arenas, Odds, Payouts, win_data=load_past_data(rnd)
            combos=calc_combos(Arenas,Odds,Payouts)
            bet_today=calc_bets(combos, max_bet, risk)
            win=calc_winnings(bet_today,win_data)
            total_win.append(win)
            bets+=10
        print("%.2f %d %.2f" % (risk,sum(total_win),sum(total_win)/bets))
        
        
def start():
    global browser
    FirefoxProfile=r'C:\Users\Vincent\AppData\Roaming\Mozilla\Firefox\Profiles\swdbgbjk.profileToolsQA'
    profile = webdriver.FirefoxProfile(FirefoxProfile)
    browser = webdriver.Firefox(profile)

def daqtools(bets,max_bet):
    bnames=bets.ix[1:10,0:5]
    browser.get("http://foodclub.daqtools.info/Bets_Dropdown.php")
    page=browser.find_element_by_xpath("//input[@name='maxbet']")
    time.sleep(.5)
    page.clear()
    page.send_keys(max_bet)    
    for number in range(10):
        for tavern in range(5):
            betindex="bet[%d][%d]" % (number+1, tavern+1)
            pirate=bnames.iat[number,tavern]
            if pirate!='':
                browser.find_element_by_xpath("//select[@name='"+betindex+"']/option[text()='%s']" % pirate).click()
            else:
                pass