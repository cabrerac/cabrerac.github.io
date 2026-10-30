<!-- SLIDES: -->

## Reducing the Dimensions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>An item by word matrix</b></p>
                <ul>
                    <li>One row per item, one column per word</li>
                    <li>Hundreds or thousands of columns</li>
                    <li>Most cells are zero</li>
                    <li>Words that go together form blocks</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 55%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/topic-detection-document-word-matrix.gif" alt="Blocks of words appear in a document word matrix" style="height: 380px">
                <div class="footnote">Topic detection in a document-word matrix - Christoph Carl Kling, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reducing the Dimensions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>Singular value decomposition</b></p>
                <p>$$X = U \, S \, V^{\top}$$</p>
                <ul>
                    <li><p>$V$ holds directions over the words</p></li>
                    <li><p>$S$ holds how much each direction explains, largest first</p></li>
                    <li><p>Keep the first $r$ directions, $Z = U_r S_r$</p></li>
                    <li><p>Explained variance tells how much of $X$ is kept</p></li>
                </ul>
                <p>Used on text it is called latent semantic analysis <a href="https://doi.org/10.1002/(SICI)1097-4571(199009)41:6%3C391::AID-ASI1%3E3.0.CO;2-9" target="_blank" rel="noopener noreferrer">(Deerwester et al., 1990)</a>.</p>
            </div>
            <div class="column vertical-middle text-center" style="width: 45%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/singular-value-decomposition.svg" alt="Singular value decomposition as rotation, scaling, rotation" style="height: 360px">
                <div class="footnote">Singular-Value-Decomposition - Georg-Johann, CC BY-SA 3.0 <https://creativecommons.org/licenses/by-sa/3.0>, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Reducing the Dimensions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Why distances fail in many dimensions</b></p>
                <ul>
                    <li>With many columns, the nearest and the farthest item end up at almost the same distance <a href="https://doi.org/10.1007/3-540-49257-7_15" target="_blank" rel="noopener noreferrer">(Beyer et al., 1999)</a></li>
                    <li>Then "close" says little</li>
                    <li>Density methods suffer most, almost every item looks alone</li>
                    <li>A few SVD directions keep the main word blocks and drop the rest</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Reducing the Dimensions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 35%">
                <p><b>Python</b></p>
                <ul>
                    <li>Fit on the scaled vectors</li>
                    <li>Read the explained variance</li>
                    <li>Keep few directions, then standardise them for a mixture</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 65%">


```python
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

svd = TruncatedSVD(n_components=DENSITY_COMPONENTS, random_state=SEED)
Z = svd.fit_transform(X)
print(svd.explained_variance_ratio_.cumsum().round(3))

Z_mixture = StandardScaler().fit_transform(Z[:, :MIXTURE_COMPONENTS])
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
