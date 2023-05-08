import clubs
from clubs_gym.agent import base
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy


class SARSA(base.BaseAgent):
    def __init__(self, env, name):
        super().__init__()
        self.name = name
        self.color = 'orange'

        self.reward_history = []
        self.action_size = env.action_space.n
        self.input_shape = (1, 35)

        model = self.build_model()

        policy = EpsGreedyQPolicy(eps=0.1)

        self.agent = SARSAAgent(model=model, nb_actions=self.action_size, nb_steps_warmup=100,
                                policy=policy, gamma=.99)
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

    def build_model(self):
        model = Sequential()
        model.add(Flatten(input_shape=self.input_shape))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        return model

    def act(self, obs):
        self.agent.reset_states()
        return self.agent.forward(obs)
    
    def store_experience(self, action, reward, obs, done):
        pass

    def backward(self, rewards, terminal):
        self.agent.backward(rewards, terminal)
