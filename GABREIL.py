import os
import gym
import time
import clubs_gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from envWrapper import envWrapper
from DQNAgent import DQN
from DDPGAgent import DDPG

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


####CONFIG####
num_episodes = 100000
ddpg = True
dqn = True
sarsa = False
cem = False
###############


def create_env():
    env = gym.make("NoLimitHoldemNinePlayer-v0", disable_env_checker=True)
    env = envWrapper(env)
    return env

def register_agents(env):
    DQN1 = DQN(env)
    DQN2 = DQN(env)
    DQN3 = DQN(env)
    DQN4 = DQN(env)
    DQN5 = DQN(env)
    DQN6 = DQN(env)
    DQN7 = DQN(env)
    DQN8 = DQN(env)
    DQN9 = DQN(env)

    DDPG1 = DDPG(env)
    DDPG2 = DDPG(env)
    DDPG3 = DDPG(env)
    DDPG4 = DDPG(env)
    DDPG5 = DDPG(env)
    DDPG6 = DDPG(env)
    DDPG7 = DDPG(env)
    DDPG8 = DDPG(env)
    DDPG9 = DDPG(env)


    agents = [DQN1, DQN2, DQN3, DQN4, DQN5, DQN6, DQN7, DQN8, DQN9]
    #agents = [DDPG1, DDPG2, DDPG3, DDPG4, DDPG5, DDPG6, DDPG7, DDPG8, DDPG9]
    #agents = [DDPG1, DQN2, DDPG3, DQN4, DDPG5, DQN6, DDPG7, DQN8, DDPG9]
    env.register_agents(agents)

    return agents

def main():
    start_time = time.time()
    env = create_env()
    agents = register_agents(env)

    n_episodes = num_episodes
    cumulative_rewards = np.zeros((n_episodes, 9))

    for episode in range(n_episodes):
        if(episode % 100 == 0):
            elapsed_time = np.round(time.time() - start_time,1)
            time_left = np.round(elapsed_time / (episode+1) * (n_episodes - episode),1)
            print("Episode", episode, "/", n_episodes,",", elapsed_time, "/", time_left, "s               ",  end = '\r')

        episode_rewards = np.zeros(9)
        done = False
        actions = []
        obs = env.reset(reset_stacks=True, reset_button=False)
        while not done:
            for agent in env.agents.values():
                action = env.act(obs)
                actions.append(action)

                obs, rewards, done, info = env.step(action)

                agent.store_experience(action, rewards, obs, done)
                agent.backward(rewards, terminal=done)

                episode_rewards += rewards

        cumulative_rewards[episode] = episode_rewards + cumulative_rewards[episode-1] if episode > 0 else episode_rewards

    
    plt.title("Cumulative rewards")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative reward")
    for i in range(9):
        plt.plot(cumulative_rewards[:,i], label="Player " + str(i+1))
    plt.legend()
    plt.show()
    print("")


if __name__ == "__main__":
    main()