import numpy as np
from masced_bandits.bandits.Bandit import Bandit
from collections import deque


REWARD = 0
ACTION = 1
XI = 2


class SWUCB(Bandit):
    def __init__(self, **kwargs):
        super().__init__("SWUCB-" + str(kwargs))

        self.look_back = int(kwargs.get("look_back",10))

        self.bandit_round = -1
        self.game_list = deque(maxlen=self.look_back)

    def get_next_arm(self, reward):
               
        self.game_list.append([reward, self.last_action])

        self.bandit_round = self.bandit_round + 1

        if((self.bandit_round) < (len(self.arms))):
            #initial exploration      
            next_arm = self.arms[self.bandit_round]
        else:
            next_arm = max(self.arms, key=lambda arm: \
                       self.X_t(arm) + self.c_t(arm))

        self.last_action = next_arm
        return next_arm

    def N_t(self, arm):
        count = 0
        for game in self.game_list:
            if(game[ACTION] == arm): count += 1

        return count

    def X_t(self, arm):

        summated = 0

        
        for current_game in self.game_list:
            if(current_game[ACTION] == arm): #the games in which i was the arm
                X_s = current_game[REWARD]
                summated+=X_s
        try:
            times_arm_played = self.N_t(arm) 
            if(summated == 0 or times_arm_played == 0): return 0
            
            return summated/self.N_t(arm)
        except:
            print("Divide by zero error likely")
            print(self.game_list)
            print("Last tau games are")
            print(self.game_list[-self.look_back:])
            print("Length of game list is ")
            print(len(self.game_list))
            print("Result of N_t that was trigger is ")
            print(self.N_t(arm))
            print("and the arm causing it was ")
            print(arm)
            print("Value of summated is ")
            print(summated)
            exit(1)

        
    def c_t(self, arm):
        res = self.chapter7(arm, len(self.game_list)) #t or tau has become unnecessary

        return res
    
    def sqreward_average(self, arm):
        r_sum = 0

        for game in self.game_list:  
            if(game[ACTION] == arm):
                r_sum+=np.square(game[REWARD])

        times_arm_played = self.N_t(arm) 
        if(r_sum == 0 or times_arm_played == 0): return 0
            
        return r_sum/times_arm_played
    
    def tuned(self, arm, n):
        n_k = self.N_t(arm)

        average_of_squares = self.sqreward_average(arm)
        square_of_average = np.square(self.X_t(arm))
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_k = estimated_variance + np.sqrt(2 * param)

        return np.sqrt(param * V_k)
    
    def chapter7(self, arm, n):
        DELTA = 1 / np.square(self.look_back)

        n_k = self.N_t(arm)


        upper_term = 2 * np.log( (1 / DELTA) )
        
        to_be_sqrt = upper_term/n_k
        
        return np.sqrt(to_be_sqrt)
        


