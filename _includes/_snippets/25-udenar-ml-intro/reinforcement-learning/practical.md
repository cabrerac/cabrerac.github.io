<!-- NOTEBOOK: -->

# Practical Introduction

In this practical session, we will build upon our previous work with neural networks and explore GANs architectures. Then, we will focus on the reinforcement learning algorithms we explored in our last lecture.

---

## Exercise 1: Exploring Generative Adversarial Networks (GANs)

Generative Adversarial Networks consist of two competing networks: a generator that creates fake data and a discriminator that tries to distinguish between real and fake data.

First, we need to import the relevant libraries:

```python
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
```

And define a dataset to play with:

```python
# Generate synthetic image data
def generate_image_data(n_samples=1000, img_size=32):
    """
    Generate synthetic image data for GAN training.
    """
    X = np.random.randn(n_samples, img_size, img_size, 1)
    
    # Create patterns that can be detected by convolutions
    for i in range(n_samples):
        if i % 2 == 0:
            # Add horizontal lines for class 0
            X[i, :, img_size//2-2:img_size//2+2, 0] += 2
        else:
            # Add vertical lines for class 1
            X[i, img_size//2-2:img_size//2+2, :, 0] += 2
    # Create labels
    y = (np.arange(n_samples) % 2).astype(int)   
    return X, y
```

Generate the data:

```python
X_img, y_img = generate_image_data()
# Split the data
X_img_train, X_img_test, y_img_train, y_img_test = train_test_split(
    X_img, y_img, test_size=0.2, random_state=42)
# Convert to one-hot encoding
y_img_train_onehot = tf.keras.utils.to_categorical(y_img_train, 2)
y_img_test_onehot = tf.keras.utils.to_categorical(y_img_test, 2)
print(f"Image training data shape: {X_img_train.shape}")
print(f"Image test data shape: {X_img_test.shape}")
```
     
Let's visualise some of the generated images:

```python
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
for i in range(8):
    row = i // 4
    col = i % 4
    axes[row, col].imshow(X_img[i, :, :, 0], cmap='gray')
    axes[row, col].set_title(f'Class {y_img[i]}')
    axes[row, col].axis('off')
plt.tight_layout()
plt.show()
```

Let's create a simple GAN for generating synthetic data:

```python
def create_generator(latent_dim, output_shape):
    """
    Create a generator network.
    """
    inputs = layers.Input(shape=(latent_dim,))
    
    x = layers.Dense(128, activation='relu')(inputs)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(np.prod(output_shape), activation='tanh')(x)
    x = layers.Reshape(output_shape)(x)
    
    return models.Model(inputs, x, name='generator')
```

```python
def create_discriminator(input_shape):
    """
    Create a discriminator network.
    """
    inputs = layers.Input(shape=input_shape)
    
    x = layers.Flatten()(inputs)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(1, activation='sigmoid')(x)
    
    return models.Model(inputs, x, name='discriminator')
```

```python
def create_gan(generator, discriminator):
    """
    Create a GAN by combining generator and discriminator.
    """
    # Freeze discriminator during GAN training
    discriminator.trainable = False
    
    gan_input = layers.Input(shape=(generator.input_shape[1],))
    gan_output = discriminator(generator(gan_input))
    
    gan = models.Model(gan_input, gan_output, name='gan')
    
    # Unfreeze discriminator for separate training
    discriminator.trainable = True
    
    return gan
```

We create three components: a generator that transforms random noise into synthetic data, a discriminator that classifies data as real or fake, and a GAN that combines them for adversarial training.

Let's train the GAN on our synthetic data:

```python
# Prepare data for GAN training
X_gan = X_img_train  # Use the image data we generated earlier
X_gan = (X_gan - X_gan.min()) / (X_gan.max() - X_gan.min()) * 2 - 1  # Normalise to [-1, 1]
# Create models
latent_dim = 100
generator = create_generator(latent_dim, (32, 32, 1))
discriminator = create_discriminator((32, 32, 1))
gan = create_gan(generator, discriminator)
```

Compile the models:

```python
# Compile models
discriminator.compile(optimizer='adam', loss='binary_crossentropy', 
                     metrics=['accuracy'])
gan.compile(optimizer='adam', loss='binary_crossentropy')
```

Create training function:

