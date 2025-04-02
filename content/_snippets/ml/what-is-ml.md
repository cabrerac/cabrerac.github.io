# What is Machine Learning?

Machine Learning is a field of study that gives computers the ability to learn without being explicitly programmed. It's a subset of Artificial Intelligence that focuses on building systems that can learn from and make decisions based on data.

![ML Overview](/assets/media/images/ml-overview.png)

## Key Characteristics
- Data-driven approach
- Pattern recognition
- Statistical methods
- Iterative learning

<video width="100%" controls>
  <source src="/assets/media/videos/ml-intro.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Interactive Example
Here's a simple example of how ML works:

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate sample data
X, y = make_blobs(n_samples=100, centers=2, random_state=42)

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Sample ML Dataset")
plt.show()
``` 