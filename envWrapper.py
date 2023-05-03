import gym
import numpy as np
import clubs
from copy import deepcopy
import tempfile
from keras.models import load_model
import pickle

class envWrapper(gym.Wrapper):
    def __init__(self, env):
        super(envWrapper, self).__init__(env)

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        return dict_to_numpy_array(obs).astype(np.float32), reward, done, {}

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        return dict_to_numpy_array(obs).astype(np.float32)
    
    
def dict_to_numpy_array(obs):
    def convert_to_numbers(value):
        if isinstance(value, clubs.poker.card.Card):
            return card_to_number(value)
        else:
            return value

    processed_obs = []
    for v in obs.values():
        v = np.array(v)
        v = np.vectorize(convert_to_numbers, otypes=[np.float32])(v)
        processed_obs.append(v.flatten())

    return np.concatenate(processed_obs).astype(np.float32)
    
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