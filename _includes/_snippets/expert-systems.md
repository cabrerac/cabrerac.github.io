<!-- SLIDES: -->

## Expert Systems (1969-1986) - Knowledge-Based Systems

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

## Expert Systems (1969-1986) - Knowledge-Based Systems

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
                    Agents are limited because of the problems complexity. They should leverage <b>human knowledge</b> and emulate <b>human reasoning</b>.
                </p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/2d/LiewDIKrepresentation.png" alt="Data, Information, and Knowledge" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Data, Information, and Knowledge (Per Liew, 2007)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

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
                    Agents are limited because of the problems complexity. They should leverage <b>human knowledge</b> and emulate <b>human reasoning</b>.
                </p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/2d/LiewDIKrepresentation.png" alt="Data, Information, and Knowledge" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Data, Information, and Knowledge (Per Liew, 2007)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    An <b>expert system</b> is defined by a <em>knowledge base, inference engine, and user interface</em> that work together to apply domain expertise to specific problems.
                </p>
$$
ES = (KB, IE, UI)
$$
$KB$: Knowledge Base
$IE$: Inference Engine
$UI$: User Interface
</div>
            <div class="column vertical-middle text-left" style="width: 33%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

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
                    Agents are limited because of the problems complexity. They should leverage <b>human knowledge</b> and emulate <b>human reasoning</b>.
                </p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/2/2d/LiewDIKrepresentation.png" alt="Data, Information, and Knowledge" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Data, Information, and Knowledge (Per Liew, 2007)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    An <b>expert system</b> is defined by a <em>knowledge base, inference engine, and user interface</em> that work together to apply domain expertise to specific problems.
                </p>
$$
ES = (KB, IE, UI)
$$
$KB$: Knowledge Base
$IE$: Inference Engine
$UI$: User Interface
</div>
            <div class="column vertical-middle text-left" style="width: 33%">
                <p>
                    <b>Knowledge</b> is typically modelled using subject, object, predicate <b>semantic triple model.</b>
                </p>
                <img class="external-svg" src="https://upload.wikimedia.org/wikipedia/commons/8/88/Basic_RDF_Graph.svg" alt="Semantic Triple Model" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Basic Semantic Triple</div>
                <p>
                    <b>Rules</b> are if statements.</b>
                </p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"An <b>ontology</b> is an explicit specification of a <em>shared conceptualisation.</em>" (Gruber, 1993)</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/0/00/OntologyBasic.png" alt="Vehicles Ontology" style="width: 70%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Vehicles Ontology: ​English Wikipedia user Gwernol, CC BY-SA 3.0 <http://creativecommons.org/licenses/by-sa/3.0/>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"An <b>ontology</b> is an explicit specification of a <em>shared conceptualisation.</em>" (Gruber, 1993)</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/8/8c/Wikidata-spacecraft-ontology-2017-05-11.png" alt="Spacecraft Ontology" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Spacecraft Ontology: Fuzheado, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"An <b>ontology</b> is an explicit specification of a <em>shared conceptualisation.</em>" (Gruber, 1993)</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Ontology_of_Things_%28OoT%29_Framework_Using_Ontology_of_Ontology.png" alt="Ontology of Things" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
                <div class="footnote">Ontology of Things: Niceclat, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>"An <b>ontology</b> is an explicit specification of a <em>shared conceptualisation.</em>" (Gruber, 1993)</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-bottom text-left" style="width: 50%">
                <p><strong>Konwledge Base</strong></p>
                <p><strong>Example:</strong> Medical diagnosis</p>
                <p>The expert systems embodies medical knowledge</p>
            </div>
            <div class="column vertical-bottom text-left" style="width: 50%">
                <p><strong>Forward Chaining (Data-Driven)</strong></p>
                <p>Facts: The patient has fever, cough, headache, and muscle pain</p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 80%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <pre style="background-color: #f8f8f8; padding: 8px; border-radius: 4px; margin-top: 5px;">
