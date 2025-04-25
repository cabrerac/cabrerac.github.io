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
    --primary-color: #FFFFFF;
    --secondary-color: #0E73B8;
    --accent-color: #0E73B8;
    --text-color: #FFFFFF;
    --background-color: #1E1E1E;
    --progress-color: #0E73B8;
  }

  html[data-theme='dark'] section,
  html[data-theme='dark'] section h1,
  html[data-theme='dark'] section h2,
  html[data-theme='dark'] .columns,
  html[data-theme='dark'] .rows,
  html[data-theme='dark'] .column,
  html[data-theme='dark'] .row,
  html[data-theme='dark'] p,
  html[data-theme='dark'] strong,
  html[data-theme='dark'] em {
    color: #FFFFFF !important;
  }

  section {
    padding-top: 60px; /* Add space for header */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    min-height: calc(100vh - 60px);
    color: var(--text-color);
  }

  /* Main title (h1) styling */
  section > h1 {
    text-align: left;
    font-size: 1.5em;
    font-weight: bold;
    margin: 0;
    padding: 0;
    padding-left: 0;
    color: var(--text-color);
  }

  /* Section title (h2) styling */
  section > h2 {
    position: absolute;
    top: 2cm;
    left: 1.5cm;
    right: 0;
    margin: 0;
    padding: 0;
    padding-left: 0;
    font-size: 1.5em;
    text-align: left;
    z-index: 1;
    color: var(--text-color);
  }

  /* Content spacing for sections with h2 titles */
  section:has(h2) > *:not(h2) {
    margin-top: 3.5cm;
  }

  /* Additional spacing for rows and columns layouts */
  section:has(.rows) > .rows,
  section:has(.columns) > .columns {
    margin-top: 2.5cm;
  }

  /* Spacing for nested rows and columns */
  .rows .rows,
  .columns .columns {
    margin-top: 2.5cm;
  }

  /* Code block styling */
  pre {
    background-color: var(--background-color);
    border: 1px solid var(--accent-color);
    border-radius: 4px;
    padding: 1em;
    margin: -0.5cm 0;
    max-width: 100%;
    height: calc(100vh - 3.5cm);
    box-sizing: border-box;
    white-space: pre-wrap;
    word-wrap: break-word;
    display: flex;
    flex-direction: column;
  }

  code {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.65em; /* Slightly smaller font to fit more content */
    line-height: 1.1;
    color: var(--text-color);
    display: block;
    width: 100%;
    height: 100%;
  }

  /* Ensure paragraphs after titles have proper spacing */
  section > p {
    margin-top: 1.5cm;
  }

  /* Syntax highlighting for code blocks */
  .hljs {
    background: transparent !important;
    padding: 0 !important;
    width: 100%;
    height: 100%;
  }

  /* Dark mode specific code styles */
  html[data-theme='dark'] pre {
    background-color: #2A2A2A !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
  }

  html[data-theme='dark'] code {
    color: #E0E0E0 !important;
  }

  .columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    align-items: center;
    margin: 1rem 0;
    color: var(--text-color);
  }

  .rows {
    display: grid;
    grid-template-rows: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    align-items: center;
    margin: 1rem 0;
    color: var(--text-color);
  }

  .column, .row {
    padding: 0.5rem;
    min-width: 0; /* Prevents overflow */
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: var(--text-color);
  }

  .column p, .row p {
    margin: 0;
    text-align: left;
    white-space: normal;
    line-height: 1.5;
    color: var(--text-color);
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

  /* Ensure code blocks in columns and rows work properly */
  .column pre, .row pre {
    height: 100%;
    margin: 0;
    padding: 0.5em;
  }

  .column code, .row code {
    font-size: 0.65em;
    line-height: 1.1;
  }

  /* Dark mode styles for code in columns and rows */
  html[data-theme='dark'] .column pre,
  html[data-theme='dark'] .row pre {
    background-color: #2A2A2A !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
  }

  html[data-theme='dark'] .column code,
  html[data-theme='dark'] .row code {
    color: #E0E0E0 !important;
  }

  /* Add styles for HTML elements */
  strong {
    font-weight: bold;
    display: inline;
    color: var(--text-color);
  }

  em {
    font-style: italic;
    display: inline;
    color: var(--text-color);
  }

  .footnote {
    font-size: 0.6em;
    color: var(--secondary-color);
    margin-top: 0;
    text-align: center;
    font-style: italic;
  }

  /* Override paragraph color in dark mode with more specific selectors */
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .column p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .row p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .columns p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .rows p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .column p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .row p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section div p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section span p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .column > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .row > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .columns > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .rows > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section div > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section span > p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p strong,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p em,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .column p strong,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .column p em,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .row p strong,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section .row p em,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p * {
    color: #FFFFFF !important;
  }

  /* Force all text in dark mode to be white */
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section * {
    color: #FFFFFF !important;
  }

  /* Override any inline styles that might be setting text color */
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section [style*="color"],
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section [style*="text-align"],
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section [style*="display"],
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section [style*="align-items"] {
    color: #FFFFFF !important;
  }

  /* Specific override for text within paragraphs */
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p * {
    color: #FFFFFF !important;
  }

  /* Override the root text color variable in dark mode */
  html[data-theme='dark'] {
    --text-color: #FFFFFF !important;
  }

  /* Force all text in dark mode sections */
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section *,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section p *,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section div,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section div *,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section span,
  html[data-theme='dark'] div#\:\$p > svg > foreignObject > section span * {
    color: #FFFFFF !important;
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

<div class="columns" style="width: 100%; height: 100%;">
<div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">
<p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
</div>
<div class="column" style="width: 100%;">
<img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover" style="width: auto; height: auto;">
<div class="footnote">Stuart Russell and Peter Norvig, Artificial Intelligence: A Modern Approach (4th Edition)</div>
</div>
<div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">
<p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
</div>
</div>


---

## Artificial Intelligence - Intelligent Entities
<div class="rows" style="width: 100%; height: 500px;">
  <div class="row" style="text-align: left; display: flex; align-items: center; height: 200px;">
    <p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
  </div>
  <div class="row" style="height: 300px;">
    <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover" style="width: 400px; height: auto;">
    <div class="footnote">The most widely used textbook in AI education</div>
  </div>
</div>


---

## Artificial Intelligence - Intelligent Entities
<div class="rows" style="width: 100%; height: 100%;">
  <div class="row">
    <div class="columns" style="width: 100%; height: 100%;">
        <div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">
            <p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
        </div>
        <div class="column" style="width: 100%;">
            <p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
        </div>
    </div>
  </div>
  <div class="row">
    <div class="columns" style="width: 100%; height: 100%;">
        <div class="column" style="width: 100%;">
            <img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover" style="width: 100%; height: auto;">
        </div>
        <div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">
            <p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
        </div>
    </div>
  </div>
</div>


---

## Code Example

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

---

# Generate sample data
X, y = make_blobs(n_samples=100, centers=2, random_state=42)

---

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Sample ML Dataset")
plt.show()

``` 


---

## Code Example in Columns

<div class="columns" style="width: 100%; height: 100%;">
<div class="column" style="width: 100%;">
<img src="https://cabrerac.github.io/assets/media/images/ai-modern-approach.jpeg" alt="Artificial Intelligence: A Modern Approach book cover" style="width: auto; height: auto;">
<div class="footnote">Stuart Russell and Peter Norvig, Artificial Intelligence: A Modern Approach (4th Edition)</div>
</div>
<div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">
<p>The field of <strong>Artificial Intelligence</strong> (AI) is concerned with <em>understanding and building intelligent entities.</em></p>
</div>
<div class="column" style="text-align: left; display: flex; align-items: center; width: 100%;">

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

---

# Generate sample data
X, y = make_blobs(n_samples=100, centers=2, random_state=42)

---

# Plot the data
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.title("Sample ML Dataset")
plt.show()

```
</div>
</div>

---

<!-- _class: lead last-slide -->
# Many Thanks!
<p><a href="mailto:chc79@cam.ac.uk">chc79@cam.ac.uk</a></p>
