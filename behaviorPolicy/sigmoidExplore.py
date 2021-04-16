from behaviorPolicy.policy import Policy
import numpy as np
import math

class SigmoidExplore(Policy):
    # Num action = 2
    def __init__(self, epsilon=0.5, w=1):
        self.w = w
        self.epsilon = epsilon

    def getPolicy(self):
        def chooseAction(values_of_all_actions, exclude_indexs=[]):
            n_actions = len(values_of_all_actions)
            varient = abs(values_of_all_actions[0] - values_of_all_actions[1])
            self.epsilon = 1 - (1 / (1 + math.exp(- self.w * varient)))
            prob_taking_best_action_only = 1 - self.epsilon
            prob_taking_any_random_action = self.epsilon / (n_actions - len(exclude_indexs))
            action_prob_vertor = [prob_taking_any_random_action] * n_actions
            min_values = np.min(values_of_all_actions)
            for i in exclude_indexs:
                action_prob_vertor[i] = 0
                values_of_all_actions[i] = min_values - 1
            exploitation_action_index = np.argmax(values_of_all_actions)
            action_prob_vertor[exploitation_action_index] += prob_taking_best_action_only
            # print(action_prob_vertor)
            chosen_action = np.random.choice(np.arange(n_actions), p=action_prob_vertor)
            return chosen_action
        return chooseAction