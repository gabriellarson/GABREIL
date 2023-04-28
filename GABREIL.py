import gym
from gym import spaces
import clubs_gym

from DQNAgent import DQN

def main():
    env = gym.make("NoLimitHoldemNinePlayer-v0", disable_env_checker=True)
    agents = [DQN(env) for _ in range(9)]
    env.register_agents(agents)

    obs = env.reset()

    for i in range(10):
        while True:
            bet = env.act(obs)
            obs, rewards, done, info = env.step(bet)

            if done:
                print(rewards)
                obs = env.reset()
                break

if __name__ == "__main__":
    main()
