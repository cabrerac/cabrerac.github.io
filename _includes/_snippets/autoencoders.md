<!-- SLIDES: -->

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/autoencoder-schema.png" alt="Autoencoder" style="max-width: 70%; height: auto;">
                <div class="footnote">Autoencoder schema - Michela Massi, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Tasks:</b> dimensionality reduction, denoising, anomaly detection, and generation</p></li>
                    <li><p><b>Data:</b> unlabelled inputs such as images, signals, and feature vectors</p></li>
                    <li><p><b>Key idea:</b> learn to reconstruct the input through a small latent code</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/autoencoder-schema.png" alt="Autoencoder" style="max-width: 70%; height: auto;">
                <div class="footnote">Autoencoder schema - Michela Massi, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Example:</b> handwritten digit images</p>
                <ul>
                    <li><p><b>Input:</b> one image, with no label</p></li>
                    <li><p><b>Latent code:</b> a short vector</p></li>
                    <li><p><b>Output:</b> the reconstructed image</p></li>
                    <li><p><b>Task:</b> reconstruction, such as spotting an unusual digit from a large error</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python implementation:</b> PyTorch</p>
                <p>An autoencoder for vectors of size $D$</p>
                <ul>
                    <li><p><b>Latent code:</b> smaller than $D$</p></li>
                    <li><p><b>Loss:</b> squared error between the input and the reconstruction</p></li>
                    <li><p><b>Target:</b> the input itself, so no labels are needed</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
from torch import nn

class Autoencoder(nn.Module):
    def __init__(self, D, M, latent_dim):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(D, M), nn.ReLU(), nn.Linear(M, latent_dim))
        self.dec = nn.Sequential(nn.Linear(latent_dim, M), nn.ReLU(), nn.Linear(M, D))

    def forward(self, x):
        z = self.enc(x)
        return self.dec(z)

def ae_loss(x_hat, x):
    return ((x - x_hat) ** 2).sum()
```
</div>
        </div>
    </div>
</div>

## Variational Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/vae-basic.png" alt="Variational Autoencoder" style="max-width: 100%; height: auto;">
                <div class="footnote">Variational autoencoder structure - EugenioTL, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><p><b>Tasks:</b> generating new samples and learning a continuous latent space</p></li>
                    <li><p><b>Data:</b> unlabelled inputs such as images, signals, and feature vectors</p></li>
                    <li><p><b>Key idea:</b> the encoder outputs a distribution over the latent code</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Variational Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/vae-basic.png" alt="Variational Autoencoder" style="max-width: 100%; height: auto;">
                <div class="footnote">Variational autoencoder structure - EugenioTL, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Example:</b> the same digit images</p>
                <ul>
                    <li><p><b>Input:</b> one image, with no label</p></li>
                    <li><p><b>Latent code:</b> a sample from a learned distribution</p></li>
                    <li><p><b>Decode:</b> a new image from a drawn code</p></li>
                    <li><p><b>Task:</b> generating new digits</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>Python implementation:</b> PyTorch</p>
                <p>A VAE for vectors of size $D$</p>
                <ul>
                    <li><p><b>log_var:</b> $\ln \boldsymbol{\sigma}^2$ for numerical stability</p></li>
                    <li><p><b>KL term:</b> closed form for Gaussians</p></li>
                    <li><p><b>Added here:</b> mu, log_var, and the KL term</p></li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">

```python
import torch
from torch import nn

class VAE(nn.Module):
    def __init__(self, D, M, latent_dim):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(D, M), nn.ReLU())
        self.mu = nn.Linear(M, latent_dim)
        self.log_var = nn.Linear(M, latent_dim)
        self.dec = nn.Sequential(nn.Linear(latent_dim, M), nn.ReLU(), nn.Linear(M, D))

    def forward(self, x):
        h = self.enc(x)
        mu, log_var = self.mu(h), self.log_var(h)
        z = mu + torch.exp(0.5 * log_var) * torch.randn_like(mu)   # reparameterisation
        return self.dec(z), mu, log_var

def vae_loss(x_hat, x, mu, log_var):
    rec = ((x - x_hat) ** 2).sum()
    kl = -0.5 * (1 + log_var - mu ** 2 - log_var.exp()).sum()
    return rec + kl
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/autoencoder-schema.png" alt="Autoencoder" style="max-width: 70%; height: auto;">
                <div class="footnote">Autoencoder schema - Michela Massi, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Theory:</b> an encoder and a decoder trained together</p>
$$
\mathbf{z} = f_{\text{enc}}(\mathbf{x}) \qquad \hat{\mathbf{x}} = f_{\text{dec}}(\mathbf{z})
$$
$$
E = \sum_{n=1}^{N} \|\mathbf{x}_n - \hat{\mathbf{x}}_n\|^2
$$
                <ul>
                    <li><p><b>Target:</b> the input itself, $y = \mathbf{x}$, so no labels are needed</p></li>
                    <li><p><b>Bottleneck:</b> the latent code $\mathbf{z}$ is smaller than $\mathbf{x}$</p></li>
                    <li><p><b>Linear encoder and decoder:</b> the same subspace as PCA</p></li>
                    <li><p><b>Anomaly detection:</b> a large reconstruction error flags an unusual input</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Autoencoders

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/vae-basic.png" alt="Variational Autoencoder" style="max-width: 100%; height: auto;">
                <div class="footnote">Variational autoencoder structure - EugenioTL, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Variational autoencoder (VAE)</b> <a href="https://arxiv.org/abs/1312.6114" target="_blank" rel="noopener noreferrer">(Kingma and Welling, 2014)</a>: the encoder outputs a distribution</p>
$$
q_\phi(\mathbf{z} \mid \mathbf{x}) = \mathcal{N}\left(\boldsymbol{\mu}, \text{diag}(\boldsymbol{\sigma}^2)\right)
$$
                <p><b>Reparameterisation:</b> sampling that backpropagation can pass through</p>
$$
\mathbf{z} = \boldsymbol{\mu} + \boldsymbol{\sigma} \odot \boldsymbol{\epsilon} \qquad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
$$
                <p><b>Loss:</b> reconstruction plus a KL term</p>
$$
E = \|\mathbf{x} - \hat{\mathbf{x}}\|^2 + D_{\text{KL}}\left(q_\phi(\mathbf{z} \mid \mathbf{x}) \,\|\, \mathcal{N}(\mathbf{0}, \mathbf{I})\right)
$$
                <p><b>Generation:</b> sample $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and decode</p>
</div>
        </div>
    </div>
</div>
