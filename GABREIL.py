import os
import gym
import clubs_gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from envWrapper import envWrapper
from DQNAgent import DQN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


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

    agents = [DQN1, DQN2, DQN3, DQN4, DQN5, DQN6, DQN7, DQN8, DQN9]
    env.register_agents(agents)


def main():
    env = create_env()
    register_agents(env)

    n_episodes = 100000
    cumulative_rewards = np.zeros((n_episodes, 9))

    for episode in range(n_episodes):
        episode_rewards = np.zeros(9)
        done = False
        actions = []
        obs = env.reset(reset_stacks=True)
        while not done:
            for agent in env.agents.values():
                action = env.act(obs)
                actions.append(action)

                obs, rewards, done, info = env.step(action)

                agent.store_experience(action, rewards, obs, done)
                agent.backward(rewards, terminal=done)
                agent.reward_history.append(rewards)

                episode_rewards += rewards

        cumulative_rewards[episode] = episode_rewards + cumulative_rewards[episode-1] if episode > 0 else episode_rewards

    
    plt.title("Cumulative rewards")
    plt.xlabel("Episode")
    plt.ylabel("Cumulative reward")
    for i in range(9):
        plt.plot(cumulative_rewards[:,i], label="Player " + str(i+1))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()


