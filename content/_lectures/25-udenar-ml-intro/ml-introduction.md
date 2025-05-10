---
author: Christian Cabrera Jojoa
course_code: 25-udenar-ml-intro
department: Department of Computer Science and Technology
description: This lecture presents the Artificial Intelligence and Machine Learning
  concepts. Their definition, history, implications, and applications.
email: chc79@cam.ac.uk
end_time: TBD
hours: 4
institution: University of Cambridge
layout: lecture
lecture_code: ml-introduction
lecture_date: 10/05/2025
permalink: /teaching/25-udenar-ml-intro/ml-introduction/
position: Senior Research Associate and Affiliated Lecturer
session: 1
start_time: TBD
title: Artificial Intelligence and Machine Learning
visible: true
---

<link rel="stylesheet" href="/assets/css/slides.css">

<script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
<script>
    async function main() {
        let pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'});
        await pyodide.loadPackage("numpy");
        await pyodide.loadPackage("matplotlib");
    }
    main();
</script>

<div class="lecture-resources">
  <p>
    <a href="/assets/slides/25-udenar-ml-intro/ml-introduction.pdf" target="_blank">[PDF Slides]</a>
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

<div> NOTEBOOK+RENDER TEST</div>

<div> RENDER+NOTEBOOK TEST</div>

## AI Foundations

## AI Foundations

<div class="word-cloud" style="width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px; padding: 20px;">
  <span style="font-size: 2em; color: #224466;">Philosophy</span>
  <span style="font-size: 1.8em; color: #0e73b8;">Mathematics</span>
  <span style="font-size: 1.6em; color: #224466;">Economics</span>
  <span style="font-size: 1.8em; color: #0e73b8;">Neuroscience</span>
  <span style="font-size: 1.6em; color: #224466;">Psychology</span>
  <span style="font-size: 1.8em; color: #0e73b8;">Computer Engineering</span>
  <span style="font-size: 1.6em; color: #224466;">Control Theory</span>
  <span style="font-size: 1.8em; color: #0e73b8;">Linguistics</span>
  <span style="font-size: 1.4em; color: #224466;">Mind-body problem</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Logic</span>
  <span style="font-size: 1.4em; color: #224466;">Reasoning</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Ethics</span>
  <span style="font-size: 1.4em; color: #224466;">Probability</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Statistics</span>
  <span style="font-size: 1.4em; color: #224466;">Optimization</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Graph theory</span>
  <span style="font-size: 1.4em; color: #224466;">Decision theory</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Game theory</span>
  <span style="font-size: 1.4em; color: #224466;">Neural networks</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Learning</span>
  <span style="font-size: 1.4em; color: #224466;">Cognition</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Memory</span>
  <span style="font-size: 1.4em; color: #224466;">Algorithms</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Systems</span>
  <span style="font-size: 1.4em; color: #224466;">Feedback</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Language</span>
  <span style="font-size: 1.4em; color: #224466;">NLP</span>
  <span style="font-size: 1.2em; color: #0e73b8;">Communication</span>