```python
# Training function
def train_gan(generator, discriminator, gan, real_data, epochs=100, batch_size=32):
    """
    Train the GAN model.
    """
    d_losses = []
    g_losses = []
    
    for epoch in range(epochs):
        # Train discriminator
        idx = np.random.randint(0, real_data.shape[0], batch_size)
        real_batch = real_data[idx]
        
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        fake_batch = generator.predict(noise)
        
        d_loss_real = discriminator.train_on_batch(real_batch, np.ones((batch_size, 1)))
        d_loss_fake = discriminator.train_on_batch(fake_batch, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        # Train generator
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        g_loss = gan.train_on_batch(noise, np.ones((batch_size, 1)))
        
        d_losses.append(d_loss[0])
        g_losses.append(g_loss)
        
        if epoch % 20 == 0:
            print(f"Epoch {epoch}, D Loss: {d_loss[0]:.4f}, G Loss: {g_loss:.4f}")
    
    return d_losses, g_losses
```

Train the GAN:

```python
# Train the GAN
print("Training GAN...")
d_losses, g_losses = train_gan(generator, discriminator, gan, X_gan, epochs=100)
```

Let's compare the models behaviour:

```python
# Plot training losses
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(d_losses, label='Discriminator Loss', linewidth=2)
plt.plot(g_losses, label='Generator Loss', linewidth=2)
plt.title('GAN Training Losses')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)
```

The GAN training process involves alternating between training the discriminator and the generator. The discriminator is trained on both real and fake data to improve its classification ability, whilst the generator is trained to fool the discriminator.

Generate and visualise synthetic samples:

```python
# Generate and visualise synthetic samples
plt.subplot(1, 2, 2)
noise = np.random.normal(0, 1, (8, latent_dim))
generated_images = generator.predict(noise)
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(generated_images[i, :, :, 0], cmap='gray')
    plt.title(f'Generated {i+1}')
    plt.axis('off')
plt.tight_layout()
plt.show()
print("GAN training completed! Generated samples are shown above.")
```

The training loss plot shows the adversarial dynamics between the generator and discriminator. The generated samples show that the generator is not able to fool the discriminator.

---

## Exercise 2: Policy Iteration Algorithm

In this exercise, we will implement the Policy Iteration algorithm, which is a fundamental dynamic programming method for solving Markov Decision Processes (MDPs). Policy Iteration alternates between policy evaluation and policy improvement until convergence to an optimal policy.

**Theoretical Overview:**

Policy Iteration consists of two main steps:
1. **Policy Evaluation:** Compute the value function for the current policy
2. **Policy Improvement:** Update the policy to be greedy with respect to the current value function

The algorithm iterates between these steps until the policy stabilizes.

**Implementation:**

Let's start by creating a simple grid world environment and implementing Policy Iteration:

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, List, Dict
import random
```

First, let's create a simple grid world environment:

```python
class GridWorld:
    """
    A simple grid world environment for reinforcement learning.
    """
    def __init__(self, size=4, goal_reward=1, step_reward=-0.01, obstacle_reward=-1):
        self.size = size
        self.goal_reward = goal_reward
        self.step_reward = step_reward
        self.obstacle_reward = obstacle_reward
        
        # Define the grid
        self.grid = np.zeros((size, size))
        self.goal = (size-1, size-1)  # Bottom-right corner
        self.obstacles = [(1, 1), (2, 2)]  # Some obstacles
        
        # Mark goal and obstacles
        self.grid[self.goal] = 2  # Goal
        for obs in self.obstacles:
            self.grid[obs] = 1  # Obstacle
        
        # Actions: up, right, down, left
        self.actions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.action_names = ['Up', 'Right', 'Down', 'Left']
        
        # Current state
        self.current_state = (0, 0)
        
    def reset(self):
        """Reset the environment to initial state."""
        self.current_state = (0, 0)
        return self.current_state
    
    def step(self, action):
        """Take a step in the environment."""
        # Get action direction
        action_dir = self.actions[action]
        
        # Calculate new state
        new_state = (
            max(0, min(self.size-1, self.current_state[0] + action_dir[0])),
            max(0, min(self.size-1, self.current_state[1] + action_dir[1]))
        )
        
        # Check if new state is an obstacle
        if new_state in self.obstacles:
            new_state = self.current_state  # Stay in place
            reward = self.obstacle_reward
        elif new_state == self.goal:
            reward = self.goal_reward
        else:
            reward = self.step_reward
        
        self.current_state = new_state
        done = (new_state == self.goal)
        
        return new_state, reward, done
    
    def get_transition_probabilities(self, state, action):
        """Get transition probabilities for a state-action pair."""
        action_dir = self.actions[action]
        next_state = (
            max(0, min(self.size-1, state[0] + action_dir[0])),
            max(0, min(self.size-1, state[1] + action_dir[1]))
        )
        
        # Check if next state is an obstacle
        if next_state in self.obstacles:
            next_state = state  # Stay in place
        
        return [(1.0, next_state)]
    
    def get_reward(self, state, action, next_state):
        """Get reward for a state-action-next_state transition."""
        if next_state in self.obstacles:
            return self.obstacle_reward
        elif next_state == self.goal:
            return self.goal_reward
        else:
            return self.step_reward
