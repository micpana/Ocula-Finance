import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.preprocessing import StandardScaler
from collections import deque
import random

# Define the neural network for the policy (actor) and value function (critic)
class ActorCriticNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ActorCriticNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.actor = nn.Linear(64, output_dim)  # Output for action probabilities
        self.critic = nn.Linear(64, 1)  # Output for value function

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        action_probs = torch.softmax(self.actor(x), dim=-1)  # Probability distribution over actions
        value = self.critic(x)  # Value of the state
        return action_probs, value

# Define PPO class
class PPO:
    def __init__(self, input_dim, output_dim, lr=0.001, gamma=0.99, epsilon=0.2, batch_size=64):
        self.model = ActorCriticNetwork(input_dim, output_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.memory = deque(maxlen=10000)  # Memory to store transitions
        self.mse_loss = nn.MSELoss()

    def get_action(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action_probs, _ = self.model(state)
        dist = torch.distributions.Categorical(action_probs)
        action = dist.sample()
        return action.item(), dist.log_prob(action)

    def store_transition(self, state, action, log_prob, reward, next_state, done):
        self.memory.append((state, action, log_prob, reward, next_state, done))

    def update(self):
        states, actions, log_probs, rewards, next_states, dones = zip(*self.memory)

        # Convert lists to tensors
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int32)
        old_log_probs = torch.tensor(log_probs, dtype=torch.float32)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # Get the value function and action probabilities for current and next states
        action_probs, values = self.model(states)
        _, next_values = self.model(next_states)

        # Compute advantages and targets
        advantages = rewards + self.gamma * next_values.squeeze() * (1 - dones) - values.squeeze()
        targets = advantages + values.squeeze()

        # Compute the ratio (for PPO clip objective)
        dist = torch.distributions.Categorical(action_probs)
        new_log_probs = dist.log_prob(actions)
        ratios = torch.exp(new_log_probs - old_log_probs)

        # Calculate surrogate loss (PPO objective)
        surr1 = ratios * advantages
        surr2 = torch.clamp(ratios, 1 - self.epsilon, 1 + self.epsilon) * advantages
        actor_loss = -torch.min(surr1, surr2).mean()

        # Calculate value loss (critic loss)
        critic_loss = self.mse_loss(values.squeeze(), targets)

        # Total loss
        loss = actor_loss + 0.5 * critic_loss

        # Update the network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Clear memory
        self.memory.clear()

    def train(self, x_train, y_train, num_episodes=1000):
        for episode in range(num_episodes):
            state = x_train[0]  # Start with the first state
            total_reward = 0
            done = False

            for t in range(len(x_train) - 1):
                # Get action and log probability
                action, log_prob = self.get_action(state)

                # Get reward (from your y_train) and next state
                reward = y_train[t]  # Reward is assumed to be your target
                next_state = x_train[t + 1]

                # Store the transition
                self.store_transition(state, action, log_prob, reward, next_state, done)

                # Move to the next state
                state = next_state
                total_reward += reward

                # Update model if batch is full
                if len(self.memory) >= self.batch_size:
                    self.update()

            print(f"Episode {episode + 1}, Total Reward: {total_reward}")

    def test(self, x_test):
        state = x_test[0]
        actions = []

        for t in range(len(x_test)):
            action, _ = self.get_action(state)
            actions.append(action)
            state = x_test[t]  # Update state for next step

        return actions

# Example usage:

# Assume you have x_train, y_train, x_test, and y_test (replace with your actual data)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize PPO
input_dim = x_train.shape[1]
output_dim = 3  # Number of actions: Buy, Sell, Nothing
ppo = PPO(input_dim, output_dim)

# Train the PPO model
ppo.train(x_train, y_train)

# Test the PPO model
y_pred = ppo.test(x_test)

# Compare y_pred with y_test to calculate accuracy or other metrics
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")
