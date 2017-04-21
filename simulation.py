import food_tools2
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
risks=[.95]
max_bet=10000

Random=False
test_amount=1
days=30

r_start=6265
r_end=6295

start=[5251,5501,5751,6001,6250]
end=[5500,5750,6000,6250,6547]


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
#        print("Test: %d" %(tests+1))
        print(" ")
        food_tools2.test_model(risks,rounds,max_bet)
        food_tools2.test_clf_model(risks,rounds,max_bet)
print("Done")

#food_tools2.get_past_data(6551)