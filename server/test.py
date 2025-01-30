import numpy as np
from sklearn.preprocessing import StandardScaler
from q_learning import q_learning, test_model  # Import the Q-learning functions
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
np.random.seed(42)

# Generate dummy data
num_samples = 1000  # Total number of samples
num_features = 1248  # Number of features

# Generate random features (normal distribution)
x_data = np.random.randn(num_samples, num_features)

# Generate random labels (0: Nothing, 1: Buy, 2: Sell)
y_data = np.random.randint(0, 3, size=num_samples)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=42)

# Print shapes of the datasets
print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)
print("x_test shape:", x_test.shape)
print("y_test shape:", y_test.shape)

# Normalize the data (optional but recommended)
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# Train the Q-learning model
Q = q_learning(x_train, y_train)

# Test the model
y_pred = test_model(x_test, Q)

# Compare y_pred with y_test to calculate accuracy, etc.
accuracy = np.mean(y_pred == y_test)
print(f"Accuracy: {accuracy * 100:.2f}%")