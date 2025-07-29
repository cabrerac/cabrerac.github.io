<!-- SLIDES: -->

## Data Address

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After assessing the data (i.e., data assess), we need to <b>use the data to address the problem in question</b>. This process includes implementing a <b>Machine Learning algorithm</b> that creates a <b>Machine Learning model</b>.</p>
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
                <p><b>A Machine Learning algorithm is a set of instructions</b> that are used to train a machine learning model. It defines how the model learns from data and makes predictions or decisions. Linear regression, decision trees, and neural networks are examples of machine learning algorithms.</p>
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
                <p><b>A Machine Learning model is a program</b> that is trained on a dataset and used to make predictions or decisions. The goal is to create a <em>trained model</em> that can generalise well to new, unseen data. For example, a trained model could predict house prices based on new input features.</p>
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
                <p>A Machine Learning algorithm uses the <b>training process</b> that goes from a specific set of observations to a general rule (i.e., induction). This process adjusts the Machine Learning model internal parameters to minimise prediction errors. For example, in a linear regression model, the algorithm adjusts the slope and intercept to minimise the difference between predicted and actual values.</p>
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
                <p>The parameters of Machine Learning models are adjusted according to the <b>training data</b> (i.e., seen data). For example, when training a model to predict house prices, the training data would include features like square footage, number of bedrooms, and location, along with their actual sale prices. <b>The training data consists of vectors of attribute values.</b></p>
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
                <p>In classification problems, the prediction (i.e., model's output) is one of a finite set of values (e.g., sunny/cloudy/rainy or true/false). In the regression problems, the model's output is a number.</p>
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
                <p>Predictions can deviate from the expected values. Prediction errors are quantified by a <b>loss function</b> that indicates to the algorithm how far the prediction is from the target value. This difference is used to update the machine learning model's internal parameters to minimise the prediction errors. Common examples include Mean Squared Error for regression problems and Cross-Entropy for classification problems.</p>
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
                <p>Three types of feedback can be part of the inputs in our training process:</p>
                <ul>
                    <li><b>Supervised Learning</b>: The model is trained on labeled data to learn a mapping between inputs and the corresponding labels, so the model can make predictions on unseen data.</li>
                    <li><b>Unsupervised Learning</b>: The model is trained on unlabeled data, and it must find patterns in the data. The goal is to identify hidden structures or groupings in the data.</li>
                    <li><b>Reinforcement Learning</b>: The model learns by interacting with an environment and receiving rewards or penalties. The goal is to learn a policy that maximizes the reward.</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/training-process.svg" alt="Training Process" style="height: 500px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

