<!-- SLIDES: -->

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>For the department team</b></p>
                <p>The team reads an HDBSCAN group when its top words touch its topic, such as obesity, diet, diabetes or hypertension.</p>
                <ul>
                    <li><b>read_group:</b> marks each paper in a group the team reads</li>
                    <li>Noise papers do not get it. They are the outlier list, kept for a look</li>
                </ul>
                <p><b>HDBSCAN groups of the papers</b></p>
                                                <table class="table" style="font-size: 0.55em">
                                                    <thead>
                                                        <tr><th>Group</th><th>Papers</th><th>Top words</th><th>Read by the team</th></tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr><td>0</td><td>16</td><td>cancer, deaths, million, countries, incidence, mortality, cases, years</td><td>no</td></tr>
                                                        <tr><td>1</td><td>10</td><td>diabetes, care, standards, recommendations, committee, members, practice, professional</td><td>yes</td></tr>
                                                        <tr><td>2</td><td>38</td><td>guidelines, disease, management, recommendations, evidence, patients, patient, liver</td><td>no</td></tr>
                                                        <tr><td>3</td><td>58</td><td>million, age, years, risk, prevalence, global, burden, deaths</td><td>no</td></tr>
                                                        <tr><td>4</td><td>87</td><td>studies, data, research, effects, food, human, review, use</td><td>no</td></tr>
                                                    </tbody>
                                                </table>
                                                <p style="font-size: 0.8em">108 noise papers, kept for a look. 8 in view with MIN_SUPPORTS = 2. Each group sets and justifies this number in its project.</p>
            </div>
        </div>
    </div>
</div>

## The Project

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>What would change it</b></p>
                <ul>
                    <li>Another floor, more SVD directions or another reading of the top words</li>
                    <li>Group 4 has food in its top words but is not read under the declared word list</li>
                    <li>k-means with k = 8 is used only for stability and agreement</li>
                </ul>

```python
SUPPORT_COLUMNS = ["has_pattern", "read_group"]
```

                <p>The week 2 group notebook, part 1, does the same on the department file.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
