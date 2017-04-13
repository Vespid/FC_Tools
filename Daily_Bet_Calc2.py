import food_tools2 as ft
import warnings
warnings.filterwarnings('ignore')

rnd=0
risk=0.955
max_bet=9442

a,o,p=ft.get_todays_data()
combodf=ft.calc_combos(a,o,p)
bets=ft.calc_bets(combodf, max_bet, risk)
ft.calc_bust(ft.calc_cumulative(bets, ft.calc_oddsdf(bets, o)),bets,rnd,risk)





#####Calculate Past Round#####
#ft.get_past_data(rnd)
#a,o,p,w=ft.load_past_data(rnd)
#combodf=ft.calc_combos(a,o,p)
#bets=ft.calc_bets(combodf, max_bet, risk)
#print(w)
#print(ft.calc_winnings(bets,w))
#
#ft.calc_bust(ft.calc_cumulative(bets, ft.calc_oddsdf(bets, o)),bets,rnd,risk)