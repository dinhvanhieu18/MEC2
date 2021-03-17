from behaviorPolicy.policy import Policy
import numpy as np

class EpsilonGreedy(Policy):
    
    def __init__(self, nActions, epsilon=0.1):
        self.nActions = nActions
        self.epsilon = epsilon

    def getPolicy(self):
        def chooseAction(values_of_all_actions):
            prob_taking_best_action_only = 1 - self.epsilon
            prob_taking_any_random_action = self.epsilon / self.nActions
            action_prob_vertor = [prob_taking_any_random_action] * self.nActions
            exploitation_action_index = np.argmax(values_of_all_actions)
            action_prob_vertor[exploitation_action_index] += prob_taking_best_action_only
            chosen_action = np.random.choice(np.arange(self.nActions), p=action_prob_vertor)
            return chosen_action
        return chooseAction