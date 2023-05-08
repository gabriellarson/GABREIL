import clubs
from clubs_gym.agent import base
import numpy as np

class RandomAgent(base.BaseAgent):
    def __init__(self, env, name):
        super().__init__()
        self.name = name
        self.color = 'purple'
        self.action_size = env.action_space.n

    def act(self, obs):
        return np.random.randint(self.action_size)

    def store_experience(self, action, reward, obs, done):
        pass

    def backward(self, rewards, terminal):
        pass
