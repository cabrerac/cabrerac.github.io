<!-- SLIDES: -->

## Expert Systems (1970-1990) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Capture and apply</b> specialized human <b>expertise</b> to solve complex problems that typically require human experts.
                </p>
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/dendral.svg" alt="DENDRAL expert system" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">DENDRAL (1965-1970): First expert system developed at Stanford to analyze chemical compounds</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Capture and apply</b> specialized human <b>expertise</b> to solve complex problems that typically require human experts.
                </p>
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/dendral.svg" alt="DENDRAL expert system" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">DENDRAL (1965-1970): First expert system developed at Stanford to analyze chemical compounds</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    An <b>expert system</b> is defined by a <em>knowledge base, inference engine, and user interface</em> that work together to apply domain expertise to specific problems.
                </p>
$$
ES = (KB, IE, UI)
$$
$KB$: Knowledge Base (facts and rules)
$IE$: Inference Engine
$UI$: User Interface
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Problem Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Formal Definition</strong></p>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <p><strong>Computational Representation</strong></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Capture and apply</b> specialized human <b>expertise</b> to solve complex problems that typically require human experts.
                </p>
                <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/dendral.svg" alt="DENDRAL expert system" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">DENDRAL (1965-1970): First expert system developed at Stanford to analyze chemical compounds</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    An <b>expert system</b> is defined by a <em>knowledge base, inference engine, and user interface</em> that work together to apply domain expertise to specific problems.
                </p>
$$
ES = (KB, IE, UI)
$$
$KB$: Knowledge Base (facts and rules)
$IE$: Inference Engine
$UI$: User Interface
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Expert systems</b> are typically <em>modelled</em> using rule-based programming with if-then statements and knowledge representation formalisms.
                </p>
                <p style="font-family: monospace; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                    IF patient_has_fever AND patient_has_cough<br>
                    THEN consider_diagnosis(respiratory_infection)<br><br>
                    
                    IF respiratory_infection AND patient_has_chest_pain<br>
                    THEN order_test(chest_x_ray)
                </p>
                <div class="footnote">Rule-based knowledge representation in medical diagnosis expert system</div>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Architecture Components

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <img src="https://d1whtlypfis84e.cloudfront.net/guides/wp-content/uploads/2019/07/29075754/Expert-System-1024x649.jpg" alt="Expert System Architecture" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Classic expert system architecture with knowledge base, inference engine, and user interface</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><strong>Knowledge Base</strong></p>
                <p>Contains domain-specific knowledge represented as facts and rules</p>
                <br>
                <p><strong>Inference Engine</strong></p>
                <p>Processes rules and facts to derive conclusions using forward chaining (data-driven) or backward chaining (goal-driven)</p>
                <br>
                <p><strong>User Interface</strong></p>
                <p>Facilitates interaction between users and the system, including explanation facilities</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Notable Examples

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>MYCIN (1972)</strong></p>
                <p>Diagnosed bacterial infections and recommended antibiotics with accuracy exceeding some doctors</p>
                <br>
                <p><strong>PROSPECTOR (1978)</strong></p>
                <p>Identified potential mineral deposits, successfully predicting a molybdenum deposit worth over $100 million</p>
                <br>
                <p><strong>XCON/R1 (1980)</strong></p>
                <p>Configured VAX computer systems for Digital Equipment Corporation, saving estimated $40 million annually</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>DENDRAL (1965-1970)</strong></p>
                <p>Identified unknown organic compounds from mass spectrometry data</p>
                <br>
                <p><strong>PUFF (1979)</strong></p>
                <p>Interpreted pulmonary function test results to diagnose lung disorders</p>
                <br>
                <p><strong>CADUCEUS/INTERNIST-I (1982)</strong></p>
                <p>Diagnosed complex internal medicine cases covering over 500 diseases</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Reasoning Approaches

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>Forward Chaining (Data-Driven)</strong></p>
                <img src="https://www.researchgate.net/publication/329715657/figure/fig1/AS:705181092986881@1545139632989/Forward-chaining-inference-example.png" alt="Forward Chaining" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Forward chaining: starting with available data and applying rules until reaching a conclusion</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>Backward Chaining (Goal-Driven)</strong></p>
                <img src="https://www.researchgate.net/publication/329715657/figure/fig2/AS:705181092991003@1545139633153/Backward-chaining-inference-example.png" alt="Backward Chaining" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Backward chaining: starting with a goal and working backward to determine what facts are needed</div>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"Expert systems will be the most important commercial application for artificial intelligence in the next decade." (Bruce G. Buchanan, 1983)</em></p>
            <br>
            <p><em>"The use of knowledge in computer programs to solve problems that normally require human expertise is the basic characteristic of expert systems." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Within 10 years, expert systems will be so common that they will disappear as separate applications, and become part of every computer system." (Edward Feigenbaum, 1984)</em></p>
            <br>
            <p><em>"Japan's Fifth Generation Computer Systems project will revolutionize computing through the integration of large-scale knowledge bases." (MITI, Japan, 1982)</em></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://s3.amazonaws.com/s3.timetoast.com/public/uploads/photo/17871326/image/medium-c7cf33db9affa9895ea1daa7c3202a6c.png" alt="Expert Systems in Business (1980s)" style="height: 400px">
            <div class="footnote">Time Magazine cover highlighting AI's business applications (1980s)</div>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Technology Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img class="external-svg" src="{{ site.url }}/assets/media/diagrams/combinatorial-explosion.svg" alt="Combinatorial explosion diagram" style="width: 100%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><strong>Knowledge Acquisition Bottleneck</strong></p>
            <p>Extracting knowledge from human experts and encoding it into rules was difficult, time-consuming, and expensive</p>
            <br>
            <p><strong>Brittleness</strong></p>
            <p>Systems could not reason beyond their pre-programmed knowledge and failed when confronted with unexpected situations</p>
            <br>
            <p><strong>Scaling Limitations</strong></p>
            <p>Adding more rules often led to rule interaction problems and combinatorial explosion</p>
            <br>
            <p><strong>Maintenance Challenges</strong></p>
            <p>Updating knowledge bases as domains evolved required significant effort</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1970-1990) - Legacy and Impact

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><strong>Commercial Success</strong></p>
            <p>First AI systems to achieve commercial success and widespread industry adoption</p>
            <br>
            <p><strong>Knowledge Engineering</strong></p>
            <p>Established knowledge engineering as a discipline for extracting and representing expertise</p>
            <br>
            <p><strong>Practical Applications</strong></p>
            <p>Demonstrated AI's practical utility in specific domains like medicine, finance, and manufacturing</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><strong>AI Winter Contribution</strong></p>
            <p>Overpromising capabilities led to disappointment and contributed to the AI winter of the late 1980s</p>
            <br>
            <p><strong>Modern Influence</strong></p>
            <p>Evolved into business rule management systems and forms the foundation of many decision support systems today</p>
            <br>
            <p><strong>Human-AI Collaboration</strong></p>
            <p>Pioneered the concept of AI systems complementing (rather than replacing) human expertise</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

