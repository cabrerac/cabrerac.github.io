<!-- NOTEBOOK: -->

# Practical: Reinforcement Learning and Advanced Neural Architectures

In this practical session, we will build upon our previous work with neural networks and explore advanced architectures that have revolutionised machine learning. Each exercise is designed to deepen your understanding through hands-on implementation and detailed narrative explanations.

---

## Exercise 1: Exploring Advanced Neural Network Architectures

In this exercise, we will complement our previous lecture by investigating and experimenting with a range of neural network architectures that have driven recent advances in machine learning. We will focus on four key architectures:

- **Residual Networks (ResNet)**
- **Recurrent Neural Networks (RNN)**
- **Convolutional Neural Networks (CNN)**
- **Generative Adversarial Networks (GAN)**

For each architecture, we will provide a brief theoretical overview, followed by a step-by-step implementation and discussion of results.

### 1.1 Residual Networks (ResNet)

Residual Networks address the fundamental problem of vanishing gradients in deep networks by introducing shortcut connections, also known as skip connections. These connections allow the network to learn residual mappings, making it significantly easier to train very deep architectures.

**Theoretical Overview:**

A residual block can be expressed mathematically as:
$$
y = F(x, \\{W_i\\}) + x
$$

where \( F(x, \\{W_i\\}) \) is the residual mapping to be learned, and \( x \) is the input that gets added directly to the output.

**Implementation:**

Let's start by importing the necessary libraries and implementing a basic residual block:

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

Set random seeds for reproducibility:

```python
# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)
```

Now, let's create a function to build a residual block:

```python
def build_resnet_block(input_layer, units, activation='relu'):
    """
    Build a residual block with skip connections.
    
    Args:
        input_layer: Input tensor
        units: Number of units in the dense layers
        activation: Activation function to use
    
    Returns:
        Output tensor with residual connection
    """
    # Store the input for the skip connection
    shortcut = input_layer
    
    # First dense layer
    x = layers.Dense(units, activation=activation)(input_layer)
    
    # Second dense layer (no activation here)
    x = layers.Dense(units, activation=None)(x)
    
    # Add the skip connection (residual connection)
    x = layers.Add()([x, shortcut])
    
    # Apply activation after the addition
    x = layers.Activation(activation)(x)
    
    return x
```

In the code above, we define a simple residual block using Keras. The key innovation is the addition of the input (`shortcut`) to the output of the dense layers, which forms the skip connection. This allows gradients to flow more easily through the network during backpropagation, facilitating the training of deeper models.

Let's create a simple ResNet model and compare it with a traditional deep network:

```python
def create_resnet_model(input_shape, num_classes=2):
    """
    Create a ResNet model with multiple residual blocks.
    """
    inputs = layers.Input(shape=input_shape)
    
    # Initial dense layer
    x = layers.Dense(64, activation='relu')(inputs)
    
    # Add multiple residual blocks
    for _ in range(3):
        x = build_resnet_block(x, 64)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    return model
```

```python
def create_traditional_model(input_shape, num_classes=2):
    """
    Create a traditional deep network without residual connections.
    """
    inputs = layers.Input(shape=input_shape)
    
    x = layers.Dense(64, activation='relu')(inputs)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(64, activation='relu')(x)
    
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    return model
```

Here we create two models: a ResNet with residual connections and a traditional deep network without them. The ResNet model uses our `build_resnet_block` function to create multiple residual blocks, whilst the traditional model simply stacks dense layers.

Let's generate some data and train both models:

```python
# Generate synthetic data for demonstration
X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, 
                          n_clusters_per_class=1, n_redundant=0, 
                          random_state=42)
```

Split the data:

```python
# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42)

# Convert to one-hot encoding for multi-class classification
y_train_onehot = tf.keras.utils.to_categorical(y_train, 2)
y_test_onehot = tf.keras.utils.to_categorical(y_test, 2)

print(f"Training data shape: {X_train.shape}")
print(f"Test data shape: {X_test.shape}")
```

Now let's create and train both models:

