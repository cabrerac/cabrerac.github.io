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
                <p><b>Preparation: a covariance the elements can support</b></p>
                <br>
                <p>$$p(x) = \frac{1}{(2\pi)^{m/2} \sqrt{\det \Sigma}} \exp\left(-\frac{1}{2}(x - \mu)^{\top} \Sigma^{-1} (x - \mu)\right)$$</p>
                <br>
                <p>$n$ elements are described by $m$ attributes in a matrix of shape $n \times m$. The mixture assigns a height $p(x)$ to every element.</p>
                <p>$\Sigma$ is the $m \times m$ covariance, with one width per attribute and one tilt per pair. When $m \geq n$, the centred elements span at most $n-1$ directions, so $\det \Sigma = 0$ and $p(x)$ is undefined.</p>
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
                <p><b>Preparation: a covariance the elements can support</b></p>
                <br>
                <p>$$p(x) = \frac{1}{(2\pi)^{m/2} \sqrt{\det \Sigma}} \exp\left(-\frac{1}{2}(x - \mu)^{\top} \Sigma^{-1} (x - \mu)\right)$$</p>
                <br>
                <p>$n$ elements can support $\Sigma$ when $m < n$. Many attributes move together, so those columns repeat one piece of information.</p>
                <p>Singular value decomposition packs the repeated columns into a few directions. We keep fewer than $n$ of them, the ones with the largest singular values. The mixture fits each bell on those scores.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/singular-value-decomposition.svg" alt="Singular value decomposition as rotation, scaling, rotation" style="height: 280px">
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
                <p>$$p(x) = \frac{1}{(2\pi)^{m/2} \sqrt{\det \Sigma}} \exp\left(-\frac{1}{2}(x - \mu)^{\top} \Sigma^{-1} (x - \mu)\right)$$</p>
                <br>
                <p>The Gaussian mixture gives a density at every point for different bell shaped clouds.</p>
                <br>
                <p>$$p(\mathbf{x}) = \sum_{k=1}^{K} \pi_k \, \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \Sigma_k)$$</p>
                <br>
                <p>$\pi_k$ is the weight of group $k$, and the weights add to 1. $\mathcal{N}$ is the cloud of group $k$, with centre $\boldsymbol{\mu}_k$ and shape $\Sigma_k$. The sum adds the $K$ clouds.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/gaussian-mixture-example.svg" alt="A density made of three bells" style="height: 300px">
                <div class="footnote">Gaussian-mixture-example - Smason79, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
                <p><b>Choosing K:</b> the number of clouds is the $k$ the evaluation keeps.</p>
            </div>
        </div>
    </div>
</div>

## Gaussian Mixtures

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Two bells with weights $\pi_1 = \pi_2 = 0.5$.</p>
                <br>
                <p>At element A: </p>
                $$\mathcal{N}(x_A \mid \mu_1, \Sigma_1) = 0.30, \: \mathcal{N}(x_A \mid \mu_2, \Sigma_2) = 0.10$$
                <p>At element B: </p>
                $$\mathcal{N}(x_B \mid \mu_1, \Sigma_1) = 0.20, \: \mathcal{N}(x_B \mid \mu_2, \Sigma_2) = 0.20$$
                <br>
                <p>Probability of A belonging to bell 1</p>
                <p>$$\gamma_{A1} = \frac{\pi_1 \mathcal{N}(x_A \mid \mu_1, \Sigma_1)}{\pi_1 \mathcal{N}(x_A \mid \mu_1, \Sigma_1) + \pi_2 \mathcal{N}(x_A \mid \mu_2, \Sigma_2)} = 0.75$$</p>
                <br>
                <p>The Expectation Maximisation (EM) loop repeats this step, then move weights, centres and shapes <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer">(Dempster et al., 1977)</a>.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/mixture-two-clouds.svg" alt="Two clouds and the heights at elements A and B" style="height: 380px">
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
place K bells on the kept directions
repeat
    for each element and each bell
        write gamma, that bell's share of p(x)
    for each bell
        set its weight to the average of its gamma values
        set its centre to the gamma-weighted mean of the elements
        set its shape to the gamma-weighted covariance
until p(x) barely changes
give each element the bell with the largest gamma
```

            </div>
            <div class="column vertical-middle text-left" style="width: 5%">
            </div>
            <div class="column vertical-middle text-left" style="width: 47.5%">

```python
from sklearn.decomposition import TruncatedSVD
from sklearn.mixture import GaussianMixture

Z = TruncatedSVD(n_components=n_directions,
                 random_state=SEED).fit_transform(X)
mixture = GaussianMixture(
    n_components=K, covariance_type="full",
    random_state=SEED).fit(Z)  # fit repeats the E and M steps
mixture_labels = mixture.predict(Z)
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
