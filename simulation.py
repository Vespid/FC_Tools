import food_tools as ft
import pickle
import random
import warnings
warnings.filterwarnings('ignore')
##############TEST###########
#Have data from 3574 to 6547
data_file=open("fcwin_data.pickle","rb")
FC_data = pickle.load(data_file)
datarange=list(FC_data.keys())
data_file.close()
#--------------USER INPUTS--------------
risks=[1]
max_bet=1000

Random=True
test_amount=10
days=30

r_start=3574
r_end=6499

start=[6265,6296,6327,6357,6388,6418,6449,6480,6508]
end=[6295,6326,6356,6387,6417,6448,6479,6507,6538]

#start=[3574,4001,4251,4501,4751,5001,5251,5501,5751,6001,6251]
#end=[4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6538]

start=[3574]
end=[6499]

for x in range(len(start)):
    r_start=start[x]
    r_end=end[x]
##6265-6538
#---------------------------------------
    if Random==False:
        test_amount=1
        
    for tests in range(test_amount):
        if Random==True:
            rounds=random.sample(datarange,days)
            print(rounds)
        else:
            x=list(range(r_start,r_end+1))
            rounds=[y for y in x if y in datarange]
            print("Start:",start,"End",end)
#        print("Test: %d" %(tests+1))
        print(" ")
#        ft.test_model(risks,rounds,max_bet)
#        ft.test_dumb_model(risks,rounds,max_bet)
        ft.test_daq_model(risks,rounds,max_bet)
#        ft.test_vdaq_model(risks,rounds,max_bet)
#        ft.test_clf_model(risks,rounds,max_bet)
        ft.test_ao_model(risks,rounds,max_bet)
#        ft.test_value_model(risks,rounds,max_bet)
        ft.test_AORO(risks,rounds,max_bet)
        ft.test_newodd(risks,rounds,max_bet)
print("Done")

#ft.get_past_data(6551)
