<!-- SLIDES: -->

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After assessing the data (i.e., data assess), we need to <b>use the data to address the problem in question.</b>. This process includes implementing a <b>Machine Learning algorithm</b> that creates a <b>Machine Learning model</b>.</p>
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A Machine Learning algorithm is a set of instructions</b> that is used to train a machine learning model. It defines how the model learns from data and makes predictions or decisions. Linear regression, decision trees, and neural networks are examples of machine learning algorithms.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-algorithm.svg" alt="ML Algorithm" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>A Machine Learning model is a program</b> that is trained on a dataset and used to make predictions or decisions. The goal is to create a <em>trained model</em> that can generalise well to new, unseen data. For example, a trained model could predict house prices based on new input features, or classify images into different categories.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/ml-model.svg" alt="ML Model" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>A Machine Learning algorithm uses the <b>training process</b> to adjust the Machine Learning model internal parameters to minimise prediction errors. For example, in a linear regression model, the algorithm adjusts the slope and intercept to minimise the difference between predicted and actual values.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The parameters of Machine Learning models are adjusted according to the <b>training data</b> (i.e., seen data). For example, when training a model to predict house prices, the training data would include features like square footage, number of bedrooms, and location, along with their actual sale prices</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The prediction errors are quantified by a <b>loss function</b> that indicates the algorithm how far is the prediction from the target value. This difference is used to update the machine learning model's internal parameters to minimise the prediction errors. Common examples include Mean Squared Error for regression problems and Cross-Entropy for classification problems.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Validation and test datasets</b> (i.e., unseen data) are used to evaluate the Machine Learning model. Validation datasets are used during training to tune hyperparameters. Test datasets are used at the end for final evaluation. We must split our data in training, validation, and test datasets. For instance, if you have 1000 house price records, you might use 700 for training, 150 for validation, and 150 for testing.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Hyperparameters</b> are parameters that are set before training a Machine Learning model. They control the learning process and model architecture, and are typically set by the data scientist or engineer. Examples include learning rate, number of layers in a neural network, and regularization strength.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/hyperparameters.svg" alt="Hyperparameters" style="height: 500px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

