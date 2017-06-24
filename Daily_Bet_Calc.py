import food_tools as ft
import warnings
import time, math
warnings.filterwarnings('ignore')

rnd=math.floor((time.time()-926028865)/60/60/24)
risk=1
max_bet=10100



#####Calculate Today's Round#####
#a,o,p=ft.get_todays_data()
#combodf=ft.calc_combos(a,o,p)
#bets,TER=ft.calc_bets(combodf, max_bet, risk)
#ft.calc_bust(ft.calc_cumulative(bets, ft.calc_oddsdf(bets, o)),bets,rnd,risk)

bets,TER,combos=ft.today_AORO_bets(max_bet, risk)


ft.start()
time.sleep(2)
ft.daqtools(bets,max_bet)


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