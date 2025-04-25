---
marp: true
theme: default
paginate: true
header: "Session 1 - Artificial Intelligence and Machine Learning"
footer: ""
style: |
  :root {
    --primary-color: #00244A;
    --secondary-color: #0E73B8;
    --accent-color: #0E73B8;
    --text-color: #00244A;
    --background-color: #FFFFFF;
    --progress-color: #0E73B8;
  }

  html[data-theme='dark'] {
    --primary-color: #0E73B8;
    --secondary-color: #80FFF6;
    --accent-color: #0E73B8;
    --text-color: #FFFFFF;
    --background-color: #1E1E1E;
    --progress-color: #0E73B8;
  }

  .columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    align-items: start;
    margin: 1rem 0;
  }

  .rows {
    display: grid;
    grid-template-rows: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    align-items: start;
    margin: 1rem 0;
  }

  .column, .row {
    padding: 0.5rem;
    min-width: 0; /* Prevents overflow */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .column img, .row img {
    max-width: 100%;
    max-height: 300px;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin: 0.5rem auto;
  }

  .column p, .row p {
    margin: 0.5rem 0;
    text-align: center;
  }

  .column em, .row em {
    margin-top: 0.5rem;
    display: block;
    font-size: 0.9em;
    text-align: center;
  }

  section {
    padding-top: 60px; /* Add space for header */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    min-height: calc(100vh - 60px);
  }

  section > *:first-child {
    margin-top: 0;
  }

  h1, h2 {
    margin: 0;
    padding: 0;
    text-align: left;
  }

  h1 {
    font-size: 2em;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 1.5em;
    margin-bottom: 0.5rem;
  }

  html {
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  body {
    background-color: var(--background-color);
    color: var(--text-color);
  }

  section::before {
    font-size: 0.6em;
    content: attr(data-marpit-pagination) " / " attr(data-marpit-pagination-total);
    position: absolute;
    text-align: right;
    top: 96.2%;
    width: 100%;
    right: 0;
    left: -0.5em;
    color: var(--secondary-color);
  }

  section::after {
    display: none !important;
  }

  header {
    color: var(--text-color);
    font-size: 20px;
    padding: 10px;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--accent-color);
    z-index: 100;
  }

  section.lead h1 {
    margin-bottom: 10px;
  }

  section.lead p {
    font-size: 24px;
    margin: 5px 0;
    line-height: 1.2;
  }

  section.lead header {
    display: none;
  }

  section.lead.last-slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 100vh;
  }

  section.lead.last-slide h1 {
    margin-bottom: 20px;
  }

  section.lead.last-slide p {
    margin: 10px 0;
  }

---

<!-- _class: lead -->
# Artificial Intelligence and Machine Learning
<p><b>Christian Cabrera Jojoa</b></p>
<p>Senior Research Associate and Affiliated Lecturer</p>
<p>Department of Computer Science and Technology</p>
<p>University of Cambridge</p>
<p><a href="mailto:chc79@cam.ac.uk">chc79@cam.ac.uk</a></p>

---

# The Machine Learning Context


---

## Artificial Intelligence

<div class="columns">
<div class="column">

<p>"The field of Artificial Intelligence (AI) is concerned with <em>understanding and building intelligent entities</em>".</p>

<em>Stuart Russell and Peter Norvig, Artificial Intelligence: A Modern Approach (4th Edition)</em>

</div>
<div class="column">

<img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover">

</div>
</div>


---

## Artificial Intelligence - Intelligent Entities
<div class="rows">
  <div class="row">
    "The field of Artificial Intelligence (AI) is concerned with understanding and building intelligent entities."
  </div>
  <div class="row">
    <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover">
  </div>
  <div class="row">
    <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover">
  </div>
</div>


---

## Artificial Intelligence - Intelligent Entities
<div class="rows">
  <div class="row">
    <div class="columns">
        <div class="column">
            The field of Artificial Intelligence (AI) is concerned with understanding and building intelligent entities"
        </div>
        <div class="column">
            <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover">
        </div>
    </div>
  </div>
  <div class="row">
    <div class="columns">
        <div class="column">
            <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover">
        </div>
        <div class="column">
            The field of Artificial Intelligence (AI) is concerned with understanding and building intelligent entities"
        </div>
    </div>
  </div>
</div>


---

<!-- _class: lead last-slide -->
# Many Thanks!
<p><a href="mailto:chc79@cam.ac.uk">chc79@cam.ac.uk</a></p>