<!-- RENDER: -->

# Expert Systems (1970-1990)

## The Rise of Knowledge-Based Systems

Expert systems represented the first commercially successful AI applications in the 1970s and 1980s. These knowledge-based systems captured human expertise in narrow domains to solve specific problems that typically required human specialists.

### Key Components of Expert Systems

1. **Knowledge Base**: Domain-specific knowledge represented as facts and rules
2. **Inference Engine**: Mechanism for applying rules to facts to derive conclusions
3. **User Interface**: Mechanism for users to interact with the system and receive explanations

### Notable Expert Systems

- **MYCIN (1972)**: Diagnosed bacterial infections and recommended antibiotics
- **DENDRAL (1965-1970)**: Identified unknown organic compounds from mass spectrometry data
- **PROSPECTOR (1978)**: Identified potential mineral deposits, successfully predicting a molybdenum deposit
- **XCON/R1 (1980)**: Configured VAX computer systems for Digital Equipment Corporation, saving estimated $40 million annually
- **CADUCEUS/INTERNIST-I (1982)**: Diagnosed complex internal medicine cases covering over 500 diseases

### Reasoning Approaches

Expert systems typically used one of two reasoning approaches:

```python
# Example of forward chaining (data-driven reasoning)
def forward_chaining(facts, rules):
    new_facts = set(facts)
    while True:
        # Find all rules that can fire based on current facts
        fired = False
        for rule in rules:
            if rule.condition.issubset(new_facts) and rule.conclusion not in new_facts:
                new_facts.add(rule.conclusion)
                print(f"Applied rule: {rule}")
                fired = True
        
        # If no new facts were derived, we're done
        if not fired:
            break
    
    return new_facts

# Example of backward chaining (goal-driven reasoning)
def backward_chaining(goal, rules, facts):
    if goal in facts:
        return True
    
    # Find rules that could prove this goal
    relevant_rules = [rule for rule in rules if rule.conclusion == goal]
    
    for rule in relevant_rules:
        # Check if all conditions can be satisfied
        all_conditions_met = True
        for condition in rule.conditions:
            if not backward_chaining(condition, rules, facts):
                all_conditions_met = False
                break
        
        if all_conditions_met:
            return True
    
    return False
```

### Legacy and Impact

Expert systems represented the first wave of commercially successful AI applications. They demonstrated that AI could provide practical value in specific domains, even with limited computing resources. However, they also faced significant limitations:

1. **Knowledge Acquisition Bottleneck**: Extracting knowledge from human experts was difficult and time-consuming
2. **Brittleness**: Systems could not reason beyond their pre-programmed knowledge
3. **Scaling Limitations**: Adding more rules often led to rule interaction problems and combinatorial explosion

Despite these limitations, expert systems established knowledge engineering as a discipline and laid the groundwork for future rule-based and knowledge-based applications. Many modern business rule management systems and decision support tools trace their lineage to expert systems.

<!-- end RENDER: -->
