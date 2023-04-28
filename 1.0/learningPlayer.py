from pokerPlayer import pokerPlayer
import numpy as np
import random
import tensorflow as tf

class learningPlayer(pokerPlayer):

    def __init__(self, name, state_size, action_size, learning_rate, tau):
        super().__init__(name)
        self.state_size = state_size
        self.action_size = action_size
        #self.action_space_max = action_space_max
        self.learning_rate = learning_rate
        self.tau = tau

        self.actor_model = self.build_actor_model()
        self.critic_model = self.build_critic_model()
        self.target_actor_model = self.build_actor_model()
        self.target_critic_model = self.build_critic_model()

        self.memory = []
        self.gamma = 0.99

    def build_actor_model(self):
        # Define the architecture of the actor model
        state_input = tf.keras.layers.Input(shape=(self.state_size,))
        dense1 = tf.keras.layers.Dense(24, activation='relu')(state_input)
        #dense2 = tf.keras.layers.Dense(48, activation='relu')(dense1)
        output = tf.keras.layers.Dense(self.action_size, activation='tanh')(dense1)

        model = tf.keras.models.Model(inputs=state_input, outputs=output)
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        return model

    def build_critic_model(self):
        # Define the architecture of the critic model
        state_input = tf.keras.layers.Input(shape=(self.state_size,))
        action_input = tf.keras.layers.Input(shape=(self.action_size,))
        state_dense = tf.keras.layers.Dense(24, activation='relu')(state_input)
        state_dense = tf.keras.layers.Dense(48)(state_dense)
        combined = tf.keras.layers.concatenate([state_dense, action_input])
        dense1 = tf.keras.layers.Dense(24, activation='relu')(combined)
        output = tf.keras.layers.Dense(1, activation='linear')(dense1)

        model = tf.keras.models.Model(inputs=[state_input, action_input], outputs=output)
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate))

        return model

    def update_target_models(self):
        actor_weights = self.actor_model.get_weights()
        actor_target_weights = self.target_actor_model.get_weights()
        for i in range(len(actor_weights)):
            actor_target_weights[i] = self.tau * actor_weights[i] + (1 - self.tau) * actor_target_weights[i]
        self.target_actor_model.set_weights(actor_target_weights)

        critic_weights = self.critic_model.get_weights()
        critic_target_weights = self.target_critic_model.get_weights()
        for i in range(len(critic_weights)):
            critic_target_weights[i] = self.tau * critic_weights[i] + (1 - self.tau) * critic_target_weights[i]
        self.target_critic_model.set_weights(critic_target_weights)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        state = np.reshape(state, [1, self.state_size])
        action = self.actor_model.predict(state)[0]
        return action

    def replay(self, batch_size):
        # Sample a batch of experiences from memory
        mini_batch = random.sample(self.memory, batch_size)
        states = np.zeros((batch_size, self.state_size))
        actions = np.zeros((batch_size, self.action_size))
        rewards = np.zeros((batch_size, 1))
        next_states = np.zeros((batch_size, self.state_size))
        dones = np.zeros((batch_size, 1))

        for i in range(batch_size):
            states[i] = mini_batch[i][0]
            actions[i] = mini_batch[i][1]
            rewards[i] = mini_batch[i][2]
            next_states[i] = mini_batch[i][3]
            dones[i] = mini_batch[i][4]

        # Predict the Q-value using the target critic model
        next_actions = self.target_actor_model.predict(next_states)
        q_values = self.target_critic_model.predict([next_states, next_actions])

        # Update the critic model
        target = rewards + self.gamma * q_values * (1 - dones)
        self.critic_model.fit([states, actions], target, epochs=1, verbose=0)

        # Update the actor model
        action_gradients = np.reshape(self.critic_model.get_gradients([states, actions, 0]), (batch_size, self.action_size))
        self.actor_model.fit(states, action_gradients, epochs=1, verbose=0)
    
    def takeAction(self, gamestate, actionSpace):
        state = np.array([gamestate], dtype=object) # convert gamestate to a numpy array for processing
        action = self.actor_model.predict(state) # predict the action using the actor model
        action = action[0] # extract the predicted action from the output array
        action = np.clip(action, -2, actionSpace[1]) # clip the predicted action to the valid range defined by actionSpace
        return action
    
        