<!-- SLIDES: -->

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 70%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/group-task-taxonomy.svg" alt="Taxonomy of grouping methods" style="width: 100%; height: 100%">
            </div>
        </div>
    </div>
    <div class="row" style="height: 30%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p><b>Partitioning:</b> each item goes to one of $k$ groups around centres.</p>
                <p><b>Model-based:</b> each group is a distribution, so membership is a probability.</p>
                <p><b>Density-based:</b> groups are dense regions, and thin regions are noise.</p>
                <p><b>Hierarchical:</b> a tree of groups inside groups.</p>
            </div>
        </div>
    </div>
</div>

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
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The idea</b></p>
                <ul>
                    <li>Clouds can be long, tilted, and of different sizes</li>
                    <li>Each item gets a probability for each group</li>
                    <li>An item between two clouds gets two middling probabilities</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/em-clustering-old-faithful.gif" alt="EM fitting two clouds" style="height: 360px">
                <div class="footnote">EM Clustering of Old Faithful data - Chire, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Preparation: a few directions</b></p>
                <p>A full covariance in $d$ dimensions has $d(d+1)/2$ numbers per group. With hundreds of attributes that is more than the items.</p>
                <p>$$X = U \, S \, V^{\top}$$</p>
                <p>$X$ has one row per item. $V$ holds directions over the attributes, $S$ how much each one explains, and $U$ where each item sits on them.</p>
                <p>We keep the first 5 directions and standardise each one.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/singular-value-decomposition.svg" alt="Singular value decomposition as rotation, scaling, rotation" style="height: 300px">
                <div class="footnote">Singular-Value-Decomposition - Georg-Johann, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The mixture gives a density at every point.</p>
                <br>
                <p>$$p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \Sigma_k)$$</p>
                <br>
                <p>$\pi_k$ is the weight of group $k$, and the weights add to 1. $\mathcal{N}$ is the cloud of group $k$, with centre $\boldsymbol{\mu}_k$ and shape $\Sigma_k$. The sum adds the $K$ clouds.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gaussian-mixture-example.svg" alt="A density made of three bells" style="height: 300px">
                <div class="footnote">Gaussian-mixture-example - Smason79, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
                <p><b>Choosing K:</b> $K$ from 1 to 8, and the lowest BIC wins <a href="https://doi.org/10.1214/aos/1176344136" target="_blank" rel="noopener noreferrer">(Schwarz, 1978)</a>.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li>Two groups with weights 0.5 and 0.5</li>
                    <li>At item A, group 1 has density 0.30 and group 2 has 0.10</li>
                    <li>At item B, both have 0.20</li>
                </ul>
                <p>$$\gamma_{A1} = \frac{0.5 \cdot 0.30}{0.5 \cdot 0.30 + 0.5 \cdot 0.10} = 0.75$$</p>
                <p>A belongs to group 1 with probability 0.75. B gets 0.5 for each group, because it sits between the clouds.</p>
                <p><b>EM:</b> repeat this step, then move the weights, centres and shapes <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer">(Dempster et al., 1977)</a>.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/mixture-two-clouds.svg" alt="Two clouds and the densities at items A and B" style="height: 380px">
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 47.5%">

```text
reduce the items to 10 SVD directions
keep the first 5 and standardise each one
for each K from 1 to 8
    fit K clouds with E and M steps
    keep the BIC of this K
choose the K with the lowest BIC
fit again with that K
give each item its most likely group
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.decomposition import TruncatedSVD
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

svd = TruncatedSVD(n_components=DENSITY_SVD_DIRECTIONS,
                   random_state=SEED)
Z = svd.fit_transform(X)
Z_mixture = StandardScaler().fit_transform(
    Z[:, :MIXTURE_SVD_DIRECTIONS])

bic = {}
for K in MIXTURE_K:
    model = GaussianMixture(
        n_components=K, covariance_type="full",
        random_state=SEED).fit(Z_mixture)
    bic[K] = model.bic(Z_mixture)
K_MIXTURE = min(bic, key=bic.get)
mixture = GaussianMixture(
    n_components=K_MIXTURE, covariance_type="full",
    random_state=SEED).fit(Z_mixture)
mixture_labels = mixture.predict(Z_mixture)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
