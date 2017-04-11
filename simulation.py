import food_tools
import pickle
import random
##############TEST###########
#Have data from 3574 to 6547
data_file=open("food_data.pickle","rb")
FC_data = pickle.load(data_file)
datarange=list(FC_data.keys())
data_file.close()
#--------------USER INPUTS--------------
risks=[.95,.955]

Random=False
test_amount=1
days=30

r_start=6265
r_end=6295

start=[6265,6296,6327,6357,6388,6418,6449,6480,6508]
end=[6295,6326,6356,6387,6417,6448,6479,6507,6538]

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
        food_tools.test_model(risks,rounds,test_amount)
print("Done")

#ft.get_past_data(6347)