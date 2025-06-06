<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
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
                <p>Data augmentation helps us increase the size and diversity of our datasets.</p>
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
def augment_image(image, angle_range=(-15, 15)):
    angle = np.random.uniform(angle_range[0], angle_range[1])
    rotated = rotate(image.reshape(20, 20), angle, mode='edge')
    noise = np.random.normal(0, 0.05, rotated.shape)
    augmented = rotated + (noise * (rotated > 0.1))
    return augmented.flatten()
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
def augment_image(image, angle_range=(-15, 15)):
    angle = np.random.uniform(angle_range[0], angle_range[1])
    rotated = rotate(image.reshape(20, 20), angle, mode='edge')
    noise = np.random.normal(0, 0.05, rotated.shape)
    augmented = rotated + (noise * (rotated > 0.1))
    return augmented.flatten()
```
</div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/media/augmented.png" alt="Data Augmentation" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Benefits</b></p>
                <ul>
                    <li>Reduces overfitting</li>
                    <li>Improves model generalization</li>
                    <li>Enables use of smaller datasets</li>
                    <li>Helps with class imbalance</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Challenges</b></p>
                <ul>
                    <li>May introduce unrealistic samples</li>
                    <li>Can increase training time</li>
                    <li>Requires domain knowledge for effective transformations</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Best Practices</b></p>
                <ul>
                    <li>Choose augmentation techniques relevant to your data type</li>
                    <li>Validate augmented data for realism and label correctness</li>
                    <li>Monitor model performance with and without augmentation</li>
                    <li>Combine multiple augmentation methods for better results</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 