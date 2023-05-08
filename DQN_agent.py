import clubs
from clubs_gym.agent import base
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory


class DQN(base.BaseAgent):
    def __init__(self, env, name):
        super().__init__()
        self.name = name
        self.color = 'red'
        
        self.action_size = env.action_space.n
        self.input_shape = (1,35)

        model = Sequential()
        model.add(Flatten(input_shape=self.input_shape))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='sigmoid'))

        memory = SequentialMemory(limit=100000, window_length=1)
        policy = EpsGreedyQPolicy(eps=0.1)

        self.agent = DQNAgent(model=model, nb_actions=self.action_size, memory=memory, nb_steps_warmup=100,
                              target_model_update=1e-2, policy=policy)
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

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


