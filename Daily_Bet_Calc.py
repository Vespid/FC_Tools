import food_tools as ft

rnd="6549"
risk=0.955

ft.get_past_data(int(rnd))
AllTaverns=ft.get_soup_data()
todaysbets,TER=ft.calc_bet(risk)
localdf=ft.calc_cumulative(todaysbets)
ft.calc_bust(localdf,todaysbets,rnd,risk)
print("TER: %.2f" %TER)
ft.start()
ft.daqtools(todaysbets)