import gym
from gym import spaces
#import clubs_gym

import numpy as np

from envWrapper import envWrapper

from DQNAgent import DQN

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from copy import deepcopy

def main():
    env = gym.make("NoLimitHoldemNinePlayer-v0", disable_env_checker=True)
    env = envWrapper(env)
    agents = [DQN(env) for _ in range(9)]
    env.register_agents(agents)

    n_episodes = 100

    for episode in range(n_episodes):
        print("Episode:", episode)
        episode_rewards = np.zeros(9)
        done = False

        actions = []
        i = 0
        obs = env.reset(reset_stacks=True)
        while not done:
            print("NUMBER ", i, ", ", obs)
            i += 1

            for agent in env.agents.values():
                action = env.act(obs)
                actions.append(action)

                obs, rewards, done, info = env.step(action)
                agent.store_experience(actions, rewards, obs, done)
                
                copy = deepcopy(env)
                agent.train(copy, nb_steps=1)

                episode_rewards += rewards

        print("Episode rewards:", episode_rewards)

if __name__ == "__main__":
    main()
