---
course_code: 25-udenar-ml-intro
title: Artificial Intelligence and Machine Learning
description: This lecture presents the Artificial Intelligence and Machine Learning concepts. Their definition, history, implications, and applications.
session: 1
start_time: 8:00 am
end_time: 12:00 am
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 17/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
visible: true
---

<!-- ALL: content that goes everywhere -->
<!-- SLIDES: content that only goes to slides -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- SLIDES+RENDER: content that goes to both rendered markdown and slides -->
<!-- SLIDES+NOTEBOOK: content that goes to both slides and notebook -->
<!-- RENDER+NOTEBOOK: content that goes to both rendered markdown and notebook -->

<!-- RENDER: -->
<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {
        let pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }
    main();
</script>
<!-- end RENDER: -->

<!-- SLIDES: -->

# The ML Context

<!-- end SLIDES: -->

{% include _snippets/ai-concept.md %}

{% include _snippets/ai-foundations.md %}

{% include _snippets/ai-history.md %}

<!-- SLIDES: -->

# ML Today

<!-- end SLIDES: -->

{% include _snippets/ml-applications.md %}

{% include _snippets/ml-perception.md %}

<!-- SLIDES: -->

# ML Definition

<!-- end SLIDES: -->

{% include _snippets/ml-objective.md %}

<!--SLIDES: -->

## Conclusions

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Overview</h3>
            <ul>
                <li>ML Context</li>
                <li>AI History</li>
                <li>AI Perception</li>
                <li>AI Winters</li>
                <li>ML Today</li>
                <li>ML Applications, Promises, and Risks</li>
                <li>ML Perception</li>
                <li>ML Definition</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            </div>
        </div>
    </div>
</div>

## Conclusions

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Overview</h3>
            <ul>
                <li>ML Context</li>
                <li>AI History</li>
                <li>AI Perception</li>
                <li>AI Winters</li>
                <li>ML Today</li>
                <li>ML Applications, Promises, and Risks</li>
                <li>ML Perception</li>
                <li>ML Definition</li>
            </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
            <h3>Next Time</h3>
            <ul>
                <li>ML Adoption Process</li>
                <li>ML with Purpose</li>
                <li>ML and Socio-technical Systems</li>
                <li>Data-First</li>
                <li>Data Access</li>
            </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->

<!-- RENDER: -->

### Resources

<!-- end RENDER: -->

