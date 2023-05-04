import clubs
from clubs_gym.agent import base
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Input, Concatenate
from keras.optimizers import Adam
from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess


class DDPG(base.BaseAgent):
    def __init__(self, env):
        super().__init__()
        self.action_size = env.action_space.n
        self.input_shape = (1, 35)

        actor = self.build_actor()
        critic, critic_action_input = self.build_critic()

        memory = SequentialMemory(limit=100000, window_length=1)
        random_process = OrnsteinUhlenbeckProcess(size=self.action_size, theta=.3, mu=self.action_size/2., sigma=100)

        self.agent = DDPGAgent(nb_actions=self.action_size, actor=actor, critic=critic, critic_action_input=critic_action_input, memory=memory,
                               nb_steps_warmup_critic=100, nb_steps_warmup_actor=100, random_process=random_process,
                               gamma=.99, target_model_update=1e-3)
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

    def build_actor(self):
        inputs = Input(shape=self.input_shape)
        x = Flatten()(inputs)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(self.action_size, activation='sigmoid')(x)
        return Model(inputs=inputs, outputs=outputs)

    def build_critic(self):
        action_input = Input(shape=(self.action_size,))
        observation_input = Input(shape=self.input_shape)
        x = Flatten()(observation_input)
        x = Concatenate()([x, action_input])
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(1, activation='sigmoid')(x)
        return Model(inputs=[action_input, observation_input], outputs=outputs), action_input

    def act(self, obs):
        action = self.agent.forward(obs)
        #print("a ", action)
        scaled_action = action[0] * self.action_size
        #print("c ", scaled_action)
        return scaled_action

    def store_experience(self, action, reward, obs, done):
        self.agent.memory.append(action, reward, obs, done)

    def backward(self, rewards, terminal):
        self.agent.backward(rewards, terminal)