```

Now let's implement the Policy Iteration algorithm:

```python
class PolicyIteration:
    """
    Implementation of Policy Iteration algorithm.
    """
    def __init__(self, env, gamma=0.9, theta=1e-6):
        self.env = env
        self.gamma = gamma  # Discount factor
        self.theta = theta  # Convergence threshold
        
        # Initialize value function and policy
        self.V = np.zeros((env.size, env.size))
        self.policy = np.zeros((env.size, env.size), dtype=int)
        
    def policy_evaluation(self):
        """Evaluate the current policy."""
        while True:
            delta = 0
            for i in range(self.env.size):
                for j in range(self.env.size):
                    state = (i, j)
                    
                    # Skip goal state
                    if state == self.env.goal:
                        continue
                    
                    # Skip obstacle states
                    if state in self.env.obstacles:
                        continue
                    
                    v = self.V[i, j]
                    
                    # Calculate new value based on current policy
                    action = self.policy[i, j]
                    new_v = 0
                    
                    # Get transition probabilities
                    transitions = self.env.get_transition_probabilities(state, action)
                    for prob, next_state in transitions:
                        reward = self.env.get_reward(state, action, next_state)
                        new_v += prob * (reward + self.gamma * self.V[next_state])
                    
                    self.V[i, j] = new_v
                    delta = max(delta, abs(v - new_v))
            
            if delta < self.theta:
                break
    
    def policy_improvement(self):
        """Improve the policy based on current value function."""
        policy_stable = True
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                state = (i, j)
                
                # Skip goal state
                if state == self.env.goal:
                    continue
                
                # Skip obstacle states
                if state in self.env.obstacles:
                    continue
                
                old_action = self.policy[i, j]
                
                # Find best action
                best_value = float('-inf')
                best_action = old_action
                
                for action in range(len(self.env.actions)):
                    value = 0
                    transitions = self.env.get_transition_probabilities(state, action)
                    
                    for prob, next_state in transitions:
                        reward = self.env.get_reward(state, action, next_state)
                        value += prob * (reward + self.gamma * self.V[next_state])
                    
                    if value > best_value:
                        best_value = value
                        best_action = action
                
                self.policy[i, j] = best_action
                
                if old_action != best_action:
                    policy_stable = False
        
        return policy_stable
    
    def solve(self, max_iterations=100):
        """Solve the MDP using Policy Iteration."""
        for iteration in range(max_iterations):
            print(f"Iteration {iteration + 1}")
            
            # Policy evaluation
            self.policy_evaluation()
            
            # Policy improvement
            policy_stable = self.policy_improvement()
            
            if policy_stable:
                print(f"Policy converged after {iteration + 1} iterations")
                break
        return self.V, self.policy
