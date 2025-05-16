---
author: Christian Cabrera Jojoa
course_code: 25-udenar-ml-intro
department: Department of Computer Science and Technology
description: This lecture presents the Artificial Intelligence and Machine Learning
  concepts. Their definition, history, implications, and applications.
email: chc79@cam.ac.uk
end_time: 12:00 am
hours: 4
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 17/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
position: Senior Research Associate and Affiliated Lecturer
session: 1
start_time: 8:00 am
title: Artificial Intelligence and Machine Learning
visible: true
---

<link rel="stylesheet" href="/assets/css/slides.css">
<div class="lecture-resources">  
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.html" target="_blank">[HTML Slides]</a>    
    <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/25-udenar-ml-intro/ml-introduction.ipynb" target="_blank">[Colab Notebook]</a>
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

### Resources
- [Turing A. M. (1950). Computing Machinery and Intelligence](https://courses.cs.umbc.edu/471/papers/turing.pdf)
- [Lighthill J. (1972). Artificial Intelligence: A General Survey](https://www.chilton-computing.org.uk/inf/literature/reports/lighthill_report/p001.htm)
- [Feigenbaum E. A. (1980). Expert Systems in the 1980s](https://stacks.stanford.edu/file/druid:vf069sz9374/vf069sz9374.pdf)
- [Vol. 117, No. 1, Winter, 1988, Artificial Intelligence](https://www.jstor.org/stable/i20025133)
- Russell, S. and Norvig, P. (2010). Artificial Intelligence: A Modern Approach. Prentice Hall (3rd ed.)
- [Hart P. An Artificial Intelligence Odyssey: From the Research Lab to the Real World](https://ieeexplore.ieee.org/abstract/document/9423541)
- [Shumailov I. et. al. (2024). AI models collapse when trained on recursively generated data](https://www.nature.com/articles/s41586-024-07566-y)
- [Demmis Hassabis talk at Cambridge (2025)](https://www.youtube.com/watch?v=hHooQmmzG4k)
