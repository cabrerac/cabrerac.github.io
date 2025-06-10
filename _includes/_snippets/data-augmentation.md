<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Augmentation

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Process of <b>increasing the size and diversity</b> of our datasets.</p>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Increasing diversity to make our models more robust</p>
                <ul>
                    <li>Adding controlled noise</li>
                    <li>Random rotations</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Increasing diversity to make our models more robust</p>
                <ul>
                    <li>Adding controlled noise</li>
                    <li>Random rotations</li>
                    <li>...</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg" alt="Standard Normal Distribution" style="height: 300px">
                <div class="footnote">Inductiveload, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def augment_image(img, angle_range=(-15, 15)):
    angle = np.random.uniform(angle_range[0], angle_range[1])
    rot = rotate(img.reshape(20, 20), angle, mode='edge')
    noise = np.random.normal(0, 0.05, rot.shape)
    aug = rot + (noise * (rot > 0.1))
    return aug.flatten()
```
</div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/7/74/Normal_Distribution_PDF.svg" alt="Standard Normal Distribution" style="height: 300px">
                <div class="footnote">Inductiveload, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def augment_image(img, angle_range=(-15, 15)):
    angle = np.random.uniform(angle_range[0], angle_range[1])
    rot = rotate(img.reshape(20, 20), angle, mode='edge')
    noise = np.random.normal(0, 0.05, rot.shape)
    aug = rot + (noise * (rot > 0.1))
    return aug.flatten()
```
</div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/augmented.png" alt="Data Augmentation" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Increasing the size of our dataset to improve model generalisation</p>
                <ul>
                    <li>Interpolating between existing datapoints</li>
                    <li>Applying domain-specific transformations</li>
                    <li>Generating synthetic data using GANs</li>
                    <li>...</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">

```python
def numerical_smote(data, k=5):
    aug_data = []
    for i in range(len(data)):
        uniq_values = np.unique(data[data != data[i]])
        dists = np.abs(uniq_values - data[i])
        k_neigs = unique_values[np.argsort(dists)[:k]]
        for neig in k_neigs:
            sample = data[i] + np.random.random() * (neig - data[i])
            aug_data.append(sample)
    return np.array(aug_data)
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>SMOTE (Synthtetic Minority Over-sampling Technique)</p>
                <ul>
                    <li>Using the k-nearest neighbours</li>
                    <li>Interpolation between the original data point and the neighbour</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 
