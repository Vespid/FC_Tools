import pandas as pd
from selenium import webdriver
import math, time
rnd=math.floor((time.time()-926028865)/60/60/24)

pirates=["","Scurvy Dan the Blade",
"Young Sproggie",
"Orvinn the First Mate",
"Lucky McKyriggan",
"Sir Edmund Ogletree",
"Peg Leg Percival",
"Bonnie Pip Culliford",
"Puffo the Waister",
"Stuff-A-Roo",
"Squire Venable",
"Captain Crossblades",
"Ol' Stripey",
"Ned the Skipper",
"Fairfax the Deckhand",
"Gooblah the Grarrl",
"Franchisco Corvallio",
"Federismo Corvallio",
"Admiral Blackbeard",
"Buck Cutlass",
"The Tailhook Kid",
]

probDict={2:0.5226,3:0.29166666666666663,4:0.225,5:0.18333333333333335,6:0.15476190476190477,7:0.13392857142857142,8:0.11805555555555555,9:0.10555555555555556,10:0.09545454545454546,11:0.08712121212121213,12:0.08012820512820512,13:.05}

def start():
    global browser
    FirefoxProfile=r'C:\Users\Vincent\AppData\Roaming\Mozilla\Firefox\Profiles\yxempuro.default'
    profile = webdriver.FirefoxProfile(FirefoxProfile)
    browser = webdriver.Firefox(profile)
    
def get_initialNeodata():
    browser.get("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    current_pirate_odds=browser.execute_script("return pirate_odds;")
    current_pirate_odds.pop(0)
    OpenOdds={}; ArenasDict={}; 
    for pirate_index in range(1,len(pirates)):
        pirateName=pirates[pirate_index]
        OpenOdds[pirateName]=current_pirate_odds[pirate_index]
        ArenasDict[pirateName]=math.floor(pirate_index/4)+1
    ArenaFoods={}          
    for arenaIndex in range(1,6):          
        browser.get("http://www.neopets.com/pirates/foodclub.phtml?type=current&id=%d" % arenaIndex)
        linkElems=browser.find_elements_by_tag_name("a")
        foodList=[]
        for foodIndex in range(85,96):
            foodList.append(linkElems[foodIndex].text)
        ArenaFoods[arenaIndex]=foodList
          
    data=pd.DataFrame(list(ArenasDict.items()),columns=["Pirate","Arena"])
    
    Arenas=[list(data[data["Arena"]==x]["Pirate"]) for x in range(1,6)]
    Odds=daq_combos(Arenas, OpenOdds)
    
    data["OpenOdds"]=data["Pirate"]
    data["OpenOdds"].update(data["Pirate"].map(OpenOdds))
    data["Payout"]=data["Pirate"]
    data["Payout"].update(data["Pirate"].map(OpenOdds))
    data["EstProb"]=data["Pirate"]
    data["EstProb"].update(data["Pirate"].map(Odds))
    data["ExpectedRatio"]=data["EstProb"]*data["Payout"]

    data["Foods"]=data["Arena"]
    data["Foods"].update(data["Arena"].map(ArenaFoods))

def daq_combos(Arenas, OpenOdds):
    detail=[]; prates=[]
    for y in range(len(Arenas)):
        open_odds=[]; summation=0
        for x in Arenas[y]:
            open_odds.append(probDict[OpenOdds[x]])
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
    
    return Odds

def get_info(data):    
    Arenas=[list(data[data["Arena"]==x]["Pirate"]) for x in range(1,6)]
    
def updateDF(data):
    browser.get("http://www.neopets.com/pirates/foodclub.phtml?type=bet")
    current_pirate_odds=browser.execute_script("return pirate_odds;")
    current_pirate_odds.pop(0)
    Payout={};
    for pirate_index in range(len(pirates)):
        pirateName=pirates[pirate_index]
        Payout[pirateName]=current_pirate_odds[pirate_index]
    data["Payout"]=data["Pirate"]
    data["Payout"].update(data["Pirate"].map(OpenOdds))
    return data,Payout