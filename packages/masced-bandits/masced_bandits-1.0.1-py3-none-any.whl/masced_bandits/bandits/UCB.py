from masced_bandits.bandits.Bandit import Bandit
import numpy as np


FORMULA_FUNC = None

CUM_REWARD = 0
CUM_SQ_REWARD = 1
N_K = 2




trace_len = 15000 #the total time of chosen trace in SWIM in seconds
total_count = round(trace_len / 60) 
DELTA = 1 / np.square(total_count)


class UCB(Bandit):
    def __init__(self, **kwargs):
        formula = kwargs.get("formula","TN")
        super().__init__("UCB-" + formula)
        self.formula = self.formula_to_function(formula)
        
        self.bandit_round = -1
        self.arm_reward_pairs = {}
        for arm in self.arms: self.arm_reward_pairs[arm] = [0.0,0.0,0.0]
        


        
    def get_next_arm(self, reward):
        self.arm_reward_pairs[self.last_action][CUM_REWARD]+=reward
        self.arm_reward_pairs[self.last_action][CUM_SQ_REWARD]+=np.square(reward)
        self.arm_reward_pairs[self.last_action][N_K]+=1

        self.bandit_round+=1

        if((self.bandit_round) < (len(self.arms))):    
            next_arm = self.arms[self.bandit_round]
        else:
            next_arm = max(self.arms, key=lambda arm: \
                       self.reward_average(arm) + self.formula(arm, self.bandit_round))

        self.last_action = next_arm
        return next_arm


    def formula_to_function(self, choice):
        funcs = {
                "FH": self.chapter7,
                "AO": self.asymptotically_optimal,
                "OG": self.auer2002UCB,
                "TN": self.tuned
            }
            
        func = funcs.get(choice)
        #print(func.__doc__)
        return func

    def reward_average(self, arm):
        return self.arm_reward_pairs[arm][CUM_REWARD] / self.arm_reward_pairs[arm][N_K]


    def chapter7(self, arm, n):
        global DELTA

        upper_term = 2 * np.log( (1 / DELTA) )
        
        to_be_sqrt = upper_term/self.arm_reward_pairs[arm][N_K]
        
        return np.sqrt(to_be_sqrt)

    def asymptotically_optimal(self, arm, t):
        T_i = self.arm_reward_pairs[arm][N_K]

        f_t = 1 + (t  * np.square(np.log(t)))

        upper_term = 2 * (np.log(f_t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def auer2002UCB(self, arm, t):
        T_i = self.arm_reward_pairs[arm][N_K]

        upper_term = 2 * (np.log(t))

        lower_term =  T_i

        to_be_sqrt = upper_term/lower_term
        
        return np.sqrt(to_be_sqrt)

    def tuned(self, arm, n):
        n_k = self.arm_reward_pairs[arm][N_K]

        average_of_squares = self.arm_reward_pairs[arm][CUM_SQ_REWARD] / n_k
        square_of_average = np.square(self.arm_reward_pairs[arm][CUM_REWARD]/n_k)
        estimated_variance = average_of_squares - square_of_average
        param = np.log(n) / n_k
        V_k = estimated_variance + np.sqrt(2 * param)

        confidence_value = np.sqrt(param * V_k)
        if(np.isnan(confidence_value)):
            print("\n\n\n\ncaught a nan\n\n\n\n\n")
            return 0
        else:
            return confidence_value

