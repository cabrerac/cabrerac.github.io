<!-- SLIDES: -->

## This Week Notebooks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l6-prediction.ipynb" target="_blank">Lecture 6 notebook</a> follows CRISP-DM</b></p>
                <p>The notebook predicts, from the abstract, whether a paper must be read. The label is the Lecture 4 topic label. It trains logistic regression and one hidden layer, and compares them. It does not train a transformer, and it does not use trees.</p>
                <ul>
                    <li><b>Part 1, Business understanding:</b> the question and what "must read" assumes</li>
                    <li><b>Part 2, Data understanding:</b> the label from the OpenAlex topics, and the abstracts</li>
                    <li><b>Part 3, Data preparation:</b> the held-out set and TF-IDF from the training rows</li>
                    <li><b>Part 4, Modeling:</b> the majority class, logistic regression and one hidden layer</li>
                    <li><b>Part 5, Evaluation:</b> both against the majority class and a keyword rule, over five splits, and a label leak</li>
                    <li><b>Part 6, Deployment:</b> a paper is listed only if both methods say read, in prediccion_l6.csv and lectura_l6.csv</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## This Week Notebooks

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-3-group.ipynb" target="_blank">week 3 group notebook</a></b></p>
                <p>The same steps on the department file. The label is a target category of each article. The notebook does not train a transformer, and it does not use trees.</p>
                <ul>
                    <li><b>Exercise 0, Setup:</b> group, data and parameters</li>
                    <li><b>Exercise 1, Business understanding:</b> the question and what the graph is for</li>
                    <li><b>Exercise 2, Data understanding:</b> titles, links, the label and the attributes</li>
                    <li><b>Exercise 3, Data preparation:</b> the undirected graph, the held-out set and the table</li>
                    <li><b>Exercise 4, Modeling:</b> Louvain communities and one hidden layer</li>
                    <li><b>Exercise 5, Evaluation:</b> both against the majority with the +0.02 rule</li>
                    <li><b>Exercise 6, Deployment:</b> a reading list and interpretation</li>
                </ul>
                <p>The notebook ends with a contribution log.</p>
            </div>
        </div>
    </div>
</div>

## Project Deliverables

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>After the talks on Saturday 5 December</b></p>
                <ul>
                    <li><b>Friday 4 December, 23:59:</b> slides <code>project-slides-&lt;group_id&gt;.pdf</code>, one PDF per group. <a href="https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-presentation-template.pptx" target="_blank">Slides template</a></li>
                    <li><b>Tuesday 8 December, 23:59:</b> zip <code>project-&lt;group_id&gt;.zip</code>, with the <a href="https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-requirements-template.docx" target="_blank">requirements template</a>, the <a href="https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/project-group.ipynb" target="_blank">project notebook</a>, and <code>outputs/lista_articulos.csv</code></li>
                    <li><b>Wednesday 9 December, 23:59:</b> reflection <code>project-reflection-&lt;apellido&gt;-&lt;inicial&gt;.pdf</code>. <a href="https://cabrerac.github.io/assets/documents/26-udenar-data-mining/project-reflection-template.docx" target="_blank">Reflection template</a></li>
                </ul>
                <p>Each talk is 20 minutes. Colombia time.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
