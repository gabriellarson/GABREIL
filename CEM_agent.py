import clubs
from clubs_gym.agent import base
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory


class CEM(base.BaseAgent):
    def __init__(self, env, name):
        super().__init__()
        self.name = name
        self.color = 'green'
        
        self.action_size = env.action_space.n
        self.input_shape = (1, 35)

        model = self.build_model()

        memory = EpisodeParameterMemory(limit=1000, window_length=1)

        self.agent = CEMAgent(model=model, nb_actions=self.action_size, memory=memory,
                              batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.1)
        self.agent.compile()

    def build_model(self):
        model = Sequential()
        model.add(Flatten(input_shape=self.input_shape))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='sigmoid'))
        return model

    def act(self, obs):
        action = self.agent.forward(obs)
        #print("a ", action)
        scaled_action = action * self.action_size
        #print("c ", scaled_action)
        return scaled_action

    def store_experience(self, action, reward, obs, done):
        self.agent.memory.append(action, reward, obs, done)

    def backward(self, rewards, terminal):
        self.agent.backward(rewards, terminal)