```python
# Create models
resnet_model = create_resnet_model((10,))
traditional_model = create_traditional_model((10,))
```

Compile the models:

```python
# Compile models
resnet_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                     metrics=['accuracy'])
traditional_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                         metrics=['accuracy'])
```

Train the models:

```python
# Train models
print("Training ResNet model...")
resnet_history = resnet_model.fit(X_train, y_train_onehot, 
                                  validation_split=0.2, epochs=50, 
                                  batch_size=32, verbose=1)
```

```python
print("\nTraining Traditional model...")
traditional_history = traditional_model.fit(X_train, y_train_onehot, 
                                           validation_split=0.2, epochs=50, 
                                           batch_size=32, verbose=1)
```

We generate synthetic classification data and train both models using the same optimiser and loss function. The key difference is in the architecture: the ResNet uses residual connections, whilst the traditional model uses standard dense layers.

Let's compare the training curves:

```python
# Plot training comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Training accuracy
ax1.plot(resnet_history.history['accuracy'], label='ResNet', linewidth=2)
ax1.plot(traditional_history.history['accuracy'], label='Traditional', linewidth=2)
ax1.set_title('Training Accuracy Comparison')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Validation accuracy
ax2.plot(resnet_history.history['val_accuracy'], label='ResNet', linewidth=2)
ax2.plot(traditional_history.history['val_accuracy'], label='Traditional', linewidth=2)
ax2.set_title('Validation Accuracy Comparison')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

Evaluate final performance:

```python
# Evaluate final performance
resnet_test_acc = resnet_model.evaluate(X_test, y_test_onehot, verbose=0)[1]
traditional_test_acc = traditional_model.evaluate(X_test, y_test_onehot, verbose=0)[1]

print(f"ResNet Test Accuracy: {resnet_test_acc:.4f}")
print(f"Traditional Model Test Accuracy: {traditional_test_acc:.4f}")
```

The training curves reveal important insights about the benefits of residual connections. Typically, you'll observe that the ResNet model trains more smoothly and often achieves better final performance. The residual connections help maintain gradient flow, preventing the vanishing gradient problem that can occur in very deep networks.

### 1.2 Recurrent Neural Networks (RNN)

Recurrent Neural Networks are designed to process sequential data by maintaining an internal state (memory) that captures information about previous inputs. This makes them particularly suitable for tasks involving time series, text, and other sequential data.

**Theoretical Overview:**

The basic RNN cell computes:
$$
h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)
$$

where \( h_t \) is the hidden state at time \( t \), \( x_t \) is the input at time \( t \), and \( W \) and \( b \) are learnable parameters.

**Implementation:**

Let's create a simple RNN for sequence classification:

```python
def create_simple_rnn(input_shape, num_classes=2):
    """
    Create a simple RNN model for sequence classification.
    """
    inputs = layers.Input(shape=input_shape)
    
    # Simple RNN layer
    x = layers.SimpleRNN(64, return_sequences=True)(inputs)
    x = layers.SimpleRNN(32, return_sequences=False)(inputs)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    return model
```

```python
def create_lstm_model(input_shape, num_classes=2):
    """
    Create an LSTM model for sequence classification.
    """
    inputs = layers.Input(shape=input_shape)
    
    # LSTM layer
    x = layers.LSTM(64, return_sequences=True)(inputs)
    x = layers.LSTM(32, return_sequences=False)(inputs)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    return model
```

We create two types of recurrent networks: a simple RNN and an LSTM (Long Short-Term Memory) network. The simple RNN uses the basic recurrent cell, whilst LSTM includes additional gates (input, forget, and output gates) that help it better capture long-term dependencies.

Let's generate sequential data and train these models:

```python
# Generate sequential data
def generate_sequential_data(n_samples=1000, sequence_length=10, n_features=5):
    """
    Generate synthetic sequential data for RNN training.
    """
    X = np.random.randn(n_samples, sequence_length, n_features)
    
    # Create labels based on the sum of the first feature across the sequence
    y = (np.sum(X[:, :, 0], axis=1) > 0).astype(int)
    
    return X, y
