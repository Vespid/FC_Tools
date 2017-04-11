from selenium import webdriver
import pandas as pd
import requests, bs4
import time, pickle, random, openpyxl
import numpy as np

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

def start():
    global browser
    FirefoxProfile=r'C:\Users\Vincent\AppData\Roaming\Mozilla\Firefox\Profiles\swdbgbjk.profileToolsQA'
    profile = webdriver.FirefoxProfile(FirefoxProfile)
    browser = webdriver.Firefox(profile)

def daqtools(bets):
    bnames=bets.ix[1:10,0:5]
    browser.get("http://foodclub.daqtools.info/Bets_Dropdown.php")
    page=browser.find_element_by_xpath("//input[@name='maxbet']")
    time.sleep(.5)
    page.clear()
    page.send_keys(9936)    
    for number in range(10):
        for tavern in range(5):
            betindex="bet[%d][%d]" % (number+1, tavern+1)
            pirate=bnames.iat[number,tavern]
            if pirate!='':
                browser.find_element_by_xpath("//select[@name='"+betindex+"']/option[text()='%s']" % pirate).click()
            else:
                pass
            
def import_betexcel(sheet):
    global bets
    bets=pd.read_excel('bet_data.xlsx', sheetname=sheet)
    
def export_betexcel(sheet):
    writer = pd.ExcelWriter('bet_data.xlsx')
    bets.to_excel(writer, sheet)
    writer.save()

