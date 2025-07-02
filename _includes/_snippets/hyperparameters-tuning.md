<!-- SLIDES: -->

## Hyperparameters Tuning

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>Hyperparameters tuning involves the process of <b>optimising the parameters that govern the training process of a machine learning model</b>, such as learning rate, number of layers, batch size, and number of epochs, to improve its performance and accuracy.</p>
            </div>
        </div>
    </div>
</div>

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>There is not a straight single answer to determine the "right" hyperparameter values.</p>
            </div>
        </div>
    </div>
</div>

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>There is not a straight single answer to determine the "right" hyperparameter values. But, experts follow similar steps:</p>
            <ol>
                <li>Become one with the data</li>
                <li>Set up the end-to-end training/evaluation skeleton</li> 
                <li>Start with a simple model. For most of the tasks, a fully-connected neural network with one hidden layer.</li>
                <li>Implement a complex model that overfits and regularise</li>
                <li>Tune the hyperparameters</li>
                <li>Continue training</li>
            </ol>
            </div>
        </div>
    </div>
</div>

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/15/Neural_Network.svg" alt="Deep Neural Network" style="max-width: 100%; height: auto;">
                <div class="footnote">Deep Neural Network with multiple hidden layers - QuantuMechaniX8, CC0, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-top text-left" style="width: 50%">
                <p>There is not a straight single answer to determine the "right" hyperparameter values. But, experts follow similar steps:</p>
            <ol>
                <li>Become one with the data</li>
                <li>Set up the end-to-end training/evaluation skeleton</li> 
                <li>Start with a simple model. For most of the tasks, a fully-connected neural network with one hidden layer.</li>
                <li>Implement a complex model that overfits and regularise</li>
                <li>Tune the hyperparameters</li>
                <li>Continue training</li>
            </ol>
            <p>See more in <a href="https://karpathy.github.io/2019/04/25/recipe/">Karpathy's recipe</a>, and <a href="https://fullstackdeeplearning.com/spring2021/lecture-7/#:~:text=2%20%2D%20Strategy%20to%20Debug%20Neural,8%20%2D%20Conclusion">Tobin's lecture</a>.</p> 
            </div>
        </div>
    </div>
</div>

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%"> 
                <p>In the process, you should combine the methods previously discussed like preprocessing, feature engineering, normalising inputs, parameters initialisation, etc.</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%"> 
            </div>
        </div>
    </div>
</div>

## Hyperparameters Tuning

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%"> 
                <p>In the process, you should combine the methods previously discussed like preprocessing, feature engineering, normalising inputs, parameters initialisation, etc.</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%"> 
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: --> 