Rules:
R1: If (fever AND cough) then 
(possible_flu)
R2: If (possible_flu AND headache) then (influenza)
R3: If (influenza AND muscle_pain) then (severe_case)</pre>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <pre style="background-color: #f8f8f8; padding: 8px; border-radius: 4px; margin-top: 5px;">
Process:
Facts: [fever, cough, headache, muscle_pain]
→ apply R1: add possible_flu
Facts: [headache, muscle_pain, possible_flu]
→ apply R2: add influenza
Facts: [muscle_pain, influenza]
→ apply R3: conclude sever_case</pre>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Knowledge-Based Systems

<div class="rows" style="height: 100%">
    <div class="row" style="height: 35%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-bottom text-left" style="width: 50%">
                <p><strong>Konwledge Base</strong></p>
                <p><strong>Example:</strong> Medical diagnosis</p>
                <p>The expert systems embodies medical knowledge</p>
            </div>
            <div class="column vertical-bottom text-left" style="width: 50%">
                <p><strong>Backward Chaining (Goal-Driven)</strong></p>
                <p>Facts: The patient has fever, cough, headache, and muscle pain</p>
                <p><b>Goal: Determine if the patient's case is severe</b></p>
            </div>
        </div>
    </div>
    <div class="row" style="height: 65%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <pre style="background-color: #f8f8f8; padding: 8px; border-radius: 4px; margin-top: 5px;">
Rules:
R1: If (fever AND cough) then 
(possible_flu)
R2: If (possible_flu AND headache) then (influenza)
R3: If (influenza AND muscle_pain) then (severe_case)</pre>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <pre style="background-color: #f8f8f8; padding: 8px; border-radius: 4px; margin-top: 5px;">
Process:
→ check for severe_case via R3
→ check for muscle_pain (found)
→ check for influenza via R2
→ check for headache (found)
→ check for possible_flu via R1
→ check for fever and cough
→ conclude severe_case is true</pre>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Relative Success

## Expert Systems (1969-1986) - Relative Success

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>DENDRAL (1960s)</strong></p>
                <p>Identified unknown organic molecules using knowledge of chemistry</p>
                <br>
                <p><strong>MYCIN (Earlys 1970s)</strong></p>
                <p>Supported bacterial infections diagnosis and treatment</p>
                <br>
                <p><strong>XCON/R1 (1982)</strong></p>
                <p>eXpert CONfigurer - Automated the configuration of VAX computer systems (successful deployment)</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - Relative Success

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>DENDRAL (1960s)</strong></p>
                <p>Identified unknown organic molecules using knowledge of chemistry</p>
                <br>
                <p><strong>MYCIN (Earlys 1970s)</strong></p>
                <p>Supported bacterial infections diagnosis and treatment</p>
                <br>
                <p><strong>XCON/R1 (1982)</strong></p>
                <p>eXpert CONfigurer - Automated the configuration of VAX computer systems (successful deployment)</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><strong>PUFF (1982)</strong></p>
                <p>Interpreted pulmonary function test results to diagnose lung disorders</p>
                <br>
                <p><strong>PROSPECTOR (1986)</strong></p>
                <p>An expert system for mineral exploration</p>
                <br>
                <p><strong>DEEP BLUE (1997)</strong></p>
                <p>An expert system that defeated a chess world champion</p>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Perception

