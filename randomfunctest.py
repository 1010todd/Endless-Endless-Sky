# import the required libraries 
import random 
import matplotlib.pyplot as plt 
    
# store the random numbers in a list 
nums = [] 
mu = 0
kappa = 4
    
for i in range(32): 
    temp = random.vonmisesvariate(mu, kappa) 
    nums.append(temp) 
        
# plotting a graph 
plt.hist(nums, bins = 200) 
plt.show() 