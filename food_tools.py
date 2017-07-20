import pickle, bs4, requests, time
import pandas as pd
import numpy as np
from selenium import webdriver
import matplotlib.pyplot as plt
plt.style.use('ggplot')

'''
To Do:
    1. Reduce pickles to 1 pickle
    2. 1 function for all simulations - take bet and calc winnings
    3. Pickle bets?
    4. Calc winnings based on payout data not column

'''
realodds={2:0.5226,
        3:0.2842,
        4:0.2288,
        5:0.1833,
        6:0.1583,
        7:0.1332,
        8:0.1191,
        9:0.1047,
        10:0.0989,
        11:0.087,
        12:0.08,
        13:0.044,
        }

#Downloads data from daqtools and writes to pickles
#need to remove OddsData
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
    if len(winElems)!=0:
        winners=[x.text for x in winElems]
        win_data[rnd]=winners
        win_file=open("fcwin_data.pickle","wb")
        pickle.dump(win_data, win_file)
        win_file.close()
    else:
        winners=[]
    test=soup.select("td")
    names=[1,11,20,29,40,50,59,68,79,89,98,107,118,128,137,146,157,167,176,185]
    opening_odds=[x+5 for x in names]
    current_odds=[x+6 for x in names]
    food_adjust=[x+8 for x in names]
    est_prob=[x+1 for x in names]
    foodTable=[10,49,88,127,166]
    
    Pirates=[test[x].text for x in names]
    FoodCourseData=[test[x].text for x in foodTable]
    Percent=[realodds[int(test[x].text[:-2])] for x in opening_odds]
    Payout=[int(test[x].text[:-2]) for x in current_odds]
    FA=[int(test[x].text[-2:]) for x in food_adjust]
    Favs=[int(test[x].text[:2]) for x in food_adjust]
    Alg=[int(test[x].text[6:8]) for x in food_adjust]
    EP=[float(test[x].text[:-2]) for x in est_prob]
    OO=[int(test[x].text[:-2]) for x in opening_odds]
    
    Shipwreck=Pirates[0:4]
    Lagoon=Pirates[4:8]
    Treasure_Island=Pirates[8:12]
    Hidden_Cove=Pirates[12:16]
    Harpoon_Harry=Pirates[16:20]
    
    roundData=[Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]

    OddsData={}; PayoutData={}; FoodAdjustData={}; FavoritesData={}; AllergiesData={}; EstProbData={}; RatioData={}; OpenOddsData={}
    for x in range(len(Pirates)):
        OddsData[Pirates[x]]=Percent[x]
        PayoutData[Pirates[x]]=Payout[x]
        FoodAdjustData[Pirates[x]]=FA[x]
        FavoritesData[Pirates[x]]=Favs[x]
        AllergiesData[Pirates[x]]=Alg[x]
        EstProbData[Pirates[x]]=EP[x]
        OpenOddsData[Pirates[x]]=OO[x]

    for tavern in roundData:
        OddsSum=0
        for pirate in tavern:
            OddsSum+=OddsData[pirate]
        for pirate in tavern:
            OddsData[pirate]=OddsData[pirate]/OddsSum
            RatioData[pirate]=OddsSum

    Arena_file=open("ArenaData.pickle","rb")
    Arenas = pickle.load(Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","rb")
    Odds = pickle.load(Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","rb")
    Payouts = pickle.load(Payouts_file)
    Payouts_file.close()
    
    Favorites_file=open("Favorites.pickle","rb")
    Favorites = pickle.load(Favorites_file)
    Favorites_file.close()
    
    FoodAdjust_file=open("FoodAdjustData.pickle","rb")
    FoodAdjust = pickle.load(FoodAdjust_file)
    FoodAdjust_file.close()
    
    Allergies_file=open("Allergies.pickle","rb")
    Allergies = pickle.load(Allergies_file)
    Allergies_file.close()

    EstProb_file=open("EstProb.pickle","rb")
    EstProb = pickle.load(EstProb_file)
    EstProb_file.close()
    
    OpenOdds_file=open("OpenOddsData.pickle","rb")
    OpenOdds = pickle.load(OpenOdds_file)
    OpenOdds_file.close()
    
    Ratio_file=open("RatioData.pickle","rb")
    Ratio = pickle.load(Ratio_file)
    Ratio_file.close() 
    
    Food_file=open("FoodCourses.pickle","rb")
    FoodCourse = pickle.load(Food_file)
    Food_file.close() 
    
    Arenas[rnd]=roundData
    Payouts[rnd]=PayoutData
    Odds[rnd]=OddsData
    FoodAdjust[rnd]=FoodAdjustData
    Favorites[rnd]=FavoritesData
    Allergies[rnd]=AllergiesData
    EstProb[rnd]=EstProbData
    Ratio[rnd]=RatioData
    OpenOdds[rnd]=OpenOddsData
    FoodCourse[rnd]=FoodCourseData
      
    Arena_file=open("ArenaData.pickle","wb")
    pickle.dump(Arenas, Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","wb")
    pickle.dump(Odds, Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","wb")
    pickle.dump(Payouts, Payouts_file)
    Payouts_file.close()
    
    FoodAdjust_file=open("FoodAdjustData.pickle","wb")
    pickle.dump(FoodAdjust, FoodAdjust_file)
    FoodAdjust_file.close()
          
    Favorites_file=open("Favorites.pickle","wb")
    pickle.dump(Favorites, Favorites_file)
    Favorites_file.close()
    
    Allergies_file=open("Allergies.pickle","wb")
    pickle.dump(Allergies, Allergies_file)
    Allergies_file.close()
    
    EstProb_file=open("EstProb.pickle","wb")
    pickle.dump(EstProb, EstProb_file)
    EstProb_file.close()
    
    OpenOdds_file=open("OpenOddsData.pickle","wb")
    pickle.dump(OpenOdds, OpenOdds_file)
    OpenOdds_file.close()   
    
    Ratio_file=open("RatioData.pickle","wb")
    pickle.dump(Ratio, Ratio_file)
    Ratio_file.close()  
    
    Food_file=open("FoodCourses.pickle","wb")
    pickle.dump(FoodCourse, Food_file)
    Food_file.close()
    return

def load_all_data(rnd):
    Arena_file=open("ArenaData.pickle","rb")
    Arenas = pickle.load(Arena_file)
    Arena_file.close()
    
    Odds_file=open("OddsData.pickle","rb")
    Odds = pickle.load(Odds_file)
    Odds_file.close()
    
    Payouts_file=open("PayoutsData.pickle","rb")
    Payouts = pickle.load(Payouts_file)
    Payouts_file.close()
    
    OpenOdds_file=open("OpenOddsData.pickle","rb")
    OpenOdds = pickle.load(OpenOdds_file)
    OpenOdds_file.close()
    
    Ratio_file=open("RatioData.pickle","rb")
    Ratio = pickle.load(Ratio_file)
    Ratio_file.close()
    
    FoodAdjust_file=open("FoodAdjustData.pickle","rb")
    FoodAdjust = pickle.load(FoodAdjust_file)
    FoodAdjust_file.close()
    
    win_file=open("fcwin_data.pickle","rb")
    win_data = pickle.load(win_file)
    win_file.close()
    
    favs_file=open("Favorites.pickle","rb")
    Favorites = pickle.load(favs_file)
    favs_file.close()
    
    alg_file=open("Allergies.pickle","rb")
    Allergies = pickle.load(alg_file)
    alg_file.close()

    EstProb_file=open("EstProb.pickle","rb")
    EstProb = pickle.load(EstProb_file)
    EstProb_file.close()
    
    return Arenas[rnd], Odds[rnd], Payouts[rnd], OpenOdds[rnd], Ratio[rnd], FoodAdjust[rnd], win_data[rnd], Favorites[rnd], Allergies[rnd], EstProb[rnd]


#gets today's data - does not write to pickle
def get_todays_data():
    res=requests.get("http://foodclub.daqtools.info/History.php")
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'lxml')

    test=soup.select("td")
    names=[1,11,20,29,40,50,59,68,79,89,98,107,118,128,137,146,157,167,176,185]
    opening_odds=[x+5 for x in names]
    current_odds=[x+6 for x in names]
    food_adjust=[x+8 for x in names]
    est_prob=[x+1 for x in names]
    
    Pirates=[test[x].text for x in names]
#    Percent=[realodds[int(test[x].text[:-2])] for x in opening_odds]
    Payout=[int(test[x].text[:-2]) for x in current_odds]
    FA=[int(test[x].text[-2:]) for x in food_adjust]
    Favs=[int(test[x].text[:2]) for x in food_adjust]
    Alg=[int(test[x].text[6:8]) for x in food_adjust]
    EP=[float(test[x].text[:-2])/100 for x in est_prob]
    OO=[int(test[x].text[:-2]) for x in opening_odds]
    
    Shipwreck=Pirates[0:4]
    Lagoon=Pirates[4:8]
    Treasure_Island=Pirates[8:12]
    Hidden_Cove=Pirates[12:16]
    Harpoon_Harry=Pirates[16:20]
    
    roundData=[Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]

#    OddsData={};  RatioData={};
    PayoutData={}; FoodAdjustData={}; FavoritesData={}; AllergiesData={}; EstProbData={}; OpenOddsData={}
    for x in range(len(Pirates)):
#        OddsData[Pirates[x]]=Percent[x]
        PayoutData[Pirates[x]]=Payout[x]
        FoodAdjustData[Pirates[x]]=FA[x]
        FavoritesData[Pirates[x]]=Favs[x]
        AllergiesData[Pirates[x]]=Alg[x]
        EstProbData[Pirates[x]]=EP[x]
        OpenOddsData[Pirates[x]]=OO[x]

#    for tavern in roundData:
#        OddsSum=0
#        for pirate in tavern:
#            OddsSum+=OddsData[pirate]
#        for pirate in tavern:
#            OddsData[pirate]=OddsData[pirate]/OddsSum
#            RatioData[pirate]=OddsSum
    
    return roundData, EstProbData, PayoutData, OpenOddsData

def calc_winnings(bets,winners):    
    winnings=[]
    result=winners
    for y in range(0,len(bets)):
        bet = list(filter(None, list(bets.iloc[y,0:5])))
        if set(bet).issubset(set(result)):
            winnings.append(bets.iloc[y,5])
    pay=sum(winnings)
    return pay

#Creates reduced combo_df based only on bets
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

#calculates bust % table
def calc_cumulative(bets, OddsDF):
    #needs optimization, working with dataframes is slow
    localdf=pd.DataFrame()
    for x in range(len(OddsDF)):
        local=pd.DataFrame()
        result=list(OddsDF.ix[x,0:5])
        for y in range(1,len(bets)+1):
            bet = list(filter(None, list(bets.ix[y,0:5])))
            if set(bet).issubset(set(result)):
                local=local.append([[bets.ix[y,5],OddsDF.ix[x,5]]])
            else:
                local=local.append([[0,OddsDF.ix[x,5]]])
        localdf=localdf.append([[local[0].sum(),local[1].sum()]])
      
    localdf.columns=["Odds","Percent"]
    localdf["Percent"]/=len(bets)
    localdf=localdf.groupby("Odds").sum()
    localdf["Cumulative"]=localdf.Percent.cumsum()
    print(localdf)
    return localdf

#summarizes cumulative table to bust, partial, profit
#creates html file
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

#starts firefox browser    
def start():
    global browser
    FirefoxProfile=r'C:\Users\Vincent\AppData\Roaming\Mozilla\Firefox\Profiles\swdbgbjk.profileToolsQA'
    profile = webdriver.FirefoxProfile(FirefoxProfile)
    browser = webdriver.Firefox(profile)

#inputs calculated bets in daqtools
#look into integrating this into daqtools url
def daqtools(bets,max_bet):
    bnames=bets.ix[1:10,0:5]
    browser.get("http://foodclub.daqtools.info/Bets_Dropdown.php")
#    page=browser.find_element_by_xpath("//input[@name='maxbet']")
    time.sleep(.5)
#    page.clear()
#    page.send_keys(max_bet)    
    for number in range(10):
        for tavern in range(5):
            betindex="bet[%d][%d]" % (number+1, tavern+1)
            pirate=bnames.iat[number,tavern]
            if pirate!='':
                browser.find_element_by_xpath('//select[@name="%s"]/option[text()="%s"]' % (betindex, pirate)).click()
            else:
                pass

#generates all 3125 combinations
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

#creates 3125 combinations using "realodds" variable and historic odd data
def AORO_combos(Arenas, OpenOdds, Payouts):
    detail=[]; prates=[]
    for y in range(len(Arenas)):
        open_odds=[]; summation=0
        for x in Arenas[y]:
            open_odds.append(realodds[OpenOdds[x]])
        pp=Arenas[y]
        zipfile=[A for B, A in sorted(zip(open_odds,pp))]
        open_odds.sort()
        for x in range(len(open_odds)):
            prates.append(zipfile[x])
            if open_odds[x]!=.5226:
                summation+=open_odds[x]
        if open_odds[2]==.5226:
            open_odds[2]=(1-summation)/2
            open_odds[3]=open_odds[2]
        if open_odds[3]==.5226:
            open_odds[3]=1-summation     
        for x in range(len(open_odds)):
            detail.append(open_odds[x])
    
    Odds={}
    for x in range(len(prates)):
        Odds[prates[x]]=detail[x]
    
    lookup_file=open("ArenaOdds.pickle","rb")
    lookup = pickle.load(lookup_file)
    lookup_file.close()
    
    ArenaOdds=[]
    for x in Arenas:
        A_Odds=[]
        for y in x:
            A_Odds.append(OpenOdds[y])
        A_Odds.sort()
        ArenaOdds.append(A_Odds)
    count=0; AO_key={};
    for x in Arenas:
        for y in x:
            for z in range(4):
                AO_key[y]=str(ArenaOdds[count])+"-"+str(OpenOdds[y])
        count+=1
    
    try:
        for x in Arenas:
            for pirate in x:
                Odds[pirate]=lookup[AO_key[pirate]]
    except KeyError:
        pass
    
    return calc_combos(Arenas, Odds, Payouts), Odds

def max_TER_bets(combos, max_bet, risk):
    limit=1000000/max_bet
    combos.ix[combos.Payout > limit, 'Payout'] = limit
    combos["Expected Ratio"]=combos["Percent"]*combos["Payout"]
#    combos["NP"]=(combos["Percent"]-.0102)/.0405
#    combos["NER"]=(combos["Expected Ratio"]-.3017)/.4235
#    combos["Raw"]=((1-risk)*combos.NP+risk*combos.NER)
    combos.sort_values("Expected Ratio",ascending=False,inplace=True)
    combos.index=range(1,len(combos)+1)
    bets=combos.head(10)
    bets=bets[bets["Expected Ratio"]>1]
    TER=bets["Expected Ratio"].sum()   
    return bets,TER

#decreases standard deviation by finding bets with higher %, but lower TER
def std_decrease(bets,TER,combodf):
    min_pct=.01    #minimum % increase
    min_er=-.25   #minimum drop in TER

    pbets=combodf[combodf["Expected Ratio"]>(bets.loc[10]["Expected Ratio"]+min_er)]
    pbets=pbets[pbets["Expected Ratio"]<(bets.loc[10]["Expected Ratio"])]
    if len(pbets)==0:
        return bets, TER
    
    pbets.sort_values("Expected Ratio", inplace=True, ascending=False)
    bets = bets.reset_index(drop=True)
    pbets = pbets.reset_index(drop=True)
    
    for bet_index in range(len(bets)):
        for replacement_index in range(len(pbets)):
            bet_data=bets.loc[bet_index].copy()
            r_data=pbets.loc[replacement_index].copy()
            bet_er=bets.loc[bet_index]["Expected Ratio"]
            bet_p=bets.loc[bet_index]["Percent"]
            r_er=pbets.loc[replacement_index]["Expected Ratio"]
            r_p=pbets.loc[replacement_index]["Percent"]
            if r_er-bet_er>min_er and r_p-bet_p>min_pct:
                bets.drop(bets.index[bet_index],inplace=True)
                pbets.drop(pbets.index[replacement_index],inplace=True)
                pbets=pbets.append(bet_data)
                bets=bets.append(r_data)
                pbets.sort_values("Expected Ratio", inplace=True, ascending=False)
                pbets = pbets.reset_index(drop=True)
                bets = bets.reset_index(drop=True)
                continue
    TER=bets["Expected Ratio"].sum()        
    return bets, TER

def test_daq_model(risk,rounds,max_bet):
    total_win=[]; bets=0; total_TER=[]
    for rnd in rounds:
        a,o,p,oo,r,fa,win_data,f,alg,est=load_all_data(rnd)
        for key, value in est.items():
            est[key]=value/100
        combodf=calc_combos(a, est, p)
        bet_today,TER=max_TER_bets(combodf, max_bet, risk)
        win=calc_winnings(bet_today,win_data)
        
        with open("daq_bet_data.pickle",'rb') as rfp:
            bet_win = pickle.load(rfp)
        key=str(rnd)+"-"+str(max_bet)
        try:
            bet_win[key]=win/len(bet_today)
        except ZeroDivisionError:
            bet_win[key]=None
        with open("daq_bet_data.pickle",'wb') as wfp:
            pickle.dump(bet_win, wfp)  
        
        total_win.append(win)
        total_TER.append(TER)
        bets+=len(bet_today)
    print("%.2f %d %.2f TER: %.2f - DAQ" % (risk,sum(total_win),sum(total_win)/bets,sum(total_TER)/len(rounds)))
    return sum(total_win)/bets

#need to optimize
def test_AORO(risk,rounds,max_bet):
    total_win=[]; bets=0; total_TER=[]
    for rnd in rounds:
        a,o,p,oo,r,fa,win_data,f,alg,est=load_all_data(rnd)
        combodf=AORO_combos(a, oo, p)[0]
        bet_today,TER=max_TER_bets(combodf, max_bet, risk)
        win=calc_winnings(bet_today,win_data)
        
        with open("AORO_bet_data.pickle",'rb') as rfp:
            bet_win = pickle.load(rfp)
        key=str(rnd)+"-"+str(max_bet)
        try:
            bet_win[key]=win/len(bet_today)
        except ZeroDivisionError:
            bet_win[key]=None      
        with open("AORO_bet_data.pickle",'wb') as wfp:
            pickle.dump(bet_win, wfp)   

        total_win.append(win)
        total_TER.append(TER)
        bets+=len(bet_today)
    print("%.2f %d %.2f TER: %.2f - AORO" % (risk,sum(total_win),sum(total_win)/bets,sum(total_TER)/len(rounds)))
    return sum(total_win)/bets
        
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

#creates reddit table of bets
def reddit_format(rnd,bets):
    print(str(rnd)+"|Shipwreck|Lagoon|Treasure|Hidden|Harpoon|Odds\n:-:|-|-|-|-|-|-:")
    bets["Payout"]=bets["Payout"].astype(int)
    bets["Payout"]=bets["Payout"].astype(str)+":1"
    for x in bets.columns[0:5]:
        bets.replace({x: nicknames}, inplace=True)
    olist=np.array(bets.iloc[0:10,0:6])
    count=1
    for x in olist:
        print(count,*x, sep='|')
        count+=1