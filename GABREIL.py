import os
import gym
import time
import clubs_gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from envWrapper import envWrapper
from SARSAAgent import SARSA
from DDPGAgent import DDPG
from DQNAgent import DQN
from CEMAgent import CEM

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

####CONFIG####
num_episodes = 10000
ddpg = True
dqn = True
sarsa = False
cem = False
###############

def create_env():
    env = gym.make("NoLimitHoldemNinePlayer-v0", disable_env_checker=True)
    env = envWrapper(env)
    return env

def create_agents(env):
    agents = []
    if(dqn):
        DQN1 = DQN(env, "DQN1")
        DQN2 = DQN(env, "DQN2")
        DQN3 = DQN(env, "DQN3")
        DQN4 = DQN(env, "DQN4")
        DQN5 = DQN(env, "DQN5")
        DQN6 = DQN(env, "DQN6")
        DQN7 = DQN(env, "DQN7")
        DQN8 = DQN(env, "DQN8")
        DQN9 = DQN(env, "DQN9")
        agents.append(DQN1)
        agents.append(DQN2)
        agents.append(DQN3)
        agents.append(DQN4)
        agents.append(DQN5)
        agents.append(DQN6)
        agents.append(DQN7)
        agents.append(DQN8)
        agents.append(DQN9)

    if(ddpg):
        DDPG1 = DDPG(env, "DDPG1")
        DDPG2 = DDPG(env, "DDPG2")
        DDPG3 = DDPG(env, "DDPG3")
        DDPG4 = DDPG(env, "DDPG4")
        DDPG5 = DDPG(env, "DDPG5")
        DDPG6 = DDPG(env, "DDPG6")
        DDPG7 = DDPG(env, "DDPG7")
        DDPG8 = DDPG(env, "DDPG8")
        DDPG9 = DDPG(env, "DDPG9")
        agents.append(DDPG1)
        agents.append(DDPG2)
        agents.append(DDPG3)
        agents.append(DDPG4)
        agents.append(DDPG5)
        agents.append(DDPG6)
        agents.append(DDPG7)
        agents.append(DDPG8)
        agents.append(DDPG9)

    if(sarsa):
        SARSA1 = SARSA(env, "SARSA1")
        SARSA2 = SARSA(env, "SARSA2")
        SARSA3 = SARSA(env, "SARSA3")
        SARSA4 = SARSA(env, "SARSA4")
        SARSA5 = SARSA(env, "SARSA5")
        SARSA6 = SARSA(env, "SARSA6")
        SARSA7 = SARSA(env, "SARSA7")
        SARSA8 = SARSA(env, "SARSA8")
        SARSA9 = SARSA(env, "SARSA9")
        agents.append(SARSA1)
        agents.append(SARSA2)
        agents.append(SARSA3)
        agents.append(SARSA4)
        agents.append(SARSA5)
        agents.append(SARSA6)
        agents.append(SARSA7)
        agents.append(SARSA8)
        agents.append(SARSA9)

    if(cem):
        CEM1 = CEM(env, "CEM1")
        CEM2 = CEM(env, "CEM2")
        CEM3 = CEM(env, "CEM3")
        CEM4 = CEM(env, "CEM4")
        CEM5 = CEM(env, "CEM5")
        CEM6 = CEM(env, "CEM6")
        CEM7 = CEM(env, "CEM7")
        CEM8 = CEM(env, "CEM8")
        CEM9 = CEM(env, "CEM9")
        agents.append(CEM1)
        agents.append(CEM2)
        agents.append(CEM3)
        agents.append(CEM4)
        agents.append(CEM5)
        agents.append(CEM6)
        agents.append(CEM7)
        agents.append(CEM8)
        agents.append(CEM9)

    return agents

def create_plots(rewards, agents):
    #for agent in agents: #apply moving average smoothing
        #cumrewards[agent.name] = np.convolve(cumrewards[agent.name], np.ones((1,)), mode='valid')
    
    plt.title("Cumulative rewards, All Players")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative reward")
    for agent in agents:
        plt.plot(rewards[agent.name], label=agent.name, color=agent.color)
    plt.legend()
    plt.show()
    print("")


    max_ddpg = 0
    min_ddpg = num_episodes
    max_dqn = 0
    min_dqn = num_episodes
    max_sarsa = 0
    min_sarsa = num_episodes
    max_cem = 0
    min_cem = num_episodes
    max_length = 0
    min_length = num_episodes
    for agent in agents:
        length = len(rewards[agent.name])
        if(agent.name.startswith("DDPG") and length < min_ddpg):
            min_ddpg = length
        if(agent.name.startswith("DQN") and length < min_dqn):
            min_dqn = length
        if(agent.name.startswith("SARSA") and length < min_sarsa):
            min_sarsa = length
        if(agent.name.startswith("CEM") and length < min_cem):
            min_cem = length
        if (length < min_length):
            min_length = length

    cum_ddpg = np.zeros(min_length)
    cum_dqn = np.zeros(min_length)
    cum_sarsa = np.zeros(min_length)
    cum_cem = np.zeros(min_length)

    for agent in agents:
        for i in range(min_length):
            if(agent.name.startswith("DDPG")):
                cum_ddpg[i] += rewards[agent.name][i]
            if(agent.name.startswith("DQN")):
                cum_dqn[i] += rewards[agent.name][i]
            if(agent.name.startswith("SARSA")):
                cum_sarsa[i] += rewards[agent.name][i]
            if(agent.name.startswith("CEM")):
                cum_cem[i] += rewards[agent.name][i]

    plt.title("Cumulative rewards, Average per Agent Type")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative reward")
    if(ddpg):
        plt.plot(cum_ddpg, label = "DDPG", color="blue")
    if(dqn):
        plt.plot(cum_dqn, label = "DQN", color="red")
    if(sarsa):
        plt.plot(cum_sarsa, label = "SARSA", color="orange")
    if(cem):
        plt.plot(cum_cem, label = "CEM", color="green")
    plt.legend()
    plt.show()

def main():
    env = create_env()
    agents = create_agents(env)

    n_episodes = num_episodes
    cum_rewards = {}

    start_time = time.time()
    for episode in range(1,n_episodes+1):
        if(episode % 100 == 0):
            elapsed_time = np.round(time.time() - start_time,1)
            time_left = np.round(elapsed_time / (episode+1) * (n_episodes - episode),1)
            print("Episode", episode, "/", n_episodes,",", elapsed_time, "/", time_left, "s               ",  end = '\r')

        env = create_env()
        players = np.random.choice(agents, 9, replace=False).tolist()
        env.register_agents(players)

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

        for i, player in enumerate(players):
            if player.name not in cum_rewards:
                cum_rewards[player.name] = [0]
            cum_reward = cum_rewards[player.name]
            new_reward = episode_rewards[i] + cum_reward[-1]

            cum_reward.append(new_reward)


    create_plots(cum_rewards, agents)

if __name__ == "__main__":
    main()