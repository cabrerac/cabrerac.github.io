<!-- SLIDES: -->

## AI as a Service

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>SOA is a design pattern in which <b>services are provided between components</b>, through a communication protocol over a network.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>SOA is a design pattern in which <b>services are provided between components</b>, through a communication protocol over a network.</p>
                <br>
                <p>Microservices are an architectural style that structures an application as a <b>collection of small, autonomous services</b>. Each microservice is self-contained and implements a business capability.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">
                <br>
                <p>SOA is a design pattern in which <b>services are provided between components</b>, through a communication protocol over a network.</p>
                <br>
                <p>Microservices are an architectural style that structures an application as a <b>collection of small, autonomous services</b>. Each microservice is self-contained and implements a business capability.</p>
                <br>
                <p>The concept of <b>"Everything as a Service" (XaaS)</b> extends the principles of SOA and microservices by offering comprehensive services over the internet. XaaS encompasses a wide range of services, including infrastructure, platforms, and software.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <br>
                <p><b>AI as a Service (AIaaS)</b> enables us to access and expose AI capabilities over the internet. We can integrate AI tools such as machine learning models, natural language processing, and computer vision into our <b>applications leveraging SOA and microservices features.</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## AI as a Service

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
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->