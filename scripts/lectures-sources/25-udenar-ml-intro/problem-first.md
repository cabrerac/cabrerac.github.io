---
course_code: 25-udenar-ml-intro
title: The Problem First
description: This lecture will emphasis on the importance of building ML-based systems with a purpose by focusing on the problem first. We will see the current status of ML applications, the adoption properties, and engineering mechanisms to ensure our ML projects align with the problems they are designed for.
session: 2
start_time: 10:00 am
end_time: 12:00 am
hours: 4
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Senior Research Associate and Affiliated Lecturer
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: problem-first
lecture_date: 24/05/2025
permalink: /teaching/25-udenar-ml-intro/problem-first/
visible: false
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

<!-- SLIDES: -->

# ML Today

<!-- end SLIDES: -->

{% include _snippets/ml-applications.md %}

<!-- SLIDES: -->

# ML Definition

<!-- end SLIDES: -->

{% include _snippets/ml-objective.md %}

<!-- SLIDES: -->

# Problem First

<!-- end SLIDES: -->