<!-- SLIDES: -->

## Activation choice (intuition)

| Activation | Typical use | Watch-outs |
|------------|-------------|------------|
| Linear | Regression heads | No non-linearity |
| Sigmoid | Binary probs (classic) | Saturation / vanishing gradients |
| Tanh | Zero-centred classic | Still saturates |
| ReLU | Hidden layers (default start) | Dying ReLU. Not a probability |

Match activation to the **decision surface** and training stability, not fashion.

<!-- end SLIDES: -->
