import food_tools as ft
import warnings
import math, time
import pickle

warnings.filterwarnings('ignore')

rnd=math.floor((time.time()-926028865)/60/60/24)
risk=0.95
max_bet=1000



#####Calculate Today's Round#####
a,o,p,oo=ft.get_todays_data()
combodf=ft.calc_combos(a,o,p)
bets,TER=ft.calc_bets(combodf, max_bet, risk)
ft.reddit_format(rnd,bets)

#ft.calc_bust(ft.calc_cumulative(bets, ft.calc_oddsdf(bets, o)),bets,rnd,risk)
#ft.start()
#ft.daqtools(bets,max_bet)


#import time
#t1=time.time()
######Calculate Past Round#####
#ft.get_past_data(rnd)
#a,o,p,w=ft.load_past_data(rnd)
#combodf=ft.calc_combos(a,o,p)
#
#bets=ft.calc_bets(combodf, max_bet, risk)
##
#print(ft.calc_winnings(bets,w))
##
##
#clfbets=ft.clf_bet(combodf, max_bet, risk)
#print(ft.calc_winnings(clfbets,w))
#ft.calc_bust(ft.calc_cumulative(clfbets, ft.calc_oddsdf(clfbets, o)),clfbets,rnd,risk)

#zoso=ft.daq_bets(rnd, max_bet, risk)
#a,o,p,w=ft.calc_odds(rnd)
#combodf=ft.calc_combos(a,o,p)
#bets=ft.calc_bets(combodf, max_bet, risk)
#
#redditbet_file=open("MyRedditBets.pickle","rb")
#reddit_bets = pickle.load(redditbet_file)
#redditbet_file.close()
#reddit_bets[rnd]=bets
#redditbet_file=open("MyRedditBets.pickle","wb")
#pickle.dump(reddit_bets, redditbet_file)
#redditbet_file.close()