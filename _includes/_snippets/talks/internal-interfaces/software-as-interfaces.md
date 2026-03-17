<!-- SLIDES: -->

## The AI adoption process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/adoption-1.svg" alt="AI adoption" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The AI adoption process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/adoption-2.svg" alt="AI adoption" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The AI adoption process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/adoption-3.svg" alt="AI adoption" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The AI adoption process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/adoption-4.svg" alt="AI adoption" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The AI adoption process

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/s4-general-diagram-adoption.svg" alt="Software as interface" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Software as interfaces

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/diagrams/s4-general-diagram-adoption.svg" alt="Software as interface" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Software systems are the <b>interfaces</b> between socio-technical needs and AI capabilities.</p>
                <p>Socio-technical systems include people, institutions, infrastructure, and digital technologies that cooperate to serve society.</p>
            </div>
        </div>
    </div>
</div>

## The "technocentric" View

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/single-model.png" alt="Single Model" style="height: 200px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="https://imgs.xkcd.com/comics/machine_learning.png" alt="ML System?" style="height: 500px">
                <div class="footnote">https://xkcd.com/1838/, CC BY-NC 2.5 <https://creativecommons.org/licenses/by-nc/2.5/>, via XKCD</div>
            </div>
        </div>
    </div>
</div>

## The data dichotomy

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
                <p><b>The Data Dichotomy</b>: “While data-driven systems are about exposing data, service-oriented architectures and object-oriented programming are about hiding data.” <a
                href="https://www.confluent.io/blog/data-dichotomy-rethinking-the-way-we-treat-data-and-services/" target="_blank" rel="noopener noreferrer">(Stopford, 2016).</a></p>
            </div>
        </div>
    </div>
</div>

## Intellectual debt

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/complex-systems.png" alt="AI System" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>
                  <b>Intellectual Debt</b>: Practitioners deploy data-driven systems that work in practice, but do not fully understand their inner workings. This threatens transparency, safety, and trust, increasing risks of AI's negative social impact <a href="https://www.cambridge.org/core/books/cambridge-handbook-of-responsible-artificial-intelligence/intellectual-debt/F5D4CF05857D072ABED383AE7A3222E4" target="_blank" rel="noopener noreferrer">(Zittrain, 2022)</a>.</p>
            </div>
        </div>
    </div>
</div>

## AI adoption challenges

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The AI revolution is transforming software into data-driven systems that learn from data and operate in dynamic environments. This introduces new requirements for transparency, safety, and human control. Four interrelated challenges:</p>
                <ul>
                    <li><b>Technocentrism:</b> AI-models at deployment do not work in isolation and are part of larger systems. The requirements are more complex than accuracy.</li>
                    <li><b>Data dichotomy:</b> AI-based systems require exposing data but current paradigms prioritise control flow and hide data behind interfaces.</li>
                    <li><b>Intellectual debt:</b> Systems work in practice but remain opaque to practitioners and stakeholders, undermining transparency, safety, and trust. This aspect is exacerbated by AI models generating software.</li>
                </ul>
                <p>These challenges are generating the following problems:</p>
                <ul>
                    <li><b>Human lack of control:</b> As systems become autonomous and complex, their behaviour can exceed human comprehension.</li>
                    <li><b>Interpretability: </b> Systems must explain behaviour in dynamic environments. Current approaches rely on limited, black-box knowledge.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
