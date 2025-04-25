---
course_code: 25-udenar-ml-intro
title: Artificial Intelligence and Machine Learning
description: This lecture presents the Artificial Intelligence and Machine Learning concepts. Their definition, history, implications, and applications.
session: 1
start_time: TBD
end_time: TBD
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 10/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
visible: true
---

<!-- ALL: content that goes everywhere -->
<!-- RENDER: content that only goes to rendered markdown -->
<!-- SLIDES: content that only goes to slides -->
<!-- NOTEBOOK: content that only goes to notebook -->
<!-- RENDER+SLIDES: content that goes to both rendered markdown and slides -->
<!-- RENDER+NOTEBOOK: content that goes to both rendered markdown and notebook -->
<!-- SLIDES+NOTEBOOK: content that goes to both slides and notebook -->

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

<!-- SLIDES: -->

# The Machine Learning Context

{% include _snippets/ai-concept.md %}
