<!-- SLIDES: -->

## Generative Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Generative_adversarial_network.svg" alt="Generative Adversarial Network" style="max-width: 60%; height: auto;">
                <div class="footnote">GANs - Zhang, Aston and Lipton, Zachary C. and Li, Mu and Smola, Alexander J., CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 55%">
                <p><b>Generative Adversarial Networks (GANs):</b> Used for generating realistic data samples, such as images and audio.</p>
                <ul>
                    <li><p><b>Tasks:</b> generating images, audio, and synthetic data</p></li>
                    <li><p><b>Data:</b> unlabelled samples from the data distribution $p_{\text{data}}$</p></li>
                    <li><p><b>Key idea:</b> learn to produce new samples that look like the training data</p></li>
                </ul>
                <p><b>Diffusion models</b> follow the same goal by learning to remove noise</p>
</div>
        </div>
    </div>
</div>

## Generative Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Generative_adversarial_network.svg" alt="Generative Adversarial Network" style="max-width: 60%; height: auto;">
                <div class="footnote">GANs - Zhang, Aston and Lipton, Zachary C. and Li, Mu and Smola, Alexander J., CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p><b>GAN</b> <a href="https://arxiv.org/abs/1406.2661" target="_blank" rel="noopener noreferrer">(Goodfellow et al., 2014)</a>: two networks trained against each other</p>
$$
\min_{G} \max_{D} \; \mathbb{E}_{\mathbf{x} \sim p_{\text{data}}}\left[\ln D(\mathbf{x})\right] + \mathbb{E}_{\mathbf{z} \sim p(\mathbf{z})}\left[\ln\left(1 - D(G(\mathbf{z}))\right)\right]
$$
                <ul>
                    <li><p><b>Generator $G$:</b> maps noise $\mathbf{z}$ to a sample</p></li>
                    <li><p><b>Discriminator $D$:</b> probability that a sample is real</p></li>
                    <li><p><b>Training:</b> alternate gradient steps on $D$ and $G$</p></li>
                    <li><p><b>Difficulties:</b> mode collapse and unstable training</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Generative Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/denoising-diffusion.png" alt="Denoising Diffusion" style="max-width: 100%; height: auto;">
                <div class="footnote">Example of denoising diffusion models - MrAlanKoh, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 60%">
                <p><b>Diffusion models</b> <a href="https://arxiv.org/abs/2006.11239" target="_blank" rel="noopener noreferrer">(Ho et al., 2020)</a>: learn to reverse a noising process</p>
                <p><b>Forward process:</b> add Gaussian noise over $T$ steps</p>
$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \, \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \, \boldsymbol{\epsilon} \qquad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
$$
                <p><b>Loss:</b> a network $\boldsymbol{\epsilon}_\theta$ predicts the noise</p>
$$
E = \mathbb{E}_{t, \mathbf{x}_0, \boldsymbol{\epsilon}}\left[\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2\right]
$$
                <ul>
                    <li><p><b>Noise schedule $\bar{\alpha}_t$:</b> decreases from 1 towards 0, not the learning rate</p></li>
                    <li><p><b>Sampling:</b> start from noise $\mathbf{x}_T$ and denoise step by step to $\mathbf{x}_0$</p></li>
                </ul>
</div>
        </div>
    </div>
</div>

## Generative Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Python implementation:</b> PyTorch</p>
                <p>One GAN training step</p>
                <ul>
                    <li><p><b>Discriminator:</b> real to 1, fake to 0</p></li>
                    <li><p><b>Generator:</b> make $D$ output 1 on fakes</p></li>
                    <li><p><b>detach():</b> no generator update in the discriminator step</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
import torch
from torch import nn

bce = nn.BCEWithLogitsLoss()
real, fake_label = torch.ones(batch_size, 1), torch.zeros(batch_size, 1)
fake = G(torch.randn(batch_size, latent_dim))

d_loss = bce(D(x_real), real) + bce(D(fake.detach()), fake_label)
opt_D.zero_grad()
d_loss.backward()
opt_D.step()

g_loss = bce(D(fake), real)
opt_G.zero_grad()
g_loss.backward()
opt_G.step()
```
</div>
        </div>
    </div>
</div>

## Generative Models

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Python implementation:</b> PyTorch</p>
                <p>One diffusion training step</p>
                <ul>
                    <li><p><b>model:</b> any network that maps $(\mathbf{x}_t, t)$ to a noise estimate</p></li>
                    <li><p><b>Noise steps $T$:</b> often 1,000</p></li>
                </ul>
            </div>
            <div class="column vertical-top text-left" style="width: 70%">

```python
import torch

T = 1000
beta = torch.linspace(1e-4, 0.02, T)               # noise schedule
alpha_bar = torch.cumprod(1 - beta, dim=0)

t = torch.randint(0, T, (batch_size,))
eps = torch.randn_like(x0)
a = alpha_bar[t].view(-1, *([1] * (x0.dim() - 1)))
x_t = a.sqrt() * x0 + (1 - a).sqrt() * eps        # forward process
loss = ((eps - model(x_t, t)) ** 2).mean()        # predict the noise
optimiser.zero_grad()
loss.backward()
optimiser.step()
```
</div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
