---
author: Christian Cabrera Jojoa
course_code: 25-udenar-ml-intro
department: Department of Computer Science and Technology
description: This lecture will emphasis on the importance of building ML-based systems
  with a purpose by focusing on the problem first. We will see the current status
  of ML applications, the adoption properties, and engineering mechanisms to ensure
  our ML projects align with the problems they are designed for.
email: chc79@cam.ac.uk
end_time: 12:00 am
hours: 4
institution: University of Cambridge
layout: lecture
lecture_code: problem-first
lecture_date: 24/05/2025
permalink: /teaching/25-udenar-ml-intro/problem-first/
position: Senior Research Associate and Affiliated Lecturer
session: 2
start_time: 10:00 am
title: The Problem First
visible: false
---

<link rel="stylesheet" href="/assets/css/slides.css">
<div class="lecture-resources">  
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/problem-first.html" target="_blank">[HTML Slides]</a>    
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/25-udenar-ml-intro/problem-first.ipynb" target="_blank">[Colab Notebook]</a>
    <a href="/teaching/25-udenar-ml-intro/">[Back to Course]</a>    
  </p>
</div>
  
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

# ML Definition