</div>

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Aristotle_Altemps_Inv8575.jpg" alt="Aristotle" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Aristotle (384–322 BC)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/7d/Madrid_-_Ciudad_Universitaria%2C_Monumento_a_Muhammad_al-Juarismi_%28cropped%29.jpg" alt="Al-Khwarizmi" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Al-Khwarizmi (780 - 850 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style>

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/16/Francisco_Ribalta_-_Ramon_Llull_-_Google_Art_Project.jpg" alt="Ramon Llull" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Ramon Llull (1232 - 1316 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Christoph_Bernhard_Francke_-_Bildnis_des_Philosophen_Leibniz_%28ca._1695%29.jpg" alt="Gottfried Leibniz" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Gottfried Leibniz (1646 - 1716 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style>

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/Thomas_Bayes.gif" alt="Thomas Bayes" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Thomas Bayes (1701 - 1761 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Carl_Friedrich_Gauss_1840_by_Jensen.jpg" alt="Carl Friedrich Gauss" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Carl Friedrich Gauss (1777 - 1855 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style> 

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/Charles_Babbage_-_1860.jpg" alt="Charles Babbage" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Charles Babbage (1791 - 1871 AD)
    </div>
  </div>

<div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/f9/Ada_Byron_daguerreotype_by_Antoine_Claudet_1843_or_1850_-_cropped_%28cropped%29.png" alt="Ada Lovelace" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Ada Lovelace (1815 - 1852 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Portrait_of_George_Boole.png" alt="George Boole" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      George Boole (1815 - 1864 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style> 

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/79/Hilbert.jpg" alt="David Hilbert" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      David Hilbert (1862 - 1943 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/71/Bertrand_Russell_smoking_in_1936.jpg" alt="Bertrand Russell" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Bertrand Russell (1872 - 1970 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Alan_Turing_%281951%29.jpg" alt="Alan Turing" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Alan Turing (1912 - 1954 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style> 

## AI Foundations

<div class="photo-collage" style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
">
  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Aristotle_Altemps_Inv8575.jpg" alt="Aristotle" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Aristotle (384–322 BC)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/7d/Madrid_-_Ciudad_Universitaria%2C_Monumento_a_Muhammad_al-Juarismi_%28cropped%29.jpg" alt="Al-Khwarizmi" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Al-Khwarizmi (780 - 850 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/16/Francisco_Ribalta_-_Ramon_Llull_-_Google_Art_Project.jpg" alt="Ramon Llull" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Ramon Llull (1232 - 1316 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/8/8d/Christoph_Bernhard_Francke_-_Bildnis_des_Philosophen_Leibniz_%28ca._1695%29.jpg" alt="Gottfried Leibniz" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Gottfried Leibniz (1646 - 1716 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/d/d4/Thomas_Bayes.gif" alt="Thomas Bayes" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Thomas Bayes (1701 - 1761 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Carl_Friedrich_Gauss_1840_by_Jensen.jpg" alt="Carl Friedrich Gauss" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Carl Friedrich Gauss (1777 - 1855 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/Charles_Babbage_-_1860.jpg" alt="Charles Babbage" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Charles Babbage (1791 - 1871 AD)
    </div>
  </div>

<div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/f9/Ada_Byron_daguerreotype_by_Antoine_Claudet_1843_or_1850_-_cropped_%28cropped%29.png" alt="Ada Lovelace" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Ada Lovelace (1815 - 1852 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Portrait_of_George_Boole.png" alt="George Boole" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      George Boole (1815 - 1864 AD)
    </div>
  </div>

<div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/79/Hilbert.jpg" alt="David Hilbert" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      David Hilbert (1862 - 1943 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/7/71/Bertrand_Russell_smoking_in_1936.jpg" alt="Bertrand Russell" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Bertrand Russell (1872 - 1970 AD)
    </div>
  </div>

  <div class="photo-item" style="
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
  ">
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/f8/Alan_Turing_%281951%29.jpg" alt="Alan Turing" style="
      width: 100%;
      height: 100%;
      object-fit: contain;
      aspect-ratio: 1;
      background-color: var(--background-color);
    ">
    <div class="photo-caption" style="
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: var(--primary-color);
      color: var(--background-color);
      padding: 10px;
      transform: translateY(0);
      transition: transform 0.3s ease;
      opacity: 0.9;
      font-weight: 500;
      font-size: 0.5em;
    ">
      Alan Turing (1912 - 1954 AD)
    </div>
  </div>
</div>

<style>
.photo-item:hover {
  transform: scale(1.05);
}

.photo-item:hover .photo-caption {
  transform: translateY(0);
}

img[src=""], img[src="#"] {
  display: none;
}
</style> 

## AI Foundations

<div class="columns" style="width: 100%; height: 100%; display: flex; flex-direction: row; align-items: center; justify-content: space-between;">
  <div class="column vertical-middle text-center" style="width: 35%;">
    <img src="https://cabrerac.github.io/assets/media/images/enigma.jpg" alt="Enigma Machine, Bletchley Park" style="height: auto; max-width: 100%;">
    <div class="footnote">Enigma Machine, Bletchley Park</div>
  </div>
  <div class="column vertical-middle text-center" style="width: 35%;">
    <img src="https://cabrerac.github.io/assets/media/images/turing.jpg" alt="Statue of Alan Turing, Bletchley Park" style="height: auto; max-width: 100%;">
    <div class="footnote">Statue of Alan Turing, Bletchley Park 
    (Stephen Kettle, 2007)</div>
  </div>
  <div class="column vertical-middle text-center" style="width: 30%;">
    <video controls autoplay loop muted style="max-width: 100%; height: 90%; transform: rotate(0deg); aspect-ratio: 9/16;">
      <source src="https://cabrerac.github.io/assets/media/videos/bombe.mp4" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <div class="footnote">The Bombe, Bletchley Park (Alan Turing, 1939)</div>
  </div>
</div>

## Early AI Approaches (1943-1969) - Searching Algorithms

<div class="rows" style="height: 100%">
    <div class="row" style="height: 20%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 33%">
                <strong>Problem Definition</strong>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <strong>Formalisation</strong>
            </div>
            <div class="column vertical-middle text-center" style="width: 33%">
                <strong>Approaches</strong>
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
                - Breadth-First Search (BFS)
                - Depth-First Search (DFS)
                - A* Algorithm (1968)
            </div>
        </div>
    </div>
</div>

# Early AI Approaches (1943-1969)

## The Artificial Neuron (1943)

The first mathematical model of a neuron was proposed by McCulloch and Pitts in 1943. This model laid the foundation for artificial neural networks.

```python
class McCullochPittsNeuron:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
    
    def activate(self, inputs):
        # Sum weighted inputs
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        # Apply threshold activation
        return 1 if weighted_sum >= self.threshold else 0

# Example usage
neuron = McCullochPittsNeuron(weights=[1, 1], threshold=1.5)
inputs = [1, 1]
output = neuron.activate(inputs)
print(f"Input: {inputs}, Output: {output}")
```

## Hebbian Learning (1949)

Donald Hebb proposed a learning rule that became fundamental to neural networks. The rule states that neurons that fire together, wire together.

```python
class HebbianLearning:
    def __init__(self, input_size):
        self.weights = [0] * input_size
    
    def update(self, inputs, output):
        # Hebbian learning rule: Δw = η * x * y
        learning_rate = 0.1
        for i in range(len(self.weights)):
            self.weights[i] += learning_rate * inputs[i] * output
    
    def predict(self, inputs):
        return 1 if sum(w * x for w, x in zip(self.weights, inputs)) > 0 else 0

# Example usage
hebb = HebbianLearning(input_size=2)
training_data = [([1, 1], 1), ([1, -1], -1), ([-1, 1], -1), ([-1, -1], 1)]
for inputs, target in training_data:
    hebb.update(inputs, target)
```

## The Perceptron (1957)

Frank Rosenblatt's Perceptron was the first artificial neural network that could learn from examples.

```python
class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        self.weights = [0] * input_size
        self.learning_rate = learning_rate
    
    def predict(self, inputs):
        # Calculate weighted sum
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))
        # Apply step activation
        return 1 if weighted_sum > 0 else 0
    
    def train(self, inputs, target):
        # Make prediction
        prediction = self.predict(inputs)
        # Calculate error
        error = target - prediction
        # Update weights
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * error * inputs[i]

# Example: Training a perceptron to learn AND gate
perceptron = Perceptron(input_size=2)
training_data = [
    ([1, 1], 1),
    ([1, 0], 0),
    ([0, 1], 0),
    ([0, 0], 0)
]

# Train for 10 epochs
for _ in range(10):
    for inputs, target in training_data:
        perceptron.train(inputs, target)
```

## Early Search Algorithms

Search algorithms were fundamental to early AI development. Here are implementations of key algorithms:

```python
from collections import deque
import heapq

class SearchAlgorithms:
    @staticmethod
    def bfs(graph, start, goal):
        queue = deque([(start, [start])])
        visited = set()
        
        while queue:
            (vertex, path) = queue.popleft()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        queue.append((next_vertex, path + [next_vertex]))
        return None

    @staticmethod
    def dfs(graph, start, goal):
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        stack.append((next_vertex, path + [next_vertex]))
        return None

    @staticmethod
    def a_star(graph, start, goal, heuristic):
        frontier = []
        heapq.heappush(frontier, (0, start, [start]))
        visited = set()
        
        while frontier:
            _, vertex, path = heapq.heappop(frontier)
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for next_vertex in graph[vertex]:
                    if next_vertex not in visited:
                        new_path = path + [next_vertex]
                        priority = len(new_path) + heuristic(next_vertex, goal)
                        heapq.heappush(frontier, (priority, next_vertex, new_path))
        return None

# Example usage
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['G'],
    'E': ['G'],
    'F': ['G'],
    'G': []
}

def manhattan_distance(a, b):
    return abs(ord(a) - ord(b))

# Test BFS
bfs_path = SearchAlgorithms.bfs(graph, 'A', 'G')
print(f"BFS path: {bfs_path}")

# Test DFS
dfs_path = SearchAlgorithms.dfs(graph, 'A', 'G')
print(f"DFS path: {dfs_path}")

# Test A*
a_star_path = SearchAlgorithms.a_star(graph, 'A', 'G', manhattan_distance)
print(f"A* path: {a_star_path}")
```

## General Problem Solver (1957)

Newell and Simon's GPS was one of the first AI programs designed to solve general problems.

```python
class GeneralProblemSolver:
    def __init__(self):
        self.operators = []
        self.differences = {}
    
    def add_operator(self, name, preconditions, effects):
        self.operators.append({
            'name': name,
            'preconditions': preconditions,
            'effects': effects
        })
    
    def find_difference(self, current_state, goal_state):
        for key in goal_state:
            if current_state.get(key) != goal_state.get(key):
                return key
        return None
    
    def apply_operator(self, state, operator):
        # Check if preconditions are met
        for precondition in operator['preconditions']:
            if state.get(precondition) != operator['preconditions'][precondition]:
                return None
        
        # Apply effects
        new_state = state.copy()
        for effect in operator['effects']:
            new_state[effect] = operator['effects'][effect]
        return new_state
    
    def solve(self, initial_state, goal_state):
        current_state = initial_state.copy()
        plan = []
        
        while current_state != goal_state:
            difference = self.find_difference(current_state, goal_state)
            if not difference:
                break
                
            # Find applicable operator
            for operator in self.operators:
                if difference in operator['effects']:
                    new_state = self.apply_operator(current_state, operator)
                    if new_state:
                        current_state = new_state
                        plan.append(operator['name'])
                        break
        
        return plan

# Example: Tower of Hanoi problem
gps = GeneralProblemSolver()
gps.add_operator('move_disk', 
                 {'disk': 'small', 'from': 'A', 'to': 'B'},
                 {'disk': 'small', 'from': 'B', 'to': 'C'})

initial_state = {'disk': 'small', 'from': 'A', 'to': 'A'}
goal_state = {'disk': 'small', 'from': 'C', 'to': 'C'}
solution = gps.solve(initial_state, goal_state)
```

## The DENDRAL System (1969)

The DENDRAL system was an early expert system for chemical analysis.

```python
class DendralSystem:
    def __init__(self):
        self.rules = []
        self.mass_spectrum = {}
    
    def add_rule(self, pattern, conclusion):
        self.rules.append({
            'pattern': pattern,
            'conclusion': conclusion
        })
    
    def analyze_spectrum(self, spectrum):
        conclusions = []
        for rule in self.rules:
            if self._match_pattern(spectrum, rule['pattern']):
                conclusions.append(rule['conclusion'])
        return conclusions
    
    def _match_pattern(self, spectrum, pattern):
        # Simplified pattern matching
        for mass, intensity in pattern.items():
            if mass not in spectrum or abs(spectrum[mass] - intensity) > 0.1:
                return False
        return True

# Example usage
dendral = DendralSystem()
# Add rules for chemical fragment identification
dendral.add_rule(
    pattern={15: 1.0, 29: 0.8, 43: 0.6},
    conclusion="Methyl group present"
)
dendral.add_rule(
    pattern={17: 1.0, 31: 0.9},
    conclusion="Hydroxyl group present"
)

# Analyze a mass spectrum
spectrum = {15: 1.0, 29: 0.8, 43: 0.6, 17: 1.0, 31: 0.9}
conclusions = dendral.analyze_spectrum(spectrum)
```
<!-- end RENDER+NOTEBOOK-->

<!--
## Key Concepts and Methods

1. **Neural Networks**
   - McCulloch-Pitts Neuron: Binary threshold unit
   - Hebbian Learning: Weight updates based on correlation
   - Perceptron: First learnable neural network

2. **Search Algorithms**
   - Breadth-First Search: Complete but memory-intensive
   - Depth-First Search: Memory-efficient but not complete
   - A* Algorithm: Optimal path finding with heuristics

3. **Symbolic AI**
   - General Problem Solver: Means-ends analysis
   - Rule-based systems: Expert systems like DENDRAL

4. **Learning Methods**
   - Supervised Learning: Perceptron training
   - Unsupervised Learning: Hebbian learning
   - Rule-based Learning: Expert system rules

5. **Problem-Solving Approaches**
   - State-space search
   - Pattern matching
   - Rule-based reasoning

These early approaches laid the foundation for modern AI and machine learning. They demonstrated both the potential and limitations of different AI paradigms, leading to the development of more sophisticated methods in later years.-->


<!-- SLIDES+RENDER: -->

## AI History - Expert Systems (1969 - 1986)
<div class="rows" style="width: 100%; height: 100%">
  <div class = "row"  style="width: 100%; height:100%; display: flex; align-items: center;">
    <style>
      :root {
        --conceptual-color: #4a90e2;  /* Blue for conceptual/foundational events */
        --symbolic-color: #50c878;    /* Green for symbolic AI events */
        --connectionist-color: #ffa500; /* Orange for connectionist/neural events */
        --critical-color: #9b59b6;    /* Purple for critical/reflective reports */
      }
    </style>
    <div class="timeline-container">
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
      <line x1="25" y1="50%" x2="1250" y2="50%" stroke="var(--secondary-color)" stroke-width="2"/>
      <line x1="25" y1="48%" x2="25" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="25" y="55%" text-anchor="middle">1940</text>
      <line x1="38.5" y1="49%" x2="38.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="52" y1="49%" x2="52" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="65.5" y1="49%" x2="65.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="79" y1="49%" x2="79" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="92.5" y1="49%" x2="92.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="106" y1="49%" x2="106" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="119.5" y1="49%" x2="119.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="133" y1="49%" x2="133" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="146.5" y1="49%" x2="146.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="160" y1="48%" x2="160" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="160" y="55%" text-anchor="middle">1950</text>
      <line x1="173.5" y1="49%" x2="173.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="187" y1="49%" x2="187" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="200.5" y1="49%" x2="200.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="214" y1="49%" x2="214" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="227.5" y1="49%" x2="227.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="241" y1="49%" x2="241" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="254.5" y1="49%" x2="254.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="268" y1="49%" x2="268" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="281.5" y1="49%" x2="281.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="295" y1="48%" x2="295" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="295" y="55%" text-anchor="middle">1960</text>
      <line x1="308.5" y1="49%" x2="308.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="322" y1="49%" x2="322" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="335.5" y1="49%" x2="335.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="349" y1="49%" x2="349" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="362.5" y1="49%" x2="362.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="376" y1="49%" x2="376" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="389.5" y1="49%" x2="389.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="403" y1="49%" x2="403" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="416.5" y1="49%" x2="416.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="430" y1="48%" x2="430" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="430" y="55%" text-anchor="middle">1970</text>
      <line x1="443.5" y1="49%" x2="443.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="457" y1="49%" x2="457" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="470.5" y1="49%" x2="470.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="484" y1="49%" x2="484" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="497.5" y1="49%" x2="497.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="511" y1="49%" x2="511" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="524.5" y1="49%" x2="524.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="538" y1="49%" x2="538" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="551.5" y1="49%" x2="551.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="565" y1="48%" x2="565" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="565" y="55%" text-anchor="middle">1980</text>
      <line x1="578.5" y1="49%" x2="578.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="592" y1="49%" x2="592" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="605.5" y1="49%" x2="605.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="619" y1="49%" x2="619" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="632.5" y1="49%" x2="632.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="646" y1="49%" x2="646" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="659.5" y1="49%" x2="659.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="673" y1="49%" x2="673" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="686.5" y1="49%" x2="686.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="700" y1="48%" x2="700" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="700" y="55%" text-anchor="middle">1990</text>
      <line x1="713.5" y1="49%" x2="713.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="727" y1="49%" x2="727" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="740.5" y1="49%" x2="740.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="754" y1="49%" x2="754" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="767.5" y1="49%" x2="767.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="781" y1="49%" x2="781" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="794.5" y1="49%" x2="794.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="808" y1="49%" x2="808" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="821.5" y1="49%" x2="821.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="835" y1="48%" x2="835" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="835" y="55%" text-anchor="middle">2000</text>
      <line x1="848.5" y1="49%" x2="848.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="862" y1="49%" x2="862" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="875.5" y1="49%" x2="875.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="889" y1="49%" x2="889" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="902.5" y1="49%" x2="902.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="916" y1="49%" x2="916" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="929.5" y1="49%" x2="929.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="943" y1="49%" x2="943" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="956.5" y1="49%" x2="956.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="970" y1="48%" x2="970" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="970" y="55%" text-anchor="middle">2010</text>
      <line x1="983.5" y1="49%" x2="983.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="997" y1="49%" x2="997" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1010.5" y1="49%" x2="1010.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1024" y1="49%" x2="1024" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1037.5" y1="49%" x2="1037.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1051" y1="49%" x2="1051" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1064.5" y1="49%" x2="1064.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1078" y1="49%" x2="1078" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1091.5" y1="49%" x2="1091.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1105" y1="48%" x2="1105" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="1105" y="55%" text-anchor="middle">2020</text>
      <line x1="1118.5" y1="49%" x2="1118.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1132" y1="49%" x2="1132" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1145.5" y1="49%" x2="1145.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1159" y1="49%" x2="1159" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1172.5" y1="49%" x2="1172.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1186" y1="49%" x2="1186" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1199.5" y1="49%" x2="1199.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1213" y1="49%" x2="1213" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1226.5" y1="49%" x2="1226.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1240" y1="48%" x2="1240" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="1235" y="55%" text-anchor="middle">2030</text>
      <!-- 1943 Event - Connectionist -->
      <line x1="65.5" y1="50%" x2="65.5" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="65.5" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="75.0" y="38%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="75" dy="0">Artificial Neuron</tspan>
        <tspan x="75" dy="15">(McCulloch</tspan>
        <tspan x="75" dy="15">& Pitts, 1943)</tspan>
      </text>
      <!-- 1948 Event - Conceptual -->
      <line x1="133" y1="50%" x2="133" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="133" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="100" y="20%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="100" dy="0">Information Theory</tspan>
        <tspan x="100" dy="15">(Shannon, 1948)</tspan>
      </text>
      <!-- 1948 Event - Conceptual -->
      <line x1="133" y1="50%" x2="133" y2="65%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="133" cy="65%" r="1" fill="var(--secondary-color)"/>
      <text x="100" y="68%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="100" dy="0">Cybernetics</tspan>
        <tspan x="100" dy="15">(Wiener, 1948)</tspan>
      </text>
      <!-- 1949 Event - Connectionist -->
      <line x1="146.5" y1="50%" x2="146.5" y2="75%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="146.5" cy="75%" r="1" fill="var(--secondary-color)"/>
      <text x="146.5" y="78%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="146.5" dy="0">Updating Rule</tspan>
        <tspan x="146.5" dy="15">(Hebbian, 1949)</tspan>
      </text>
      <!-- 1950 Event - Conceptual -->
      <line x1="160" y1="50%" x2="160" y2="15%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="160" cy="15%" r="1" fill="var(--secondary-color)"/>
      <text x="160" y="10%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="160" dy="0">Computing Machinery and Intelligence</tspan>
        <tspan x="160" dy="15">(Turing, 1950)</tspan>
      </text>
      <!-- 1951 Event - Connectionist -->
      <line x1="173.5" y1="50%" x2="173.5" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="173.5" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="205" y="20%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="205" dy="0">SNARC</tspan>
        <tspan x="205" dy="15">(Minsky, 1951)</tspan>
      </text>
      <!-- 1956 Event - Conceptual -->
      <line x1="241" y1="50%" x2="241" y2="90%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="241" cy="90%" r="1" fill="var(--secondary-color)"/>
      <text x="241" y="93%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="241" dy="0">AI Term</tspan>
        <tspan x="241" dy="15">(Dartmouth Workshop, 1956)</tspan>
      </text>
      <!-- 1957 Event - Symbolic -->
      <line x1="254.5" y1="50%" x2="254.5" y2="40%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="254.5" cy="40%" r="1" fill="var(--secondary-color)"/>
      <text x="230" y="35%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="230" dy="0">GPS (Newell &</tspan>
        <tspan x="230" dy="15">Simon, 1957)</tspan>
      </text>
      <!-- 1958 Event - Symbolic -->
      <line x1="268" y1="50%" x2="268" y2="83%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="268" cy="83%" r="1" fill="var(--secondary-color)"/>
      <text x="300" y="86%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="300" dy="0">Advice Taker</tspan>
        <tspan x="300" dy="15">(McCharty, 1958)</tspan>
      </text>
      <!-- 1960 Event - Connectionist -->
      <line x1="295" y1="50%" x2="295" y2="30%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="295" cy="30%" r="1" fill="var(--secondary-color)"/>
      <text x="320" y="25%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="315" dy="0">Back-Propagation</tspan>
        <tspan x="315" dy="15">(Kelley, 1960)</tspan>
      </text>
      <!-- 1962 Event - Connectionist -->
      <line x1="322" y1="50%" x2="322" y2="73%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="322" cy="73%" r="1" fill="var(--secondary-color)"/>
      <text x="330" y="76%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="330" dy="0">Perceptrons</tspan>
        <tspan x="330" dy="15">(Rosenblant, 1962)</tspan>
      </text>
      <!-- 1966 Event - Symbolic -->
      <line x1="376" y1="50%" x2="376" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="376" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="376" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="376" dy="0">ELIZA</tspan>
        <tspan x="376" dy="15">(MIT, 1966)</tspan>
      </text>
      <!-- 1969 Event - Symbolic -->
      <line x1="416.5" y1="50%" x2="416.5" y2="20%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="416.5" cy="20%" r="1" fill="var(--secondary-color)"/>
      <text x="416.5" y="15%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="416.5" dy="0">The DENDRAL</tspan>
        <tspan x="416.5" dy="15">(Buchanan, 1969)</tspan>
      </text>
      <!-- 1972 Event - Symbolic -->
      <line x1="457" y1="50%" x2="457" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="457" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="445" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="445" dy="0">PROLOG</tspan>
        <tspan x="445" dy="15">(1972)</tspan>
      </text>
      <!-- 1972 Event - Symbolic -->
      <line x1="457" y1="50%" x2="457" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="457" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="465" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="465" dy="0">MYCIN</tspan>
        <tspan x="465" dy="15">(Stanford, 1972)</tspan>
      </text>
      <!-- 1975 Event - Symbolic -->
      <line x1="497.5" y1="50%" x2="497.5" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="497.5" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="505" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="505" dy="0">FRAMES</tspan>
        <tspan x="505" dy="15">(1975)</tspan>
      </text>
      <!-- 1982 Event - Connectionist -->
      <line x1="592" y1="50%" x2="592" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="592" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="592" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="592" dy="0">Hopfield net</tspan>
        <tspan x="592" dy="15">(1982)</tspan>
      </text>
      <!-- 1982 Event - Symbolic -->
      <line x1="592" y1="50%" x2="592" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="592" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="592" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="592" dy="0">R1</tspan>
        <tspan x="592" dy="15">(McDermott, 1982)</tspan>
      </text>
      <!-- 1986 Event - Connectionist -->
      <line x1="646" y1="50%" x2="646" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="646" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="646" y="17%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="646" dy="0">Parallel Distributed Processing</tspan>
        <tspan x="646" dy="15">(Rumerlhart &</tspan>
        <tspan x="646" dy="17">McClelland, 1986)</tspan>
      </text>
    </svg>
</div>
  </div>
</div>

## AI History - The Return of Neural Networks (1987 - present)
<div class="rows" style="width: 100%; height: 100%">
  <div class = "row"  style="width: 100%; height:100%; display: flex; align-items: center;">
    <style>
      :root {
        --conceptual-color: #4a90e2;  /* Blue for conceptual/foundational events */
        --symbolic-color: #50c878;    /* Green for symbolic AI events */
        --connectionist-color: #ffa500; /* Orange for connectionist/neural events */
        --critical-color: #9b59b6;    /* Purple for critical/reflective reports */
      }
    </style>
    <div class="timeline-container">
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
      <line x1="25" y1="50%" x2="1250" y2="50%" stroke="var(--secondary-color)" stroke-width="2"/>
      <line x1="25" y1="48%" x2="25" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="25" y="55%" text-anchor="middle">1940</text>
      <line x1="38.5" y1="49%" x2="38.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="52" y1="49%" x2="52" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="65.5" y1="49%" x2="65.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="79" y1="49%" x2="79" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="92.5" y1="49%" x2="92.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="106" y1="49%" x2="106" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="119.5" y1="49%" x2="119.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="133" y1="49%" x2="133" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="146.5" y1="49%" x2="146.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="160" y1="48%" x2="160" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="160" y="55%" text-anchor="middle">1950</text>
      <line x1="173.5" y1="49%" x2="173.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="187" y1="49%" x2="187" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="200.5" y1="49%" x2="200.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="214" y1="49%" x2="214" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="227.5" y1="49%" x2="227.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="241" y1="49%" x2="241" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="254.5" y1="49%" x2="254.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="268" y1="49%" x2="268" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="281.5" y1="49%" x2="281.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="295" y1="48%" x2="295" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="295" y="55%" text-anchor="middle">1960</text>
      <line x1="308.5" y1="49%" x2="308.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="322" y1="49%" x2="322" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="335.5" y1="49%" x2="335.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="349" y1="49%" x2="349" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="362.5" y1="49%" x2="362.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="376" y1="49%" x2="376" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="389.5" y1="49%" x2="389.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="403" y1="49%" x2="403" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="416.5" y1="49%" x2="416.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="430" y1="48%" x2="430" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="430" y="55%" text-anchor="middle">1970</text>
      <line x1="443.5" y1="49%" x2="443.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="457" y1="49%" x2="457" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="470.5" y1="49%" x2="470.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="484" y1="49%" x2="484" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="497.5" y1="49%" x2="497.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="511" y1="49%" x2="511" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="524.5" y1="49%" x2="524.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="538" y1="49%" x2="538" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="551.5" y1="49%" x2="551.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="565" y1="48%" x2="565" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="565" y="55%" text-anchor="middle">1980</text>
      <line x1="578.5" y1="49%" x2="578.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="592" y1="49%" x2="592" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="605.5" y1="49%" x2="605.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="619" y1="49%" x2="619" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="632.5" y1="49%" x2="632.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="646" y1="49%" x2="646" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="659.5" y1="49%" x2="659.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="673" y1="49%" x2="673" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="686.5" y1="49%" x2="686.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="700" y1="48%" x2="700" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="700" y="55%" text-anchor="middle">1990</text>
      <line x1="713.5" y1="49%" x2="713.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="727" y1="49%" x2="727" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="740.5" y1="49%" x2="740.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="754" y1="49%" x2="754" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="767.5" y1="49%" x2="767.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="781" y1="49%" x2="781" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="794.5" y1="49%" x2="794.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="808" y1="49%" x2="808" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="821.5" y1="49%" x2="821.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="835" y1="48%" x2="835" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="835" y="55%" text-anchor="middle">2000</text>
      <line x1="848.5" y1="49%" x2="848.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="862" y1="49%" x2="862" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="875.5" y1="49%" x2="875.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="889" y1="49%" x2="889" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="902.5" y1="49%" x2="902.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="916" y1="49%" x2="916" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="929.5" y1="49%" x2="929.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="943" y1="49%" x2="943" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="956.5" y1="49%" x2="956.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="970" y1="48%" x2="970" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="970" y="55%" text-anchor="middle">2010</text>
      <line x1="983.5" y1="49%" x2="983.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="997" y1="49%" x2="997" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1010.5" y1="49%" x2="1010.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1024" y1="49%" x2="1024" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1037.5" y1="49%" x2="1037.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1051" y1="49%" x2="1051" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1064.5" y1="49%" x2="1064.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1078" y1="49%" x2="1078" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1091.5" y1="49%" x2="1091.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1105" y1="48%" x2="1105" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="1105" y="55%" text-anchor="middle">2020</text>
      <line x1="1118.5" y1="49%" x2="1118.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1132" y1="49%" x2="1132" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1145.5" y1="49%" x2="1145.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1159" y1="49%" x2="1159" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1172.5" y1="49%" x2="1172.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1186" y1="49%" x2="1186" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1199.5" y1="49%" x2="1199.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1213" y1="49%" x2="1213" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1226.5" y1="49%" x2="1226.5" y2="51%" stroke="var(--secondary-color)" stroke-width="1"/>
      <line x1="1240" y1="48%" x2="1240" y2="52%" stroke="var(--secondary-color)" stroke-width="1"/>
      <text x="1235" y="55%" text-anchor="middle">2030</text>
      <!-- 1943 Event - Connectionist -->
      <line x1="65.5" y1="50%" x2="65.5" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="65.5" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="75.0" y="38%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="75" dy="0">Artificial Neuron</tspan>
        <tspan x="75" dy="15">(McCulloch</tspan>
        <tspan x="75" dy="15">& Pitts, 1943)</tspan>
      </text>
      <!-- 1948 Event - Conceptual -->
      <line x1="133" y1="50%" x2="133" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="133" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="100" y="20%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="100" dy="0">Information Theory</tspan>
        <tspan x="100" dy="15">(Shannon, 1948)</tspan>
      </text>
      <!-- 1948 Event - Conceptual -->
      <line x1="133" y1="50%" x2="133" y2="65%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="133" cy="65%" r="1" fill="var(--secondary-color)"/>
      <text x="100" y="68%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="100" dy="0">Cybernetics</tspan>
        <tspan x="100" dy="15">(Wiener, 1948)</tspan>
      </text>
      <!-- 1949 Event - Connectionist -->
      <line x1="146.5" y1="50%" x2="146.5" y2="75%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="146.5" cy="75%" r="1" fill="var(--secondary-color)"/>
      <text x="146.5" y="78%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="146.5" dy="0">Updating Rule</tspan>
        <tspan x="146.5" dy="15">(Hebbian, 1949)</tspan>
      </text>
      <!-- 1950 Event - Conceptual -->
      <line x1="160" y1="50%" x2="160" y2="15%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="160" cy="15%" r="1" fill="var(--secondary-color)"/>
      <text x="160" y="10%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="160" dy="0">Computing Machinery and Intelligence</tspan>
        <tspan x="160" dy="15">(Turing, 1950)</tspan>
      </text>
      <!-- 1951 Event - Connectionist -->
      <line x1="173.5" y1="50%" x2="173.5" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="173.5" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="205" y="20%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="205" dy="0">SNARC</tspan>
        <tspan x="205" dy="15">(Minsky, 1951)</tspan>
      </text>
      <!-- 1956 Event - Conceptual -->
      <line x1="241" y1="50%" x2="241" y2="90%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="241" cy="90%" r="1" fill="var(--secondary-color)"/>
      <text x="241" y="93%" text-anchor="middle" style="font-size: 12px; fill: var(--conceptual-color);">
        <tspan x="241" dy="0">AI Term</tspan>
        <tspan x="241" dy="15">(Dartmouth Workshop, 1956)</tspan>
      </text>
      <!-- 1957 Event - Symbolic -->
      <line x1="254.5" y1="50%" x2="254.5" y2="40%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="254.5" cy="40%" r="1" fill="var(--secondary-color)"/>
      <text x="230" y="35%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="230" dy="0">GPS (Newell &</tspan>
        <tspan x="230" dy="15">Simon, 1957)</tspan>
      </text>
      <!-- 1958 Event - Symbolic -->
      <line x1="268" y1="50%" x2="268" y2="83%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="268" cy="83%" r="1" fill="var(--secondary-color)"/>
      <text x="300" y="86%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="300" dy="0">Advice Taker</tspan>
        <tspan x="300" dy="15">(McCharty, 1958)</tspan>
      </text>
      <!-- 1960 Event - Connectionist -->
      <line x1="295" y1="50%" x2="295" y2="30%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="295" cy="30%" r="1" fill="var(--secondary-color)"/>
      <text x="320" y="25%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="315" dy="0">Back-Propagation</tspan>
        <tspan x="315" dy="15">(Kelley, 1960)</tspan>
      </text>
      <!-- 1962 Event - Connectionist -->
      <line x1="322" y1="50%" x2="322" y2="73%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="322" cy="73%" r="1" fill="var(--secondary-color)"/>
      <text x="330" y="76%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="330" dy="0">Perceptrons</tspan>
        <tspan x="330" dy="15">(Rosenblant, 1962)</tspan>
      </text>
      <!-- 1966 Event - Symbolic -->
      <line x1="376" y1="50%" x2="376" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="376" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="376" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="376" dy="0">ELIZA</tspan>
        <tspan x="376" dy="15">(MIT, 1966)</tspan>
      </text>
      <!-- 1969 Event - Symbolic -->
      <line x1="416.5" y1="50%" x2="416.5" y2="20%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="416.5" cy="20%" r="1" fill="var(--secondary-color)"/>
      <text x="416.5" y="15%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="416.5" dy="0">The DENDRAL</tspan>
        <tspan x="416.5" dy="15">(Buchanan, 1969)</tspan>
      </text>
      <!-- 1972 Event - Symbolic -->
      <line x1="457" y1="50%" x2="457" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="457" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="445" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="445" dy="0">PROLOG</tspan>
        <tspan x="445" dy="15">(1972)</tspan>
      </text>
      <!-- 1972 Event - Symbolic -->
      <line x1="457" y1="50%" x2="457" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="457" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="465" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="465" dy="0">MYCIN</tspan>
        <tspan x="465" dy="15">(Stanford, 1972)</tspan>
      </text>
      <!-- 1975 Event - Symbolic -->
      <line x1="497.5" y1="50%" x2="497.5" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="497.5" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="505" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="505" dy="0">FRAMES</tspan>
        <tspan x="505" dy="15">(1975)</tspan>
      </text>
      <!-- 1982 Event - Connectionist -->
      <line x1="592" y1="50%" x2="592" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="592" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="592" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="592" dy="0">Hopfield net</tspan>
        <tspan x="592" dy="15">(1982)</tspan>
      </text>
      <!-- 1982 Event - Symbolic -->
      <line x1="592" y1="50%" x2="592" y2="57%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="592" cy="57%" r="1" fill="var(--secondary-color)"/>
      <text x="592" y="60%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="592" dy="0">R1</tspan>
        <tspan x="592" dy="15">(McDermott, 1982)</tspan>
      </text>
      <!-- 1986 Event - Connectionist -->
      <line x1="646" y1="50%" x2="646" y2="25%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="646" cy="25%" r="1" fill="var(--secondary-color)"/>
      <text x="646" y="17%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="646" dy="0">Parallel Distributed Processing</tspan>
        <tspan x="646" dy="15">(Rumerlhart &</tspan>
        <tspan x="646" dy="17">McClelland, 1986)</tspan>
      </text>
      <!-- 1988 Event - Symbolic -->
      <line x1="673" y1="50%" x2="673" y2="35%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="673" cy="35%" r="1" fill="var(--secondary-color)"/>
      <text x="705" y="30%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="705" dy="0">Bayesian Networks</tspan>
        <tspan x="705" dy="15">(Pearls, 1988)</tspan>
      </text>
      <!-- 1988 Event - Symbolic -->
      <line x1="673" y1="50%" x2="673" y2="73%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="673" cy="73%" r="1" fill="var(--secondary-color)"/>
      <text x="673" y="76%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="673" dy="0">Reinforcement Learning</tspan>
        <tspan x="673" dy="15">(Sutton, 1988)</tspan>
      </text>
      <!-- 1990 Event - Connectionist -->
      <line x1="700" y1="50%" x2="700" y2="65%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="700" cy="65%" r="1" fill="var(--secondary-color)"/>
      <text x="730" y="68%" text-anchor="middle" style="font-size: 12px; fill: var(--connectionist-color);">
        <tspan x="730" dy="0">Image Recognition</tspan>
        <tspan x="730" dy="15">(LeCun et al., 1990)</tspan>
      </text>
      <!-- 1997 Event - Symbolic -->
      <line x1="794.5" y1="50%" x2="794.5" y2="45%" stroke="var(--secondary-color)" stroke-width="1"/>
      <circle cx="794.5" cy="45%" r="1" fill="var(--secondary-color)"/>
      <text x="780.5" y="40%" text-anchor="middle" style="font-size: 12px; fill: var(--symbolic-color);">
        <tspan x="780.5" dy="0">Deep Blue beats</tspan>
        <tspan x="780.5" dy="15">Kasparov (IBM, 1997)</tspan>
      </text>
    </svg>
</div>
  </div>
</div>
