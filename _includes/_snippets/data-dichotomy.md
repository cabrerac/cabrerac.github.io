<!-- SLIDES: -->

## The Data Dichotomy

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 50%">

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

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text_to_analyze = data.get('text', '')
    sentiment = service.analyze_sentiment(text_to_analyze)
    return jsonify({'sentiment': sentiment})
```
</div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Service-oriented systems focus on operations. Data is secondary and <b>hidden behind service interfaces</b>.</p>
                <br>
                <p><b>The Data Dichotomy</b>: “While data-driven systems are about exposing data, service-oriented architectures and object-oriented programming are about hiding data.” <a
                href="https://www.confluent.io/blog/data-dichotomy-rethinking-the-way-we-treat-data-and-services/" target="_blank" rel="noopener noreferrer">(Stopford, 2016).</a></p>
            </div>
        </div>
    </div>

<!-- end SLIDES: -->
