<!-- SLIDES: -->
<!-- Course piece (round 2, M9). Numbers and top words from the executed L3 notebook, box-run/week-2/W2-L3-L4-VALUES.md (L3 s54 section). One table row per HDBSCAN group: size, top words, read or not. FLAG: only group 1 is read, so 8 papers are in view after L3. The critic is still ruling on whether that is acceptable. -->

## What a Group Means Here

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 45%">
                <p><b>For the council team</b></p>
                <ul style="font-size: 0.85em">
                    <li>The decision uses the HDBSCAN groups</li>
                    <li>The team reads a group when its top words touch its topic, such as obesity, diet, diabetes or hypertension</li>
                    <li>A paper gets the group support only if it sits in a group the team reads</li>
                    <li>Noise papers get no support. They are the outlier list, kept for a look</li>
                    <li>k-means with k = 8 is used only for stability and agreement</li>
                    <li>What would change it: another floor, more SVD directions, another reading of the top words</li>
                    <li>Group 4 (87 papers) has food in its top words but is not read under the declared word list, so another reading would change the result</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">
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
                <p style="font-size: 0.8em">Noise, listed for a look: 108 papers</p>
                <p style="font-size: 0.8em">In view with 2 supports: 8 papers</p>


```python
SUPPORT_COLUMNS = ["has_pattern", "read_group"]
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
