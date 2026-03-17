<!-- SLIDES: -->

## Data-Oriented Computing Systems (DOCS) — Problem and vision

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Deploying ML converts software systems into <b>data-driven systems</b>. These systems are <b>interfaces</b> between socio-technical needs and AI capabilities. Developers do not predefined behaviour—ML components learn it from data. Behaviour depends on data quality; ML components operate as black boxes with stochastic behaviour and propagating uncertainty.</p>
                <p>This shift creates <b>Intellectual Debt</b>: practitioners deploy systems that work in practice but whose inner workings they do not understand. It threatens transparency, safety, and trust.</p>
            </div>
        </div>
    </div>
</div>

## DOCS — The data dichotomy

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>Current computing paradigms prioritise <b>control flow</b> over data, creating the <b>Data Dichotomy</b>: data-driven systems require data exposure, but current paradigms hide it behind interfaces. This limits observability and adaptivity and lies at the root of Intellectual Debt.</p>
                <p><b>DOCS</b> proposes establishing <b>Data-Oriented Computing (DOC)</b> as a new paradigm that treats <b>data as the primary computational entity</b>. DOCS combines theoretical formalisation with empirical validation to develop formal semantics and primitives, establish decentralised and open frameworks, and demonstrate improvements in observability, interpretability, and sustainability.</p>
            </div>
        </div>
    </div>
</div>

## DOCS — Overview

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/interfaces/docs.png" alt="DOCS overview" style="max-height: 480px">
            </div>
        </div>
    </div>
</div>

## DOCS — Key objectives

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>Data as first-class citizen</b> — Formal semantics and primitives that make data the primary computational entity.</li>
                    <li><b>Decentralisation</b> — Local-first, peer-to-peer, and distributed frameworks respecting data ownership, privacy, and fault tolerance.</li>
                    <li><b>Openness</b> — Computational models for autonomous entity interaction and resource discovery in open, dynamic environments.</li>
                    <li><b>Integration and verification</b> — Unified paradigm with formal verification and monitoring to improve interpretability and avoid intellectual debt.</li>
                    <li><b>Paradigm validation</b> — Measurable improvements in observability, interpretability, adaptability, and sustainability across domains.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOCS — Milestones

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <ul>
                    <li><b>WP1</b> — Data-first computing: formal models, data-first primitives, observability APIs.</li>
                    <li><b>WP2</b> — Decentralised data management: consistency models, data ownership, local-first/P2P patterns.</li>
                    <li><b>WP3</b> — Open data-driven systems: resource discovery, asynchronous protocols, dynamic composition, security.</li>
                    <li><b>WP4</b> — From monitoring to shadow systems: monitoring tools, causality and uncertainty models, emulator-based interpretability.</li>
                    <li><b>WP5</b> — Validation: metrics and multi-domain evaluation (including healthcare).</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## DOCS — Impact

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>DOCS aims to provide practitioners with a concrete <b>architectural paradigm and tooling</b> that increase system transparency, reduce intellectual debt, and enable safe, sustainable AI deployments in IoT, edge computing, and healthcare.</p>
                <p><em>Reference:</em> Cabrera, Paleyes, Thodoroff, Lawrence. Machine Learning Systems: A Survey from a Data-Oriented Perspective. ACM Computing Surveys 2025.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
