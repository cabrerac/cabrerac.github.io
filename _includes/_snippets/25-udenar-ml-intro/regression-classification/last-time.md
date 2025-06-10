<!-- SLIDES: -->

## The Data Science Process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Data quality refers to <b>the state of data</b> in terms of its <b>fitness for a purpose</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-quality.jpg" alt="Data Quality" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Data quality refers to <b>the state of data</b> in terms of its <b>fitness for a purpose</b></p>
                <p>This is a multi-dimensional concept</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Accuracy</b></li>
                    <li><b>Completeness</b></li>
                    <li><b>Uniqueness</b></li>
                    <li><b>Consistency</b></li>
                    <li><b>Timeliness</b></li>
                    <li><b>Validity</b></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
               <b>1. Missing Values</b>
                  <ul>
                     <li>Incomplete records</li>
                     <li>Null or NaN values</li>
                     <li>Empty fields</li>
                  </ul>
               <b>2. Inconsistencies</b>
                  <ul>
                     <li>Format variations</li>
                     <li>Unit mismatches</li>
                     <li>Naming conventions</li>
                  </ul>
               <b>3. Outliers</b>
                  <ul>
                     <li>Extreme values</li>
                     <li>Measurement errors</li>
                     <li>Data entry mistakes</li>
                  </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <b>4. Noise</b>
                  <ul>
                     <li>Random variations</li>
                     <li>Measurement errors</li>
                     <li>Background interference</li>
                  </ul>
               <b>5. Bias</b>
                  <ul>
                     <li>Sampling bias</li>
                     <li>Selection bias</li>
                     <li>Measurement bias</li>
                     <li>...</li>
                  </ul>
            </div>
        </div>
    </div>
</div>

## Data Quality

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
               <img src="{{ site.url }}/assets/media/images/data-usability.jpg" alt="Data Usability" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <p><b>Poor data quality can lead to:</b></p>
                <ul>
                    <li>Inaccurate model predictions and reduced reliability</li>
                    <li>Biased results</li>
                    <li>Reduced generalisability</li>
                    <li>Increased training time</li>
                    <li>Higher costs</li>
                    <li>Intellectual debt</li>
                    <li>...</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After collecting the data (i.e., data access), we need to perform <b>a data assessment process to understand the data</b>, identify and mitigate data quality issues, uncover patterns, and gain insights.</p>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
            </div>
        </div>
    </div>
</div>

## ML Pipelines vs ML-based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img class="external-svg"  src="{{ site.url }}/assets/media/images/context-3.png" alt="ML-Based System" style="height: 500px">
            </div>
        </div>
    </div>
</div>

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

## Data Cleaning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p>Process of <b>detecting and correcting (or removing)</b> corrupt or inaccurate records.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Missing Datapoints:</p>
                <ul>
                    <li>Removing rows or columns with missing values</li>
                    <li>Mean imputation</li>
                    <li>Median imputation</li>
                    <li>Regression imputation</li>
                    <li>...</li>
                </ul>
                <p>Outliers:</p>
                <ul>
                    <li>Identify outliers</li>
                    <li>Capping</li>
                    <li>Log transformation</li>
                    <li>...</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Preprocessing

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p>Process of <b>transforming raw data into a format suitable for machine learning</b> while ensuring data quality and consistency.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Feature Scaling:</p>
                <ul>
                    <li>Standarisation (Z-score)</li>
                    <li>Min-Max Scaling</li>
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
            <div class="column vertical-middle text-center" style="width: 50%">
                <p>Process of <b>increasing the size and diversity</b> of our datasets.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Increasing Diversity:</p>
                <ul>
                    <li>Adding controlled noise</li>
                    <li>Random rotations</li>
                    <li>...</li>
                </ul>
                <p>Increasing Size:</p>
                <ul>
                    <li>Interpolating between datapoints</li>
                    <li>Domain-specific transformations</li>
                    <li>GANs</li>
                    <li>...</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Feature Engineering

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p>Process of <b>creating, transforming, and selecting features in our data</b>, combining domain knowledge and creativity.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Creating New Features:</p>
                <ul>
                    <li>Extracting information from existing features</li>
                    <li>Combining existing features</li>
                    <li>Adding domain knowledge</li>
                    <li>...</li>
                </ul>
                <p>Selecting Features:</p>
                <ul>
                    <li>Correlation matrix</li>
                    <li>Decision trees</li>
                    <li>Principal Component Analysis (PCA)</li>
                    <li>...</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->