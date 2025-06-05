<!-- SLIDES: -->

## Data Augmentation

## Data Augmentation

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What is Data Augmentation?</b></p>
                <ul>
                    <li>Process of creating new data samples from existing data</li>
                    <li>Improves model generalization and robustness</li>
                    <li>Helps address data scarcity and class imbalance</li>
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
                <p><b>Types of Data Augmentation</b></p>
                <ul>
                    <li>Image Data:
                        <ul>
                            <li>Rotation, flipping, cropping</li>
                            <li>Scaling, translation, shearing</li>
                            <li>Color jitter, noise injection</li>
                        </ul>
                    </li>
                    <li>Text Data:
                        <ul>
                            <li>Synonym replacement</li>
                            <li>Random insertion/deletion</li>
                            <li>Back translation</li>
                        </ul>
                    </li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Types of Data Augmentation (cont.)</b></p>
                <ul>
                    <li>Tabular Data:
                        <ul>
                            <li>Noise injection</li>
                            <li>SMOTE (Synthetic Minority Over-sampling Technique)</li>
                            <li>Random sampling</li>
                        </ul>
                    </li>
                    <li>Time Series Data:
                        <ul>
                            <li>Window slicing</li>
                            <li>Time warping</li>
                            <li>Jittering</li>
                        </ul>
                    </li>
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