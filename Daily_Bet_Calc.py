import food_tools2 as ft
import warnings
warnings.filterwarnings('ignore')

rnd=4180
risk=0.95
max_bet=9960



#####Calculate Today's Round#####
#a,o,p=ft.get_todays_data()
a,o,p=ft.get_api_data()
combodf=ft.calc_combos(a,o,p)
bets=ft.calc_bets(combodf, max_bet, risk)
ft.calc_bust(ft.calc_cumulative(bets, ft.calc_oddsdf(bets, o)),bets,rnd,risk)

#ft.start()
#ft.daqtools(bets,max_bet)


#import time
#t1=time.time()
######Calculate Past Round#####
#ft.get_past_data(rnd)
#a,o,p,w=ft.load_past_data(rnd)
#combodf=ft.calc_combos(a,o,p)
##
#bets=ft.calc_bets(combodf, max_bet, risk)
##
#print(ft.calc_winnings(bets,w))
##
##
#clfbets=ft.clf_bet(combodf, max_bet, risk)
#print(ft.calc_winnings(clfbets,w))
#ft.calc_bust(ft.calc_cumulative(clfbets, ft.calc_oddsdf(clfbets, o)),clfbets,rnd,risk)