```

Generate the data:

```python
# Generate data
X_seq, y_seq = generate_sequential_data()

# Split the data
X_seq_train, X_seq_test, y_seq_train, y_seq_test = train_test_split(
    X_seq, y_seq, test_size=0.2, random_state=42
)

# Convert to one-hot encoding
y_seq_train_onehot = tf.keras.utils.to_categorical(y_seq_train, 2)
y_seq_test_onehot = tf.keras.utils.to_categorical(y_seq_test, 2)

print(f"Sequential training data shape: {X_seq_train.shape}")
print(f"Sequential test data shape: {X_seq_test.shape}")
```

Now let's train both RNN models:

```python
# Create models
simple_rnn_model = create_simple_rnn((10, 5))
lstm_model = create_lstm_model((10, 5))
```

Compile the models:

```python
# Compile models
simple_rnn_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                        metrics=['accuracy'])
lstm_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                   metrics=['accuracy'])
```

Train the models:

```python
# Train models
print("Training Simple RNN model...")
simple_rnn_history = simple_rnn_model.fit(X_seq_train, y_seq_train_onehot, 
                                         validation_split=0.2, epochs=30, 
                                         batch_size=32, verbose=1)
```

```python
print("\nTraining LSTM model...")
lstm_history = lstm_model.fit(X_seq_train, y_seq_train_onehot, 
                             validation_split=0.2, epochs=30, 
                             batch_size=32, verbose=1)
```

We generate synthetic sequential data where the label depends on the cumulative sum of the first feature across the sequence. This creates a task that requires the model to remember information from earlier timesteps.

Let's compare the performance:

```python
# Plot training comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Training accuracy
ax1.plot(simple_rnn_history.history['accuracy'], label='Simple RNN', linewidth=2)
ax1.plot(lstm_history.history['accuracy'], label='LSTM', linewidth=2)
ax1.set_title('Training Accuracy Comparison')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Validation accuracy
ax2.plot(simple_rnn_history.history['val_accuracy'], label='Simple RNN', linewidth=2)
ax2.plot(lstm_history.history['val_accuracy'], label='LSTM', linewidth=2)
ax2.set_title('Validation Accuracy Comparison')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Accuracy')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

Evaluate final performance:

```python
# Evaluate final performance
simple_rnn_test_acc = simple_rnn_model.evaluate(X_seq_test, y_seq_test_onehot, verbose=0)[1]
lstm_test_acc = lstm_model.evaluate(X_seq_test, y_seq_test_onehot, verbose=0)[1]

print(f"Simple RNN Test Accuracy: {simple_rnn_test_acc:.4f}")
print(f"LSTM Test Accuracy: {lstm_test_acc:.4f}")
```

The comparison between simple RNN and LSTM typically shows that LSTM performs better, especially on tasks requiring long-term memory. This is because LSTM's gating mechanisms help it maintain information over longer sequences.

### 1.3 Convolutional Neural Networks (CNN)

Convolutional Neural Networks are designed to process grid-like data, such as images, by using convolutional layers that can capture spatial patterns and hierarchies of features.

**Theoretical Overview:**

A convolutional layer applies filters (kernels) to the input:
$$
(f * k)(p) = \sum_{s+t=p} f(s) k(t)
$$

where \( f \) is the input feature map, \( k \) is the kernel, and \( p \) is the position.

**Implementation:**

Let's create a CNN for image classification:

```python
def create_cnn_model(input_shape, num_classes=2):
    """
    Create a CNN model for image classification.
    """
    inputs = layers.Input(shape=input_shape)
    
    # First convolutional block
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    x = layers.MaxPooling2D((2, 2))(x)
    
    # Second convolutional block
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    
    # Third convolutional block
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = layers.MaxPooling2D((2, 2))(x)
    
    # Flatten and dense layers
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    
    # Output layer
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs, outputs)
    return model
```

We create a CNN with three convolutional blocks, each consisting of a convolutional layer followed by max pooling. The convolutional layers learn spatial features, whilst max pooling reduces spatial dimensions and provides some translation invariance.

