<!-- SLIDES: -->

## The Interfaces Research Programme

<div class="rows" style="height: 100%">
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
               <br>
               <br>
               <img src="{{ site.url }}/assets/media/images/interfaces-logo.png" alt="Interfaces logo" style="height: 500px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 50%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 100%">
                <p style="margin-top: 1em;">The programme takes a systems perspective and treats software as the interface between socio-technical needs and AI capabilities.</p>
            </div>
        </div>
    </div>
</div>

## The Systems View

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="ML-based system in context" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

## The Systems View

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
               <p>
                  AI-based software systems are <i>data-driven</i>. Unlike in traditional systems, developers cannot fully predefine their behaviour. ML components learn such behaviour from data, operating as black boxes that propagate uncertainty into complex software.
               </p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

<!-- SLIDES: -->

## The Interfaces Research Programme

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>How are systems designed and developed?</b></p>
                <p>Focus on operations (e.g., microservices). But now systems are data-driven (i.e., the data-dichotomy).</p>
                <p><b>How are systems maintained at deployment?</b></p>
                <p>Autonomous systems that self-adapt. But their decisions are hard to interpret (i.e., intellectual debt).</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/context-3.png" alt="AI System" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## The Data Dichotomy

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

## Intellectual Debt

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

## The Interfaces Research Agenda

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Two complementary projects that aim to address the dichotomy and mitigate the debt:</p>
                <ul>
                    <li><b>DOCS: Data-Oriented Computing Systems:</b> Aims to develop the Data-Oriented Architectures (DOAs) style for desining systems that prioritise data instead of operations.</li>
                    <li><b>S4: Self-Sustaining Software Systems:</b> Aims to define the building blocks for the next generation of autonomous systems that self-sustain while keeping humans in control.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

## Programme objectives

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>Design, architect, and build:</b> Novel paradigms for software architecture to design, develop, deploy, and decommission AI-based systems.</li>
                    <li><b>Interpret AI-based systems:</b> Techniques and tools to improve interpretability of autonomous behaviour and decisions, while keeping humans in control and steering.</li>
                </ul>
                <p>The outputs will benefit engineers, practitioners, and the general public through advances that different communities can use to build sustainable AI-based systems.</p>
            </div>
        </div>
    </div>
</div>

## Partners and collaborations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>The Interfaces programme validates its contributions through use cases across multiple domains: <b>IoT and smart environments</b>, <b>edge computing and local-first systems</b>, <b>healthcare</b>, and <b>security</b>.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