def get_neodata():
    global Odds
    browser.get("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    Odds=browser.execute_script("return pirate_odds;")
#    winners=["winner1","winner2","winner3","winner4","winner5"]
    Shipwreck=TavInfo("winner1")
    Lagoon=TavInfo("winner2")
    Treasure_Island=TavInfo("winner3")
    Hidden_Cove=TavInfo("winner4")
    Harpoon_Harry=TavInfo("winner5")
    return [Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]

def mine_data(roundList):
    for x in roundList:
        url="http://foodclub.daqtools.info/History.php?round="+str(x)
        roundData=pd.read_html(url)[0]
        data_file=open("fc_data.pickle","rb")
        FC_data = pickle.load(data_file)
        data_file.close()
        FC_data[x]=roundData
        data_file=open("fc_data.pickle","wb")
        pickle.dump(FC_data, data_file)
        data_file.close()

def convert_minedata(rnd):
        data_file=open("fc_data.pickle","rb")
        FC_data = pickle.load(data_file)
        data_file.close()
        rnd_df=FC_data[rnd]
        rnd_df.drop(rnd_df.index[[0,1,5,6,10,11,15,16,20,21]],inplace=True)
        names=rnd_df[0]
        opening_odds=rnd_df[7]
        current_odds=rnd_df[8]
        
def get_soup_data():
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
    All=[[Pirates[x],Percent[x],Payout[x]] for x in range(len(Pirates))]
    
    Shipwreck=All[0:4]
    Lagoon=All[4:8]
    Treasure_Island=All[8:12]
    Hidden_Cove=All[12:16]
    Harpoon_Harry=All[16:20]
    
    return [Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]


    
def get_past_data(rnd):
    data_file=open("food_data.pickle","rb")
    FC_data = pickle.load(data_file)
    if rnd in list(FC_data.keys()):
        data_file.close()
        return
    data_file.close()
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
    All=[[Pirates[x],Percent[x],Payout[x]] for x in range(len(Pirates))]
    
    Shipwreck=All[0:4]
    Lagoon=All[4:8]
    Treasure_Island=All[8:12]
    Hidden_Cove=All[12:16]
    Harpoon_Harry=All[16:20]
    
    roundData=[Shipwreck,Lagoon,Treasure_Island,Hidden_Cove,Harpoon_Harry]

    win_file=open("fcwin_data.pickle","rb")
    win_data = pickle.load(win_file)
    win_file.close()
    
    FC_data[rnd]=roundData
    win_data[rnd]=winners  
           
    data_file=open("food_data.pickle","wb")
    pickle.dump(FC_data, data_file)
    data_file.close()
    
    win_file=open("fcwin_data.pickle","wb")
    pickle.dump(win_data, win_file)
    win_file.close()
    return roundData, winners

def load_past_data(rnd):
    data_file=open("food_data.pickle","rb")
    win_file=open("fcwin_data.pickle","rb")
    FC_data = pickle.load(data_file)
    win_data = pickle.load(win_file)
    data_file.close()
    win_file.close()
    roundData=FC_data[rnd]
    winners=win_data[rnd]
    return roundData, winners

def import_daqtoolbet():
    names=[x.text for x in browser.find_elements_by_xpath("//td[contains(@class, 'odds') or contains(@class, 'name')]")]
    for x in range(len(names)):
        if names[x]=='---':
            names[x]=''
#    bets=pd.DataFrame([[names[x],names[x+1],names[x+2],names[x+3],names[x+4]] for x in range(0,len(names),5)])
    percent=[]; b=[]; p=[]
    for x in range(len(names)):
        if names[x]!='':
            percent.append(AllTavernsDict[names[x]][1])
        else:
            percent.append(1)
    for x in range(0,len(names),5):
        b.append([names[x],names[x+1],names[x+2],names[x+3],names[x+4]])
        p.append(percent[x]*percent[x+1]*percent[x+2]*percent[x+3]*percent[x+4])
    bets=pd.DataFrame(b)
    oddElems=browser.find_elements_by_tag_name("div#body td")
    payoffindex=[84,99,114,129,144,159,174,189,204,219]
    payoffs=[int(oddElems[x].text[:-2]) for x in payoffindex]
    bets["Payoff"]=payoffs
    bets["Percent"]=p
    bets["Expected Ratio"]=bets["Payoff"]*bets["Percent"]
    bets.index=range(1,len(bets)+1)
    AllTavernsDict[names[x]][1]
    return bets

def calc_winnings(bets,winners):    
    winnings=[]
    result=winners
    for y in range(1,len(bets)+1):
        bet = list(filter(None, list(bets.ix[y,0:5])))
        if set(bet).issubset(set(result)):
            winnings.append(bets.ix[y,5])
    pay=sum(winnings)
#    print(pay)
    return pay

####################################################################3
########################################################################
#Everything beyond this line sucks

def TavInfo(x):
    pName="//select[@name='"+x+"']"
    TavernElems=browser.find_element_by_xpath(pName)
    TavernPiratesElems=TavernElems.find_elements_by_tag_name("option")
    TavernPiratesElems[1].get_attribute("value")
    TavernPirates=[int(TavernPiratesElems[x].get_attribute("value")) for x in range(1,5)]
    TavernPirateNames=[pirate_list[int(x)] for x in TavernPirates]
    return [[TavernPirateNames[x], Odds[TavernPirates[x]]] for x in range(len(TavernPirateNames))]

def singles(T):
    data=AllTaverns[T]
    names=[data[x][0] for x in range(len(data))]
    odds=[data[x][1] for x in range(len(data))]
    weighted=[realodds[x] for x in odds]
    percent=[x/sum(weighted) for x in weighted]
    gain=[odds[0]*percent[0]]*len(names)
    try:
        odds=[data[x][2] for x in range(len(data))]
    except:
        pass
    result=[]
    for x in range(len(data)):
        A=['']*5
        A[T]=names[x]
        result.append([A[0],A[1],A[2],A[3],A[4],odds[x],percent[x],gain[x]])
    return result

def doubles(T1,T2):
    d1=AllTaverns[T1]
    d2=AllTaverns[T2]
    n1=[d1[x][0] for x in range(len(d1))]
    n2=[d2[x][0] for x in range(len(d2))]
    o1=[d1[x][1] for x in range(len(d1))]
    o2=[d2[x][1] for x in range(len(d2))]
    w1=[realodds[x] for x in o1]
    w2=[realodds[x] for x in o2]
    p1=[x/sum(w1) for x in w1]
    p2=[x/sum(w2) for x in w2]
    try:
        o1=[d1[x][2] for x in range(len(d1))]
        o2=[d2[x][2] for x in range(len(d2))]
    except:
        pass
    names=[]
    odds=[]
    percent=[]
    gain=[]
    result=[]
    for x in range(len(d1)):
        for y in range(len(d2)):
            A=['']*5
            A[T1]=n1[x]
            A[T2]=n2[y]
            names.append(A)
            odds.append(o1[x]*o2[y])
            percent.append(p1[x]*p2[y])
            gain.append(o1[x]*o2[y]*p1[x]*p2[y])
    for x in range(len(names)):
        result.append([names[x][0],names[x][1],names[x][2],names[x][3],names[x][4],odds[x],percent[x],gain[x]])
    return result

def triples(T1,T2,T3):
    d1=AllTaverns[T1]
    d2=AllTaverns[T2]
    d3=AllTaverns[T3]
    n1=[d1[x][0] for x in range(len(d1))]
    n2=[d2[x][0] for x in range(len(d2))]
    n3=[d3[x][0] for x in range(len(d3))]
    o1=[d1[x][1] for x in range(len(d1))]
    o2=[d2[x][1] for x in range(len(d2))]
    o3=[d3[x][1] for x in range(len(d3))]
    w1=[realodds[x] for x in o1]
    w2=[realodds[x] for x in o2]
    w3=[realodds[x] for x in o3]
    p1=[x/sum(w1) for x in w1]
    p2=[x/sum(w2) for x in w2]
    p3=[x/sum(w3) for x in w3]
    try:
        o1=[d1[x][2] for x in range(len(d1))]
        o2=[d2[x][2] for x in range(len(d2))]
        o3=[d3[x][2] for x in range(len(d3))]
    except:
        pass
    names=[]
    odds=[]
    percent=[]
    gain=[]
    result=[]
    for x in range(len(d1)):
        for y in range(len(d2)):
            for z in range(len(d3)):
                A=['']*5
                A[T1]=n1[x]
                A[T2]=n2[y]
                A[T3]=n3[z]
                names.append(A)
                odds.append(o1[x]*o2[y]*o3[z])
                percent.append(p1[x]*p2[y]*p3[z])
                gain.append(o1[x]*o2[y]*o3[z]*p1[x]*p2[y]*p3[z])
    for x in range(len(names)):
        result.append([names[x][0],names[x][1],names[x][2],names[x][3],names[x][4],odds[x],percent[x],gain[x]])
    return result

def quads(T1,T2,T3,T4):
    d1=AllTaverns[T1]
    d2=AllTaverns[T2]
    d3=AllTaverns[T3]
    d4=AllTaverns[T4]
    n1=[d1[x][0] for x in range(len(d1))]
    n2=[d2[x][0] for x in range(len(d2))]
    n3=[d3[x][0] for x in range(len(d3))]
    n4=[d4[x][0] for x in range(len(d4))]
    o1=[d1[x][1] for x in range(len(d1))]
    o2=[d2[x][1] for x in range(len(d2))]
    o3=[d3[x][1] for x in range(len(d3))]
    o4=[d4[x][1] for x in range(len(d4))]
    w1=[realodds[x] for x in o1]
    w2=[realodds[x] for x in o2]
    w3=[realodds[x] for x in o3]
    w4=[realodds[x] for x in o4]
    p1=[x/sum(w1) for x in w1]
    p2=[x/sum(w2) for x in w2]
    p3=[x/sum(w3) for x in w3]
    p4=[x/sum(w4) for x in w4]
    try:
        o1=[d1[x][2] for x in range(len(d1))]
        o2=[d2[x][2] for x in range(len(d2))]
        o3=[d3[x][2] for x in range(len(d3))]
        o4=[d4[x][2] for x in range(len(d4))]
    except:
        pass
    names=[]
    odds=[]
    percent=[]
    gain=[]
    result=[]
    for x in range(len(d1)):
        for y in range(len(d2)):
            for z in range(len(d3)):
                for a in range(len(d4)):
                        A=['']*5
                        A[T1]=n1[x]
                        A[T2]=n2[y]
                        A[T3]=n3[z]
                        A[T4]=n4[a]
                        names.append(A)
                        odds.append(o1[x]*o2[y]*o3[z]*o4[a])
                        percent.append(p1[x]*p2[y]*p3[z]*p4[a])
                        gain.append(o1[x]*o2[y]*o3[z]*o4[a]*p1[x]*p2[y]*p3[z]*p4[a])
    for x in range(len(names)):
        result.append([names[x][0],names[x][1],names[x][2],names[x][3],names[x][4],odds[x],percent[x],gain[x]])
    return result

def quints(T1,T2,T3,T4,T5):
    d1=AllTaverns[T1]
    d2=AllTaverns[T2]
    d3=AllTaverns[T3]
    d4=AllTaverns[T4]
    d5=AllTaverns[T5]
    n1=[d1[x][0] for x in range(len(d1))]
    n2=[d2[x][0] for x in range(len(d2))]
    n3=[d3[x][0] for x in range(len(d3))]
    n4=[d4[x][0] for x in range(len(d4))]
    n5=[d5[x][0] for x in range(len(d5))]
    o1=[d1[x][1] for x in range(len(d1))]
    o2=[d2[x][1] for x in range(len(d2))]
    o3=[d3[x][1] for x in range(len(d3))]
    o4=[d4[x][1] for x in range(len(d4))]
    o5=[d5[x][1] for x in range(len(d5))]
    w1=[realodds[x] for x in o1]
    w2=[realodds[x] for x in o2]
    w3=[realodds[x] for x in o3]
    w4=[realodds[x] for x in o4]
    w5=[realodds[x] for x in o5]
    p1=[x/sum(w1) for x in w1]
    p2=[x/sum(w2) for x in w2]
    p3=[x/sum(w3) for x in w3]
    p4=[x/sum(w4) for x in w4]
    p5=[x/sum(w5) for x in w5]
    try:
        o1=[d1[x][2] for x in range(len(d1))]
        o2=[d2[x][2] for x in range(len(d2))]
        o3=[d3[x][2] for x in range(len(d3))]
        o4=[d4[x][2] for x in range(len(d4))]
        o5=[d5[x][2] for x in range(len(d5))]
    except:
        pass
    names=[]
    odds=[]
    percent=[]
    gain=[]
    result=[]
    for x in range(len(d1)):
        for y in range(len(d2)):
            for z in range(len(d3)):
                for a in range(len(d4)):
                    for b in range(len(d5)):
                        A=['']*5
                        A[T1]=n1[x]
                        A[T2]=n2[y]
                        A[T3]=n3[z]
                        A[T4]=n4[a]
                        A[T5]=n5[b]
                        names.append(A)
                        odds.append(o1[x]*o2[y]*o3[z]*o4[a]*o5[b])
                        percent.append(p1[x]*p2[y]*p3[z]*p4[a]*p5[b])
                        gain.append(o1[x]*o2[y]*o3[z]*o4[a]*o5[b]*p1[x]*p2[y]*p3[z]*p4[a]*p5[b])
    for x in range(len(names)):
        result.append([names[x][0],names[x][1],names[x][2],names[x][3],names[x][4],odds[x],percent[x],gain[x]])
    return result

def calc_bet(risk):
    #needs cleanup
    global AllTaverns
    try:
        AllTaverns
    except NameError:
        AllTaverns=get_soup_data()
    
    df = pd.DataFrame()
    for x in range((len(AllTaverns))):
        df=df.append(singles(x))
    
    for x in range((len(AllTaverns))):
        for y in range(x+1,(len(AllTaverns))):
            df=df.append(doubles(x,y))
            
    for x in range((len(AllTaverns))):
        for y in range(x+1,(len(AllTaverns))):
            for z in range(y+1,(len(AllTaverns))):
                df=df.append(triples(x,y,z))
                
    for x in range((len(AllTaverns))):
        for y in range(x+1,(len(AllTaverns))):
            for z in range(y+1,(len(AllTaverns))):
                for a in range(z+1,(len(AllTaverns))):
                    df=df.append(quads(x,y,z,a))
                    
    for x in range((len(AllTaverns))):
        for y in range(x+1,(len(AllTaverns))):
            for z in range(y+1,(len(AllTaverns))):
                for a in range(z+1,(len(AllTaverns))):
                    for b in range(a+1,(len(AllTaverns))):
                        df=df.append(quints(x,y,z,a,b))
    df.columns=["Shipwreck","Lagoon","Treasure Island","Hidden Cove","Harpoon Harry","Payout","Percent","Expected Ratio"]
    df.ix[df.Payout > 100, 'Payout'] = 100
    df["Expected Ratio"]=df["Payout"]*df["Percent"]
    df["NP"]=17.63*np.log(df["Percent"])+105.35
    df["NER"]=np.where(df["Expected Ratio"]>.95, 5*np.log(df["Expected Ratio"]-.95)+90.5, 61.09*df["Expected Ratio"]**2+13.507*df["Expected Ratio"]-.3187) 
#    df["NER"]=np.where(df["Expected Ratio"]>1.71, 4.5*np.log(df["Expected Ratio"]-1.7)+90, 57*(df["Expected Ratio"]-.33))
    Raw=((1-risk)*df.NP+risk*df.NER)
#    Raw=((1-risk)*df.Percent+risk*df["Expected Ratio"])
    df["Raw"]=Raw
    df.sort_values("Raw",ascending=False,inplace=True)
    df.index=range(1,len(df)+1)
    bets=df.head(10)
    
    #Total Expected Ratio
    TER=bets["Expected Ratio"].sum()
#    print("\n"+"_"*25)
#    print("\nRisk: %f" %risk)
#    print("TER %.3f" %TER)
#    writer = pd.ExcelWriter('bet_output.xlsx')
#    df.to_excel(writer)
#    writer.save()

    return bets, TER

def calc_cumulative(bets):
    #needs cleanup
#    TER=bets["Expected Ratio"].sum()
#    print("\n"+"_"*25)
#    print("\nRisk: %f" %n)
#    print("TER %.3f" %TER)
    
    All=pd.DataFrame()
    for x in range(len(AllTaverns)):
        All=All.append(singles(x))
    All.set_index(All[0]+All[1]+All[2]+All[3]+All[4],inplace=True)
    All.drop(All.columns[list(range(0,5))], axis=1, inplace=True) 
    AllTavernsDict=All.T.to_dict('list')
    
    ebets=bets.ix[1:10,0:5]
    emp=pd.DataFrame([['']*5], columns=list(bets)[0:5])
    ebets=ebets.append(emp,ignore_index=True)
    BetCombos=[list(ebets[x].unique()) for x in list(ebets)[0:5]]
    TreducedP=[]
    for x in range(len(BetCombos)):
        BetCombos[x].sort(reverse=True)
        total=0
        reducedP=[]
        for y in range(len(BetCombos[x])):
            if BetCombos[x][y]!='':
                pPercent=AllTavernsDict[BetCombos[x][y]][1]
                reducedP.append([BetCombos[x][y],pPercent])
                total+=pPercent
            else:
                reducedP.append([BetCombos[x][y],1-total])
        TreducedP.append(reducedP)
    
    L=TreducedP
    
    Tn=[]; Tp=[]
    for x in range(len(L)):
        i=[]; p=[]
        for y in range(len(L[x])):
            i.append(L[x][y][0])
            p.append(L[x][y][1])
        Tn.append(i)
        Tp.append(p)
    outcomes=pd.DataFrame([[a,b,c,d,e] for a in Tn[0] for b in Tn[1] for c in Tn[2] for d in Tn[3] for e in Tn[4]])
    outcomes["Percent"]=[a*b*c*d*e for a in Tp[0] for b in Tp[1] for c in Tp[2] for d in Tp[3] for e in Tp[4]]
    
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
    #localdf.set_index("Odds", inplace=True)
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

def download_rounds(minRound,maxRound):
    for x in range(minRound,maxRound):
        if x%10==0:
            print("Downloading round: %d..." % x)
        get_past_data(x)
    print("Downloads complete")

def test_model(risks,rounds,test_amount):
#    modelData=openpyxl.load_workbook('model_data.xlsx')    
#    activeSheet=modelData.get_sheet_by_name("Sheet1")
#    
#    roundData=openpyxl.load_workbook('round_data.xlsx')
#    roundSheet=roundData.get_sheet_by_name("Sheet1")
    global AllTaverns
    for risk in risks:
        total_win=[]; bets=0; averageTER=0
        for rnd in rounds:
            AllTaverns,win_pirate=load_past_data(rnd)
            testbet, TER=calc_bet(risk)
            win=calc_winnings(testbet,win_pirate)
            total_win.append(win)
            bets+=10
            averageTER+=TER
#            rndmaxrow=roundSheet.max_row
#            roundSheet["A%d" % (rndmaxrow+1)]=rnd
#            roundSheet["B%d" % (rndmaxrow+1)]=risk            
#            roundSheet["C%d" % (rndmaxrow+1)]=win
#            roundSheet["D%d" % (rndmaxrow+1)]=TER
        print("%.2f %d %.2f %.3f" % (risk,sum(total_win),sum(total_win)/bets ,averageTER/bets))    
#        maxrow=activeSheet.max_row
#        activeSheet["A%d" % (maxrow+1)]=len(rounds)
#        activeSheet["B%d" % (maxrow+1)]=risk            
#        activeSheet["C%d" % (maxrow+1)]=str(sum(total_win))+":"+str(bets)
#        activeSheet["D%d" % (maxrow+1)]=sum(total_win)/bets
#        activeSheet["E%d" % (maxrow+1)]=averageTER/bets
    
#    roundData.save('round_data.xlsx')            
#    modelData.save('model_data.xlsx')

##############TEST###########
#Data goes as far as 3574
#rnd=6547
#risk=.5
#AllTaverns, winners=load_past_data(rnd)
#mybets, TER=calc_bet(risk)
#payoff=calc_winnings(mybets,winners)
#print(payoff)
#
#todaysbets=calc_bet(risk)
#calc_bust(calc_cumulative(mybets),mybets,rnd,risk)
#print("TER: %.2f" %TER)
##########################################
#risks=[.5]
#rounds=[6520]
#test_amount=1
#test_model(risks,rounds,test_amount)