Let's generate synthetic image data and train the CNN:

```python
# Generate synthetic image data
def generate_image_data(n_samples=1000, img_size=32):
    """
    Generate synthetic image data for CNN training.
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
# Generate data
X_img, y_img = generate_image_data()

# Split the data
X_img_train, X_img_test, y_img_train, y_img_test = train_test_split(
    X_img, y_img, test_size=0.2, random_state=42
)

# Convert to one-hot encoding
y_img_train_onehot = tf.keras.utils.to_categorical(y_img_train, 2)
y_img_test_onehot = tf.keras.utils.to_categorical(y_img_test, 2)

print(f"Image training data shape: {X_img_train.shape}")
print(f"Image test data shape: {X_img_test.shape}")
```

Let's visualise some of the generated images:

```python
# Visualise some examples
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

We generate synthetic image data with simple patterns: horizontal lines for class 0 and vertical lines for class 1. This creates a task where the CNN can learn to detect spatial patterns using its convolutional filters.

Now let's train the CNN:

```python
# Create and train CNN model
cnn_model = create_cnn_model((32, 32, 1))
cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                  metrics=['accuracy'])

print("Training CNN model...")
cnn_history = cnn_model.fit(X_img_train, y_img_train_onehot, 
                           validation_split=0.2, epochs=20, 
                           batch_size=32, verbose=1)
```

Evaluate performance:

```python
# Evaluate performance
cnn_test_acc = cnn_model.evaluate(X_img_test, y_img_test_onehot, verbose=0)[1]
print(f"CNN Test Accuracy: {cnn_test_acc:.4f}")
```

Plot training curves:

```python
# Plot training curves
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(cnn_history.history['accuracy'], label='Training', linewidth=2)
plt.plot(cnn_history.history['val_accuracy'], label='Validation', linewidth=2)
plt.title('CNN Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(cnn_history.history['loss'], label='Training', linewidth=2)
plt.plot(cnn_history.history['val_loss'], label='Validation', linewidth=2)
plt.title('CNN Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

The CNN training curves typically show good convergence, as the model learns to detect the spatial patterns in our synthetic images. The convolutional layers are particularly effective at capturing local spatial relationships.

### 1.4 Generative Adversarial Networks (GAN)

Generative Adversarial Networks consist of two competing networks: a generator that creates fake data and a discriminator that tries to distinguish between real and fake data.

**Theoretical Overview:**

The GAN objective function is:
$$
\min_G \max_D V(D,G) = \mathbb{E}_{x \sim p_{data}(x)}[\log D(x)] + \mathbb{E}_{z \sim p_z(z)}[\log(1-D(G(z)))]
$$

where \( G \) is the generator, \( D \) is the discriminator, and \( z \) is random noise.

**Implementation:**

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

The GAN training process involves alternating between training the discriminator and the generator. The discriminator is trained on both real and fake data to improve its classification ability, whilst the generator is trained to fool the discriminator.

Let's visualise the training progress and generated samples:

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

The training loss plot shows the adversarial dynamics between the generator and discriminator. The generated samples demonstrate the GAN's ability to create synthetic data that resembles the training distribution.

---

## Summary of Exercise 1

In this exercise, we have explored four fundamental neural network architectures:

1. **Residual Networks (ResNet):** We implemented residual connections that help train very deep networks by allowing gradients to flow more easily.

2. **Recurrent Neural Networks (RNN):** We compared simple RNNs with LSTM networks, demonstrating how LSTM's gating mechanisms help capture long-term dependencies.

3. **Convolutional Neural Networks (CNN):** We built a CNN that can detect spatial patterns in image data, showing how convolutional layers learn hierarchical features.

4. **Generative Adversarial Networks (GAN):** We implemented a GAN with competing generator and discriminator networks, demonstrating how adversarial training can generate realistic synthetic data.

Each architecture has specific strengths and applications, providing a solid foundation for more advanced deep learning applications.

<!-- end NOTEBOOK: --> 