```

Let's create and solve a grid world problem:

```python
# Create environment and solver
env = GridWorld(size=4)
solver = PolicyIteration(env)
# Solve the MDP
V, policy = solver.solve()
```

Now let's visualize the results:

```python
def plot_results(env, V, policy):
    """Plot the value function and policy."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot value function
    im1 = ax1.imshow(V, cmap='viridis', interpolation='nearest')
    ax1.set_title('Value Function')
    ax1.set_xlabel('Column')
    ax1.set_ylabel('Row')
    
    # Add text annotations for value function
    for i in range(env.size):
        for j in range(env.size):
            if (i, j) == env.goal:
                ax1.text(j, i, 'G', ha='center', va='center', fontsize=12, fontweight='bold')
            elif (i, j) in env.obstacles:
                ax1.text(j, i, 'X', ha='center', va='center', fontsize=12, fontweight='bold')
            else:
                ax1.text(j, i, f'{V[i, j]:.2f}', ha='center', va='center', fontsize=10)
    
    plt.colorbar(im1, ax=ax1)
    
    # Plot policy
    policy_arrows = ['↑', '→', '↓', '←']
    policy_display = np.full((env.size, env.size), '', dtype=object)
    
    for i in range(env.size):
        for j in range(env.size):
            if (i, j) == env.goal:
                policy_display[i, j] = 'G'
            elif (i, j) in env.obstacles:
                policy_display[i, j] = 'X'
            else:
                policy_display[i, j] = policy_arrows[policy[i, j]]
    
    im2 = ax2.imshow(np.zeros_like(V), cmap='gray', alpha=0.3)
    ax2.set_title('Optimal Policy')
    ax2.set_xlabel('Column')
    ax2.set_ylabel('Row')
    
    # Add text annotations for policy
    for i in range(env.size):
        for j in range(env.size):
            ax2.text(j, i, policy_display[i, j], ha='center', va='center', 
                    fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.show()
# Plot the results
plot_results(env, V, policy)
```

Let's also test the learned policy:

```python
def test_policy(env, policy, num_episodes=5):
    """Test the learned policy."""
    total_rewards = []
    
    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        steps = 0
        max_steps = 100
        
        while steps < max_steps:
            action = policy[state]
            state, reward, done = env.step(action)
            total_reward += reward
            steps += 1
            
            if done:
                break
        
        total_rewards.append(total_reward)
        print(f"Episode {episode + 1}: Total reward = {total_reward:.2f}, Steps = {steps}")
    
    print(f"Average reward: {np.mean(total_rewards):.2f}")
    return total_rewards
# Test the learned policy
rewards = test_policy(env, policy)
```

The Policy Iteration algorithm successfully finds the optimal policy for navigating the grid world. The value function shows the expected future rewards from each state, and the policy arrows indicate the optimal action to take from each position.

---

## Exercise 3: Q-Learning Algorithm

In this exercise, we will implement Q-Learning, a model-free reinforcement learning algorithm that learns the optimal action-value function through experience. Q-Learning is particularly useful when we don't have a model of the environment.

**Theoretical Overview:**

Q-Learning updates the Q-values using the following update rule:
$$
Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]
$$

where:
- $Q(s, a)$ is the current Q-value for state $s$ and action $a$
- $\alpha$ is the learning rate
- $r$ is the immediate reward
- $\gamma$ is the discount factor
- $s'$ is the next state
- $\max_{a'} Q(s', a')$ is the maximum Q-value for the next state

**Implementation:**

Let's implement Q-Learning for the same grid world environment:

```python
class QLearning:
    """
    Implementation of Q-Learning algorithm.
    """
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995, epsilon_min=0.01):
        self.env = env
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # Initialize Q-table
        self.Q = {}
        self.initialize_q_table()
        
        # Training history
        self.episode_rewards = []
        self.episode_lengths = []
    
    def initialize_q_table(self):
        """Initialize the Q-table with zeros."""
        for i in range(self.env.size):
            for j in range(self.env.size):
                state = (i, j)
                if state not in self.env.obstacles and state != self.env.goal:
                    self.Q[state] = {}
                    for action in range(len(self.env.actions)):
                        self.Q[state][action] = 0.0
    
    def get_action(self, state):
        """Choose action using epsilon-greedy policy."""
        if state in self.env.obstacles or state == self.env.goal:
            return 0  # Default action for terminal states
        
        if np.random.random() < self.epsilon:
            # Exploration: random action
            return np.random.randint(0, len(self.env.actions))
        else:
            # Exploitation: best action
            return max(self.Q[state], key=self.Q[state].get)
    
    def update_q_value(self, state, action, reward, next_state):
        """Update Q-value using Q-Learning update rule."""
        if state in self.env.obstacles or state == self.env.goal:
            return
        
        # Current Q-value
        current_q = self.Q[state][action]
        
        # Maximum Q-value for next state
        if next_state in self.env.obstacles or next_state == self.env.goal:
            max_next_q = 0
        else:
            max_next_q = max(self.Q[next_state].values())
        
        # Q-Learning update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.Q[state][action] = new_q
    
    def train(self, num_episodes=1000, max_steps_per_episode=100):
        """Train the Q-Learning agent."""
        for episode in range(num_episodes):
            state = self.env.reset()
            total_reward = 0
            steps = 0
            
            while steps < max_steps_per_episode:
                # Choose action
                action = self.get_action(state)
                
                # Take action
                next_state, reward, done = self.env.step(action)
                
                # Update Q-value
                self.update_q_value(state, action, reward, next_state)
                
                state = next_state
                total_reward += reward
                steps += 1
                
                if done:
                    break
            
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
            # Record episode statistics
            self.episode_rewards.append(total_reward)
            self.episode_lengths.append(steps)
            
            if episode % 100 == 0:
                avg_reward = np.mean(self.episode_rewards[-100:])
                print(f"Episode {episode}: Average reward = {avg_reward:.2f}, Epsilon = {self.epsilon:.3f}")
    
    def get_policy(self):
        """Extract policy from Q-table."""
        policy = np.zeros((self.env.size, self.env.size), dtype=int)
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                state = (i, j)
                if state in self.env.obstacles:
                    policy[i, j] = 0  # Default for obstacles
                elif state == self.env.goal:
                    policy[i, j] = 0  # Default for goal
                else:
                    # Choose best action
                    policy[i, j] = max(self.Q[state], key=self.Q[state].get)
        
        return policy
    
    def get_value_function(self):
        """Extract value function from Q-table."""
        V = np.zeros((self.env.size, self.env.size))
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                state = (i, j)
                if state in self.env.obstacles:
                    V[i, j] = 0  # Default for obstacles
                elif state == self.env.goal:
                    V[i, j] = 0  # Default for goal
                else:
                    # Maximum Q-value for the state
                    V[i, j] = max(self.Q[state].values())
        return V
```

Now let's train the Q-Learning agent:

```python
# Create Q-Learning agent
q_agent = QLearning(env, alpha=0.1, gamma=0.9, epsilon=0.1)
# Train the agent
print("Training Q-Learning agent...")
q_agent.train(num_episodes=1000, max_steps_per_episode=100)
```

Let's visualize the training progress:

```python
# Plot training progress
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
# Plot episode rewards
ax1.plot(q_agent.episode_rewards)
ax1.set_title('Episode Rewards')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward')
ax1.grid(True, alpha=0.3)
# Plot moving average of rewards
window_size = 50
if len(q_agent.episode_rewards) >= window_size:
    moving_avg = np.convolve(q_agent.episode_rewards, 
                            np.ones(window_size)/window_size, mode='valid')
    ax1.plot(range(window_size-1, len(q_agent.episode_rewards)), moving_avg, 
             'r-', linewidth=2, label=f'Moving Average (window={window_size})')
    ax1.legend()
# Plot episode lengths
ax2.plot(q_agent.episode_lengths)
ax2.set_title('Episode Lengths')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

Now let's extract and visualize the learned policy and value function:

```python
# Extract learned policy and value function
q_policy = q_agent.get_policy()
q_value = q_agent.get_value_function()
# Plot results
plot_results(env, q_value, q_policy)
```

Let's test the learned policy:

```python
# Test the learned policy
print("Testing Q-Learning policy:")
q_rewards = test_policy(env, q_policy)
```

Let's also compare the Q-Learning results with Policy Iteration:

```python
# Compare results
print("\nComparison of Policy Iteration vs Q-Learning:")
print(f"Policy Iteration - Average reward: {np.mean(rewards):.2f}")
print(f"Q-Learning - Average reward: {np.mean(q_rewards):.2f}")
# Compare value functions
print(f"\nValue function difference (max): {np.max(np.abs(V - q_value)):.4f}")
print(f"Policy agreement: {np.sum(policy == q_policy)}/{policy.size} states")
```

Q-Learning successfully learns a near-optimal policy through experience, without requiring a model of the environment. The training curves show how the agent improves over time, and the final policy closely matches the optimal policy found by Policy Iteration.

---

## Exercise 4: Deep Q-Network (DQN) Algorithm

In this exercise, we will implement Deep Q-Network (DQN), which extends Q-Learning to use neural networks for approximating Q-values. This allows DQN to handle high-dimensional state spaces and continuous environments.

**Theoretical Overview:**

DQN combines Q-Learning with deep neural networks and introduces several key innovations:
1. **Experience Replay:** Stores transitions in a replay buffer and samples from it for training
2. **Target Network:** Uses a separate network for computing target Q-values to stabilize training
3. **Neural Network Approximation:** Uses a neural network to approximate Q-values instead of a Q-table

The loss function is:
$$
L(\theta) = \mathbb{E}_{(s,a,r,s') \sim D}[(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta))^2]
$$

where $\theta$ are the main network parameters and $\theta^-$ are the target network parameters.

**Implementation:**

Let's import the required libraries.

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import collections
import random
```

Let's implement DQN using TensorFlow/Keras:

```python
class DQNAgent:
    """
    Implementation of Deep Q-Network (DQN) agent.
    """
    def __init__(self, state_size, action_size, learning_rate=0.001, gamma=0.95, 
                 epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01, 
                 memory_size=10000, batch_size=32):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.memory_size = memory_size
        self.batch_size = batch_size
        
        # Experience replay buffer
        self.memory = collections.deque(maxlen=memory_size)
        
        # Neural networks
        self.q_network = self._build_model()
        self.target_network = self._build_model()
        self.update_target_network()
        
        # Training history
        self.episode_rewards = []
        self.episode_lengths = []
        self.losses = []
    
    def _build_model(self):
        """Build the neural network model."""
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(self.state_size,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
                     loss='mse')
        return model
    
    def update_target_network(self):
        """Update target network weights."""
        self.target_network.set_weights(self.q_network.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Choose action using epsilon-greedy policy."""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = np.reshape(state, [1, self.state_size])
        q_values = self.q_network.predict(state, verbose=0)
        return np.argmax(q_values[0])
    
    def replay(self):
        """Train the neural network on a batch of experiences."""
        if len(self.memory) < self.batch_size:
            return
        
        # Sample batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states = np.array([experience[0] for experience in batch])
        actions = np.array([experience[1] for experience in batch])
        rewards = np.array([experience[2] for experience in batch])
        next_states = np.array([experience[3] for experience in batch])
        dones = np.array([experience[4] for experience in batch])
        
        # Current Q-values
        current_q_values = self.q_network.predict(states, verbose=0)
        
        # Target Q-values
        target_q_values = self.target_network.predict(next_states, verbose=0)
        
        # Update Q-values
        for i in range(self.batch_size):
            if dones[i]:
                target_q_values[i][actions[i]] = rewards[i]
            else:
                target_q_values[i][actions[i]] = rewards[i] + self.gamma * np.max(target_q_values[i])
        
        # Train the network
        history = self.q_network.fit(states, target_q_values, epochs=1, verbose=0)
        self.losses.append(history.history['loss'][0])
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def train(self, env, num_episodes=500, max_steps_per_episode=100, target_update_freq=10):
        """Train the DQN agent."""
        for episode in range(num_episodes):
            state = env.reset()
            total_reward = 0
            steps = 0
            
            # Convert state to feature vector
            state_features = self._state_to_features(state)
            
            while steps < max_steps_per_episode:
                # Choose action
                action = self.act(state_features)
                
                # Take action
                next_state, reward, done = env.step(action)
                next_state_features = self._state_to_features(next_state)
                
                # Store experience
                self.remember(state_features, action, reward, next_state_features, done)
                
                # Train the network
                self.replay()
                
                state = next_state
                state_features = next_state_features
                total_reward += reward
                steps += 1
                
                if done:
                    break
            
            # Update target network periodically
            if episode % target_update_freq == 0:
                self.update_target_network()
            
            # Record episode statistics
            self.episode_rewards.append(total_reward)
            self.episode_lengths.append(steps)
            
            if episode % 50 == 0:
                avg_reward = np.mean(self.episode_rewards[-50:])
                print(f"Episode {episode}: Average reward = {avg_reward:.2f}, Epsilon = {self.epsilon:.3f}")
    
    def _state_to_features(self, state):
        """Convert state to feature vector."""
        # For grid world, we can use one-hot encoding of position
        features = np.zeros(self.state_size)
        idx = state[0] * self.env.size + state[1]
        features[idx] = 1
        return features
    
    def get_policy(self):
        """Extract policy from trained network."""
        policy = np.zeros((self.env.size, self.env.size), dtype=int)
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                state = (i, j)
                if state in self.env.obstacles:
                    policy[i, j] = 0
                elif state == self.env.goal:
                    policy[i, j] = 0
                else:
                    state_features = self._state_to_features(state)
                    q_values = self.q_network.predict(np.array([state_features]), verbose=0)
                    policy[i, j] = np.argmax(q_values[0])
        return policy