## Expert Systems (1969-1986) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"In medicine, management, and the military — indeed in most of the world's work — the daily tasks are those requiring symbolic reasoning with detailed professional knowledge." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Commercialising Artificial Intelligence." (The New York Times, 1982)</em></p>
            <br>
            <p><em>"Gains are Slow for Artificial Intelligence Industry." (The New York Times, 1987)</em></p>
            <br>
            <p><em>"New expert systems companies were being formed at a rate of what seemed like one a week. " (Hart, 2021)</em></p>
            <br>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="{{ site.url }}/assets/media/images/ai-bytes-1981.jpg" alt="Artificial Intelligence (1981)" style="height: 520px">
            <div class="footnote">Issues with knowledge libraries (Robersts, 1981) - https://microship.com/artificial-intelligence-byte/</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"In medicine, management, and the military — indeed in most of the world's work — the daily tasks are those requiring symbolic reasoning with detailed professional knowledge." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Commercialising Artificial Intelligence." (The New York Times, 1982)</em></p>
            <br>
            <p><em>"Gains are Slow for Artificial Intelligence Industry." (The New York Times, 1987)</em></p>
            <br>
            <p><em>"New expert systems companies were being formed at a rate of what seemed like one a week. " (Hart, 2021)</em></p>
            <br>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="{{ site.url }}/assets/media/images/more-than-expert-the-sydney-morning-herald-1985.jpg" alt="Intelligence is more than experts (1985)" style="height: 520px">
            <div class="footnote">Intelligence is More than Experts (The Sidney Morning Herald, 1985)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"In medicine, management, and the military — indeed in most of the world's work — the daily tasks are those requiring symbolic reasoning with detailed professional knowledge." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Commercialising Artificial Intelligence." (The New York Times, 1982)</em></p>
            <br>
            <p><em>"Gains are Slow for Artificial Intelligence Industry." (The New York Times, 1987)</em></p>
            <br>
            <p><em>"New expert systems companies were being formed at a rate of what seemed like one a week. " (Hart, 2021)</em></p>
            <br>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="{{ site.url }}/assets/media/images/ai-stocks-1987.png" alt="AI just could be a smart buy (1987)" style="height: 400px">
            <div class="footnote">AI just could be a smart buy (1987)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"In medicine, management, and the military — indeed in most of the world's work — the daily tasks are those requiring symbolic reasoning with detailed professional knowledge." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Commercialising Artificial Intelligence." (The New York Times, 1982)</em></p>
            <br>
            <p><em>"Gains are Slow for Artificial Intelligence Industry." (The New York Times, 1987)</em></p>
            <br>
            <p><em>"New expert systems companies were being formed at a rate of what seemed like one a week. " (Hart, 2021)</em></p>
            <br>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Perception

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="{{ site.url }}/assets/media/images/kasparov-lost-angeles-times-1997.jpg" alt="Deep Blue defeats Kasparaov (1997)" style="height: 460px">
            <div class="footnote">Deep Blue defeats Kasparaov (Los Angeles Times, 1997)</div>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p><em>"In medicine, management, and the military — indeed in most of the world's work — the daily tasks are those requiring symbolic reasoning with detailed professional knowledge." (Feigenbaum, 1982)</em></p>
            <br>
            <p><em>"Commercialising Artificial Intelligence." (The New York Times, 1982)</em></p>
            <br>
            <p><em>"Gains are Slow for Artificial Intelligence Industry." (The New York Times, 1987)</em></p>
            <br>
            <p><em>"New expert systems companies were being formed at a rate of what seemed like one a week. " (Hart, 2021)</em></p>
            <br>
            </div>
        </div>
    </div>
</div>

## Expert Systems (1969-1986) - AI Limitations

## Expert Systems (1969-1986) - AI Limitations

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <img src="https://upload.wikimedia.org/wikipedia/commons/1/13/Tree_of_Knowledge_System.png" alt="Knowledge Complexity" style="width: 90%; margin-top: 1.0em; background-color: #f6f8fa; padding: 10px; border-radius: 5px;">
            </div>
            <div class="footnote">The Tree of Knowledge System: Gregg Henriques, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons</div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <p>Extracting knowledge from human experts and encoding it into rules was difficult, time-consuming, and expensive</p>
            <br>
            <p>Systems could not reason beyond their pre-programmed knowledge and failed when confronted with unexpected situations</p>
            <br>
            <p>Adding more rules often led to rule interaction problems and combinatorial explosion</p>
            <br>
            <p>Updating knowledge bases as domains evolved required significant effort</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->