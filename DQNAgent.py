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
    def __init__(self, env):
        super().__init__()
        self.action_size = env.action_space.n
        self.input_shape = (1,35)

        # Define the model architecture
        model = Sequential()
        model.add(Flatten(input_shape=self.input_shape))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        # Define the memory and policy
        memory = SequentialMemory(limit=100000, window_length=1)
        policy = EpsGreedyQPolicy(eps=0.1)

        # Compile the agent
        self.agent = DQNAgent(model=model, nb_actions=self.action_size, memory=memory, nb_steps_warmup=100,
                              target_model_update=1e-2, policy=policy)
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])

    def act(self, obs):
        # Preprocess the observation
        processed_obs = process_observation(obs)

        # Get the action from the agent
        action = self.agent.forward(processed_obs)

        # Return the action as an integer
        return np.argmax(action)



    
def process_observation(obs):
    def convert_to_numbers(value):
        if isinstance(value, clubs.poker.card.Card):
            return card_to_number(value)
        else:
            return value

    processed_obs = []
    for v in obs.values():
        v = np.array(v)
        v = np.vectorize(convert_to_numbers, otypes=[np.float])(v)
        processed_obs.append(v.flatten())

    return np.concatenate(processed_obs)


def card_to_number(card):
    return card_rank_values[card.rank] + 13 * card_suit_values[card.suit]
card_suit_values = {
    '♠': 0.0,
    '♥': 1.0,
    '♦': 2.0,
    '♣': 3.0
}
        
card_rank_values = {
    'A': 1.0,
    '2': 2.0,
    '3': 3.0,
    '4': 4.0,
    '5': 5.0,
    '6': 6.0,
    '7': 7.0,
    '8': 8.0,
    '9': 9.0,
    'T': 10.0,
    'J': 11.0,
    'Q': 12.0,
    'K': 13.0
}