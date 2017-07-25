import food_tools as ft
import warnings
import math, time

warnings.filterwarnings('ignore')

rnd=math.floor((time.time()-926028865)/60/60/24)
risk=1
max_bet=7500



#####Calculate Today's Round#####

Arenas,est_prob,Payouts,OpenOdds=ft.get_todays_data()
combos, Odds = ft.AORO_combos(Arenas, OpenOdds, Payouts)
bets, TER=ft.max_TER_bets(combos, max_bet, risk)

ft.reddit_format(rnd,bets)