```

Let's create a modified environment for DQN and train the agent:

```python
# Create environment and DQN agent
env_dqn = GridWorld(size=4)
state_size = env_dqn.size * env_dqn.size  # One-hot encoding of position
action_size = len(env_dqn.actions)
dqn_agent = DQNAgent(state_size, action_size, learning_rate=0.001, gamma=0.95,
                     epsilon=1.0, epsilon_decay=0.9999, epsilon_min=0.01,
                     memory_size=10000, batch_size=32)
# Set environment reference for feature conversion
dqn_agent.env = env_dqn
# Train the DQN agent
print("Training DQN agent...")
dqn_agent.train(env_dqn, num_episodes=1000, max_steps_per_episode=100)
```

Let's visualize the training progress:

```python
# Plot DQN training progress
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
# Plot episode rewards
ax1.plot(dqn_agent.episode_rewards)
ax1.set_title('DQN Episode Rewards')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Total Reward')
ax1.grid(True, alpha=0.3)
# Plot moving average of rewards
window_size = 25
if len(dqn_agent.episode_rewards) >= window_size:
    moving_avg = np.convolve(dqn_agent.episode_rewards, 
                            np.ones(window_size)/window_size, mode='valid')
    ax1.plot(range(window_size-1, len(dqn_agent.episode_rewards)), moving_avg, 
             'r-', linewidth=2, label=f'Moving Average (window={window_size})')
    ax1.legend()
