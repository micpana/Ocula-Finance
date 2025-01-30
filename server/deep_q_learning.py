import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.preprocessing import StandardScaler
import random
from collections import deque

# Define the Q-Network (Neural Network for Q-value approximation)
class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)  # Output for Q-values (one for each action)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        q_values = self.fc3(x)  # Q-values for each action
        return q_values

# DQN Agent
class DQN:
    def __init__(self, input_dim, output_dim, lr=0.001, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01, batch_size=64, replay_buffer_size=10000):
        self.q_network = QNetwork(input_dim, output_dim)
        self.target_network = QNetwork(input_dim, output_dim)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.batch_size = batch_size
        self.replay_buffer = deque(maxlen=replay_buffer_size)
        
        # Initialize target network weights
        self.target_network.load_state_dict(self.q_network.state_dict())

    def get_action(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = self.q_network(state)
        if np.random.rand() < self.epsilon:
            # Explore: Random action
            action = np.random.randint(q_values.shape[1])
        else:
            # Exploit: Action with highest Q-value
            action = torch.argmax(q_values).item()
        return action

    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.append((state, action, reward, next_state, done))

    def update(self):
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # Sample random batch from replay buffer
        batch = random.sample(self.replay_buffer, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # Convert lists to tensors
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # Get Q-values for current states and next states
        q_values = self.q_network(states)
        next_q_values = self.target_network(next_states)

        # Get the Q-value of the action taken in each state
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        # Compute the target Q-values using the Bellman equation
        next_q_value = next_q_values.max(1)[0]
        target_q_value = rewards + (self.gamma * next_q_value * (1 - dones))

        # Compute the loss (Mean Squared Error)
        loss = nn.MSELoss()(q_value, target_q_value)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_network(self):
        # Update target network parameters
        self.target_network.load_state_dict(self.q_network.state_dict())

    def train(self, x_train, y_train, num_episodes=1000):
        for episode in range(num_episodes):
            state = x_train[0]  # Start with the first state
            total_reward = 0
            done = False

            for t in range(len(x_train) - 1):
                # Get action
                action = self.get_action(state)

                # Get reward (from your y_train) and next state
                reward = y_train[t]  # Reward is assumed to be your target
                next_state = x_train[t + 1]

                # Store the transition
                self.store_transition(state, action, reward, next_state, done)

                # Move to the next state
                state = next_state
                total_reward += reward

                # Update the Q-network
                self.update()

            # Decay epsilon
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

            # Update target network every few episodes
            if episode % 10 == 0:
                self.update_target_network()

            print(f"Episode {episode + 1}, Total Reward: {total_reward}, Epsilon: {self.epsilon}")

    def test(self, x_test):
        state = x_test[0]
        actions = []

        for t in range(len(x_test)):
            action = self.get_action(state)
            actions.append(action)
            state = x_test[t]  # Update state for next step

        return actions

# Example usage:

# Assume you have x_train, y_train, x_test, and y_test (replace with your actual data)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize DQN
input_dim = x_train.shape[1]
output_dim = 3  # Number of actions: Buy, Sell, Nothing
dqn = DQN(input_dim, output_dim)

# Train the DQN model
dqn.train(x_train, y_train)

# Test the DQN model
y_pred = dqn.test(x_test)

# Compare y_pred with y_test to calculate accuracy or other metrics
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")
