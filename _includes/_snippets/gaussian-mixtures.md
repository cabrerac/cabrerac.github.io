<!-- SLIDES: -->

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>A <b>Gaussian mixture</b> describes the items as a few overlapping bell shaped clouds and gives each item a probability for each cloud.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>The idea</b></p>
                <p>Each group is a bell shaped cloud.</p>
                <ul>
                    <li>Clouds can be long, tilted, and of different sizes.</li>
                    <li>Each item gets a probability for each group.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/em-clustering-old-faithful.gif" alt="EM fitting two clouds" style="height: 400px">
                <div class="footnote">EM Clustering of Old Faithful data - Chire, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Mixture density</b></p>
                <p>$$p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \Sigma_k)$$</p>
                <p>$\pi_k$ is the weight of group $k$, the weights add to 1.</p>
                <p>$\boldsymbol{\mu}_k$ is its centre.</p>
                <p>$\Sigma_k$ is its covariance, the shape of the cloud.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gaussian-mixture-example.svg" alt="A density made of three bells" style="height: 340px">
                <div class="footnote">Gaussian-mixture-example - Smason79, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>EM</b> <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer">(Dempster et al., 1977)</a></p>
                <p>E step. How much each group explains each item:</p>
                <p>$$\gamma_{ik} = \frac{\pi_k \, \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_k, \Sigma_k)}{\sum_{j} \pi_j \, \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_j, \Sigma_j)}$$</p>
                <p>M step. New weights, centres and covariances from those shares:</p>
                <p>$$\pi_k = \frac{1}{n} \sum_i \gamma_{ik} \qquad \boldsymbol{\mu}_k = \frac{\sum_i \gamma_{ik} \mathbf{x}_i}{\sum_i \gamma_{ik}}$$</p>
                <p>Repeat until the likelihood stops growing.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Choosing K with BIC</b> <a href="https://doi.org/10.1214/aos/1176344136" target="_blank" rel="noopener noreferrer">(Schwarz, 1978)</a></p>
                <p>$$\text{BIC} = -2 \log L + p \log n$$</p>
                <p>$L$ is the likelihood of the fitted mixture.</p>
                <p>$p$ is the number of parameters, it grows with $K$ and with the dimensions.</p>
                <p>$n$ is the number of items.</p>
                <p>Lower is better. More groups must earn their extra parameters.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Soft membership</b></p>
                <p>Each item has a top probability, its best group.</p>
                <ul>
                    <li>Close to 1, the item fits one group well.</li>
                    <li>A low top probability means a weak fit.</li>
                    <li>Those items sit between groups and are worth a look.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gaussian-mixture-example.svg" alt="Gaussian mixture example" style="height: 320px">
                <div class="footnote">Gaussian-mixture-example - Smason79, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Preparation</b></p>
                <p>A full covariance in $d$ dimensions has $d(d+1)/2$ numbers per group.</p>
                <ul>
                    <li>With hundreds of word columns that is far more than the items.</li>
                    <li>So the mixture runs on a few SVD directions.</li>
                    <li>Each direction standardised, so none dominates.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>BIC for each K</li>
                    <li>Keep the lowest</li>
                    <li>Top probability per item</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">

```python
from sklearn.mixture import GaussianMixture

bic = {}
for K in range(1, 9):
    gm = GaussianMixture(n_components=K, covariance_type="full",
                         random_state=SEED).fit(Z_mixture)
    bic[K] = gm.bic(Z_mixture)
K_MIXTURE = min(bic, key=bic.get)

mixture = GaussianMixture(n_components=K_MIXTURE, covariance_type="full",
                          random_state=SEED).fit(Z_mixture)
top_prob = mixture.predict_proba(Z_mixture).max(axis=1)
mixture_labels = mixture.predict(Z_mixture)
print(K_MIXTURE, (top_prob < 0.6).sum())
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