# Plot episode lengths
ax2.plot(dqn_agent.episode_lengths)
ax2.set_title('DQN Episode Lengths')
ax2.set_xlabel('Episode')
ax2.set_ylabel('Steps')
ax2.grid(True, alpha=0.3)
# Plot training losses
if dqn_agent.losses:
    ax3.plot(dqn_agent.losses)
    ax3.set_title('DQN Training Loss')
    ax3.set_xlabel('Training Step')
    ax3.set_ylabel('Loss')
    ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

Now let's extract and test the learned policy:

```python
# Extract learned policy
dqn_policy = dqn_agent.get_policy()
# Test the learned policy
print("Testing DQN policy:")
dqn_rewards = test_policy(env_dqn, dqn_policy)
```

Let's compare all three algorithms:

```python
# Compare all algorithms
print("\nComparison of all algorithms:")
print(f"Policy Iteration - Average reward: {np.mean(rewards):.2f}")
print(f"Q-Learning - Average reward: {np.mean(q_rewards):.2f}")
print(f"DQN - Average reward: {np.mean(dqn_rewards):.2f}")
# Compare policies
print(f"\nPolicy agreement (PI vs QL): {np.sum(policy == q_policy)}/{policy.size} states")
print(f"Policy agreement (PI vs DQN): {np.sum(policy == dqn_policy)}/{policy.size} states")
print(f"Policy agreement (QL vs DQN): {np.sum(q_policy == dqn_policy)}/{policy.size} states")
```

