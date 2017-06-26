import food_tools as ft
import numpy as np
import pickle
import random
import warnings
warnings.filterwarnings('ignore')
##############TEST###########
#Have data from 3574 to 6547
data_file=open("fcwin_data.pickle","rb")
win_data = pickle.load(data_file)
datarange=list(win_data.keys())
data_file.close()
#--------------USER INPUTS--------------
risks=1
max_bet=8000

Random=True
test_amount=15
days=30


#start=[6265,6296,6327,6357,6388,6418,6449,6480,6508]
#end=[6295,6326,6356,6387,6417,6448,6479,6507,6538]

start=[6535]
end=[6538]


DAQ_TER=[]; AORO_TER=[]
print("Max Bet:",max_bet)
for x in range(len(start)):
    r_start=start[x]
    r_end=end[x]

    if Random==False:
        test_amount=1
        
    for tests in range(test_amount):
        if Random==True:
            rounds=random.sample(datarange,days)
#            print(rounds)
        else:
            x=list(range(r_start,r_end+1))
            rounds=[y for y in x if y in datarange]
            print("\nStart:",r_start,"End:",r_end)
#        print("Test: %d" %(tests+1))
        print(" ")
        DAQ_TER.append(ft.test_daq_model(risks,rounds,max_bet))     #daqtools
        AORO_TER.append(ft.test_AORO(risks,rounds,max_bet))         #AORO method
print("Done\n")
print("DAQ:",np.mean(DAQ_TER), np.std(DAQ_TER))
print("AORO:",np.mean(AORO_TER), np.std(AORO_TER))
