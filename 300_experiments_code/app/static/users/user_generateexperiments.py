import random
import numpy as np

# users = [[1, 'john.doe@hec.edu'], [2, 'anna@hec.edu'], [3, 'clara@hec.edu'], [4, 'luc@gmail.com'], [5, 'sara@gmail.com'], [6, 'lucie@gmail.com'], [7, 'paul@gmail.com'], [8, 'juuli@gmail.com'], [9, 'j@ghj.com'], [10, 'benjamin@gmail.com']]

i=0
while i<1000:
    with open("user_%d_experiments.csv"%i, "w") as file:
        user_experiments = random.sample(np.arange(0,39,1).tolist(), 10)
        for a in user_experiments :
            file.write(str(a) + "\n")
    i += 1
