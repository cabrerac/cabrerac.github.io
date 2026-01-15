(() => {
  const button = document.querySelector(".pyodide-example-button");
  const output = document.querySelector(".pyodide-example-output");

  if (!button) {
    return;
  }

  async function runExample() {
    if (output) {
      output.textContent = "Running example...";
    }

    const pyodide = await loadPyodide();
    await pyodide.loadPackage("numpy");
    await pyodide.loadPackage("matplotlib");

    const code = `
import numpy as np
import matplotlib.pyplot as plt

# Generate sample data
X = np.random.rand(100, 2)
y = np.array([1 if x[0] + x[1] > 1 else 0 for x in X])

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
plt.title("Sample ML Dataset")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
    `;

    await pyodide.runPythonAsync(code);

    if (output) {
      output.textContent = "Example executed.";
    }
  }

  button.addEventListener("click", () => {
    void runExample();
  });
})();