DQN successfully learns to solve the grid world problem using neural network approximation. While it may not achieve exactly the same performance as the tabular methods for this simple environment, it demonstrates the framework that can be extended to more complex, high-dimensional problems.

---

## Homework - Reinforcement Learning Algorithm Implementation

The homework assignment focuses on implementing and comparing different reinforcement learning algorithms for a specific problem. You will apply the concepts learned in this practical session to create effective RL solutions for an environment of your preference. Explore the environments in the Gymnasium platform: https://gymnasium.farama.org/

### Assignment Tasks

1. **Environment Setup and Analysis**
   - Set up the environment
   - Analyze the state and action spaces
   - Visualize the environment dynamics

2. **Algorithm Implementation**
   - Implement **Q-Learning** for the Taxi environment
   - Experiment with different learning rates, discount factors, and exploration strategies
   - Analyze the impact of hyperparameters on learning performance

3. **Performance Analysis**
   - Analyze the impact of hyperparameters on learning performance
   - Compare training curves (episode rewards, episode lengths)
   - Evaluate final performance on test episodes
   - Discuss the trade-offs between exploration and exploitation


### Submission Guidelines

- Submit your solution as a Jupyter notebook with the following name format: `reinforcement_learning_session_8_<email_username>.ipynb`
- Include clear comments explaining your code and design decisions
- Provide comprehensive analysis of your results
- Document any challenges faced and how you overcame them
- Include visualisations and comparisons of your results and model performance
- Due date: 10/07/2025

<DESCRIBE YOUR SOLUTION HERE>

```python
# Write your implementation here
```

<!-- end NOTEBOOK: --> 