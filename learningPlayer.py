import pokerPlayer
import numpy as np
import tensorflow as tf
from tensorflow import keras
import OUActionNoise
import collections

class learningPlayer(pokerPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.model = self.model()
        self.epsilon = 0.1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.gamma = 0.95
        self.learning_rate = 0.001
        self.memory = deque(maxlen=2500)

    def model():
        inputs = keras.Input()
        x = keras.layers.Dense(64, activation="relu")(inputs)
        outputs = keras.layers.Dense(1)(x)
        model = keras.Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer='rmsprop', loss='mse')
        return model

    def train(self, gamestate, action, reward, next_gamestate, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_gamestate)[0])
        target_f = self.model.predict(gamestate)
        target_f[0][action] = target
        self.model.fit(gamestate, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def takeAction(self, gamestate):
        if np.random.rand() <= self.epsilon:
            return ['fold', 0] #explorartory action
        return np.argmax(self.model.predict(gamestate)) #exploitative action

    
        