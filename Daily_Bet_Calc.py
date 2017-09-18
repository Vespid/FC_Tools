import food_tools as ft
import warnings
import time, math
warnings.filterwarnings('ignore')

rnd=math.floor((time.time()-926028865)/60/60/24)
risk=1
max_bet=10200


#Arenas,est_prob,Payouts,OpenOdds=ft.get_todays_data()
Arenas, OpenOdds, Payouts, arenaUrl=ft.get_au()
#combos, Odds = ft.AORO_combos(Arenas, OpenOdds, Payouts)
combos, Odds = ft.t13_combos(Arenas, OpenOdds, Payouts)
bets, TER=ft.max_TER_bets(combos, max_bet, risk)

print("TER: ",TER)
OddsDF=ft.calc_oddsdf(bets, Odds)
localdf=ft.calc_cumulative(bets, OddsDF)
ft.calc_bust(localdf,bets,rnd,risk)
ft.au_url(bets, arenaUrl, rnd)


#ft.start()
#time.sleep(2)
#ft.daqtools(bets,max_bet)