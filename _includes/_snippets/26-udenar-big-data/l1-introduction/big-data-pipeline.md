<!-- SLIDES: -->

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 420px">
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Cloud setup (client-server)</b></p>
                <ul>
                    <li>A server exposes an interface over the network</li>
                    <li>A client consumes that interface to request data or compute</li>
                    <li>Big data pipelines often split work across both sides</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/soa-cloud.png" alt="Client-server architecture" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <p>SOA is a design pattern in which <b>services are provided between components</b>, through a communication protocol over a network.</p>
                <br>
                <p>Microservices are an architectural style that structures an application as a <b>collection of small, autonomous services</b>. Each microservice is self-contained and exposes a business capability, which is implemented by an object (i.e., OOP).</p>
                <br>
                <p>The concept of <b>"Everything as a Service" (XaaS)</b> extends the principles of SOA and microservices by offering comprehensive services over the internet. XaaS encompasses a wide range of services, including infrastructure, platforms, and software.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/soa-system.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>AI as a Service (AIaaS)</b> enables us to access and expose AI capabilities over the internet. We can integrate AI tools such as machine learning models, natural language processing, and computer vision into our <b>applications leveraging SOA and microservices features.</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/soa-system.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>

```python
from flask import Flask, request, jsonify
app = Flask(__name__)
class SentimentAnalysisService:
    def __init__(self, model):
        self.model = model

    def analyze_sentiment(self, text):
        sentiment_score = self.model.predict(text)
        if sentiment_score > 0.5:
            return "Positive"
        elif sentiment_score < -0.5:
            return "Negative"
        else:
            return "Neutral"
...
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text_to_analyze = data.get('text', '')
    sentiment = service.analyze_sentiment(text_to_analyze)
    return jsonify({'sentiment': sentiment})
...
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/soa-system.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>

```python
from flask import Flask, request, jsonify
app = Flask(__name__)
class SentimentAnalysisService:
    def __init__(self, model):
        self.model = model

    def analyze_sentiment(self, text):
        sentiment_score = self.model.predict(text)
        if sentiment_score > 0.5:
            return "Positive"
        elif sentiment_score < -0.5:
            return "Negative"
        else:
            return "Neutral"
...
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text_to_analyze = data.get('text', '')
    sentiment = service.analyze_sentiment(text_to_analyze)
    return jsonify({'sentiment': sentiment})
...
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Focus on Operations:</p>
                <ul>
                    <li>Separation of concerns</li>
                    <li>High availability</li>
                    <li>Scalability</li>
                    <li>Low latency</li>
                </ul>
                <p>Data is secondary and hidden behind services' interfaces, making data collection difficult</p> <p>Centralised deployments are not sustainable and threatens data privacy and ownership</p>
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Data-Orientated Architectures</b> make data available by design facilitating monitoring and maintenance. Decentralisation supports local data processing, reducing latency and improving privacy by respecting data ownership. Openness enables managing resource-constrained environments by exploiting the computing power of everyday devices <a
                href="https://dl.acm.org/doi/full/10.1145/3769292" target="_blank" rel="noopener noreferrer">(Cabrera et al., 2025)</a>.</p>
                <br>
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/decentralised-deployment.png" alt="Edge deployment" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Edge computing</b></p>
                <ul>
                    <li>Process and filter close to sensors, devices, or users</li>
                    <li>Edge nodes have limited compute and storage</li>
                    <li>Trade-offs vs cloud: latency, connectivity, cost, governance, and data ownership</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Big Data Pipeline and Ecosystem

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/big-data-pipeline-template.svg" alt="Pipeline template" style="height: 420px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
