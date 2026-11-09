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
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Partitioning:</b> every item goes to one of $k$ groups around centres.</p>
                <p><b>Model-based:</b> each group is a probability distribution, so membership is a probability.</p>
                <p><b>Density-based:</b> groups are dense regions, and items in thin regions are noise.</p>
                <p><b>Hierarchical:</b> a tree of groups inside groups, cut at a chosen level.</p>
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
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>The idea</b></p>
                <p>Each group is a bell shaped cloud.</p>
                <ul>
                    <li>Clouds can be long, tilted, and of different sizes</li>
                    <li>Each item gets a probability for each group</li>
                    <li>An item between two clouds gets two middling probabilities</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Preparation: a few directions</b></p>
                <p>A full covariance in $d$ dimensions has $d(d+1)/2$ numbers per group. With hundreds of attributes that is more than the items.</p>
                <br>
                <p>$$X = U \, S \, V^{\top}$$</p>
                <p>$X$ is the item by attribute matrix, one row per item. $V$ holds directions over the attributes. $S$ holds how much each direction explains, largest first. $U$ places each item on those directions. Keeping the first $r$ gives $Z = U_r S_r$, with $r$ columns per item.</p>
                <p>On texts this is latent semantic analysis <a href="https://doi.org/10.1002/(SICI)1097-4571(199009)41:6%3C391::AID-ASI1%3E3.0.CO;2-9" target="_blank" rel="noopener noreferrer">(Deerwester et al., 1990)</a>. Each kept direction is then standardised.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
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
            <div class="column vertical-middle text-left" style="width: 55%">
                <p>The mixture gives a density at every point.</p>
                <br>
                <p>$$p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \Sigma_k)$$</p>
                <br>
                <p>$K$ is the number of groups. $\pi_k$ is the weight of group $k$, and the weights add to 1. $\mathcal{N}$ is the bell shaped density of one group, with centre $\boldsymbol{\mu}_k$ and covariance $\Sigma_k$, the shape of the cloud. The sum adds the clouds, each scaled by its weight.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gaussian-mixture-example.svg" alt="A density made of three bells" style="height: 320px">
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
                <p><b>EM <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer">(Dempster et al., 1977)</a></b></p>
                <p>E step, how much each group explains each item:</p>
                <p>$$\gamma_{ik} = \frac{\pi_k \, \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_k, \Sigma_k)}{\sum_{j} \pi_j \, \mathcal{N}(\mathbf{x}_i \mid \boldsymbol{\mu}_j, \Sigma_j)}$$</p>
                <p>The numerator is how well group $k$ explains item $i$, times its weight. The denominator adds the same over all groups, so the shares of one item add to 1.</p>
                <p>M step, new weights, centres and covariances from those shares, such as $\pi_k = \frac{1}{n} \sum_i \gamma_{ik}$. Repeat until the likelihood stops growing.</p>
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
                    <li>At item A, group 1 has density 0.30</li>
                    <li>Group 2 has density 0.10</li>
                </ul>
                <br>
                <p>Item B sits halfway, where both densities are 0.20.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>$$\gamma_{A1} = \frac{0.5 \cdot 0.30}{0.5 \cdot 0.30 + 0.5 \cdot 0.10} = 0.75$$</p>
                <br>
                <p>The numerator is group 1 at A, times its weight. The denominator adds both groups. A belongs to group 1 with probability 0.75 and to group 2 with 0.25. For B both shares are 0.5, so its top probability is low, and B is worth a look.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Choosing K with BIC <a href="https://doi.org/10.1214/aos/1176344136" target="_blank" rel="noopener noreferrer">(Schwarz, 1978)</a></b></p>
                <p>$$\text{BIC} = -2 \log L + p \log n$$</p>
                <p>$L$ is the likelihood of the fitted mixture. $p$ is the number of parameters, which grows with $K$ and with the dimensions. $n$ is the number of items. Lower is better, so more groups must earn their extra parameters. The range of $K$ is set before the results.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>Limits</b></p>
                <ul>
                    <li>Every item still gets a group, only with a lower probability</li>
                    <li>Another seed or another number of directions gives other groups</li>
                    <li>A full covariance needs many items per group</li>
                </ul>
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
reduce the items to a few SVD directions
standardise each direction
for each K in the range set before the results
    start K groups
    repeat
        E: share of each group in each item
        M: new weights, centres and shapes
    until the likelihood stops growing
    BIC of this K
keep the K with the lowest BIC
top probability of each item
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.decomposition import TruncatedSVD
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

def mixture_range(X, n_directions, ks, seed):
    svd = TruncatedSVD(n_components=n_directions,
                       random_state=seed)
    Z = StandardScaler().fit_transform(svd.fit_transform(X))
    fits = {k: GaussianMixture(n_components=k,
                               random_state=seed).fit(Z)
            for k in ks}
    best = min(fits, key=lambda k: fits[k].bic(Z))
    return Z, fits[best]

Z, mixture = mixture_range(X, 10, range(1, 9), seed=0)
top_probability = mixture.predict_proba(Z).max(axis=1)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
