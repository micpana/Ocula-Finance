import numpy as np

class QLearningAgent:
    def __init__(self, num_states, num_actions, learning_rate=0.1, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.995, min_epsilon=0.01, num_episodes=1000):
        self.num_states = num_states
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.num_episodes = num_episodes
        
        # Initialize Q-table
        self.Q = np.zeros((self.num_states, self.num_actions))
    
    def discretize_state(self, state):
        # Convert the state to an integer index
        return hash(tuple(state)) % self.num_states
    
    def get_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            # Explore: choose random action
            action = np.random.randint(self.num_actions)
        else:
            # Exploit: choose action with max Q-value
            action = np.argmax(self.Q[state, :])
        return action
    
    def update_q_value(self, state, action, reward, next_state):
        # Q-value update based on the Bellman equation
        max_future_q = np.max(self.Q[next_state, :])
        current_q = self.Q[state, action]
        
        # Q-learning update rule
        self.Q[state, action] = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
    
    def decay_epsilon(self):
        # Decay epsilon to encourage exploitation as training progresses
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def train(self, x_train, y_train):
        for episode in range(self.num_episodes):
            state = self.discretize_state(x_train[0])  # Start with the first state
            total_reward = 0

            for i in range(len(x_train) - 1):
                action = self.get_action(state)

                # Get reward and next state
                reward = y_train[i]  # Reward is assumed to be the target value
                next_state = self.discretize_state(x_train[i + 1])

                # Update Q-value
                self.update_q_value(state, action, reward, next_state)

                # Move to next state
                state = next_state
                total_reward += reward

            # Decay epsilon after each episode
            self.decay_epsilon()

            print(f"Episode {episode + 1}, Total Reward: {total_reward}, Epsilon: {self.epsilon}")
    
    def test(self, x_test):
        y_pred = []
        state = self.discretize_state(x_test[0])

        for i in range(len(x_test)):
            action = np.argmax(self.Q[state, :])  # Always choose the best action (greedy)
            y_pred.append(action)
            
            if i < len(x_test) - 1:
                state = self.discretize_state(x_test[i + 1])  # Update state
        
        return np.array(y_pred)

# Example usage

import numpy as np
from sklearn.preprocessing import StandardScaler

# Example data (replace with your actual data)
# x_train, y_train = load_training_data()
# x_test, y_test = load_test_data()

# Normalize the data (optional but recommended)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Initialize the QLearning agent
num_states = 1248  # Number of features in your state representation
num_actions = 3  # Number of actions (Buy, Sell, Nothing)
agent = QLearningAgent(num_states, num_actions)

# Train the Q-learning model
agent.train(x_train, y_train)

# Test the model
y_pred = agent.test(x_test)

# Compare y_pred with y_test to calculate accuracy, etc.
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")
