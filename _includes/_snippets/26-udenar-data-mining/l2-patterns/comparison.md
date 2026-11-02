<!-- SLIDES: -->
<!-- L2 numbers: confirmed planner table, 30 Oct 2026 (swap null with sorted(t), seed 7, 100 tables. PC wvenv run of check_week1_patterns.py --shortlist, repeatable across hash seeds). health, use p95 65 from the same fixed run. Random pair cosine p95 0.457 with the p95() rank rule: box run on rebuilt data, en_core_web_lg. All null-dependent numbers of L2 live only in this file. -->

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 40%">
                <p><b>The nutrition papers</b></p>
                <ul>
                    <li>317 papers with five words or more</li>
                    <li>Floor of 10 papers</li>
                    <li>870 words at the floor</li>
                    <li>16,271 candidate pairs at the floor</li>
                    <li>100 swap randomised tables, about 20 to 40 s on Colab</li>
                </ul>
                <p>Kept = at the floor and strictly above the 95th percentile of its 100 swap randomised counts.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>Kept pairs, highest lift first</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Pair</th><th>Papers</th><th>Lift</th><th>p95 of chance</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>intervals + uis</td><td>11</td><td>19.8</td><td>3</td></tr>
                        <tr><td>saharan + sub</td><td>16</td><td>18.6</td><td>3</td></tr>
                        <tr><td>females + males</td><td>14</td><td>17.6</td><td>3</td></tr>
                        <tr><td>fasting + plasma</td><td>10</td><td>17.4</td><td>3</td></tr>
                        <tr><td>cross + sectional</td><td>12</td><td>15.8</td><td>4</td></tr>
                    </tbody>
                </table>
                <p>Fixed phrases: uncertainty intervals (UIs), sub Saharan, fasting plasma glucose, cross sectional.</p>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 55%">
                <p><b>A selection of kept pairs with 20 papers or more, highest lift first</b></p>
                <table class="table" style="font-size: 0.7em">
                    <thead>
                        <tr><th>Rank</th><th>Pair</th><th>Papers</th><th>Lift</th><th>p95</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td>lived + ylds</td><td>20</td><td>11.3</td><td>6</td></tr>
                        <tr><td>2</td><td>sdi + socio</td><td>20</td><td>10.6</td><td>5</td></tr>
                        <tr><td>3</td><td>demographic + sdi</td><td>20</td><td>10.2</td><td>5</td></tr>
                        <tr><td>5</td><td>lost + ylls</td><td>20</td><td>9.9</td><td>7</td></tr>
                        <tr><td>6</td><td>blood + pressure</td><td>22</td><td>9.2</td><td>7</td></tr>
                        <tr><td>10</td><td>men + women</td><td>28</td><td>7.8</td><td>9</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 45%">
                <p>Twice the floor shows Global Burden of Disease terms: YLDs (years lived with disability), YLLs (years of life lost), SDI (socio-demographic index).</p>
                <p>Then plain topics: blood + pressure, men + women.</p>
                <p><b>The count, last</b></p>
                <p>7,311 pairs kept, 6,507 of them with lift 2 or more.</p>
                <p>The 95th percentile of chance has median 14, range 2 to 80.</p>
                <p>About 800 of 16,000 candidates pass by luck alone. Read from the top.</p>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 32%">
                <p><b>Highest support</b></p>
                <p>Common words. Lift stays close to 1.</p>
                <p>All four are kept. For common words the 95th percentile of chance is high, 58 to 80.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 68%">
                <table class="table">
                    <thead>
                        <tr><th>Pair</th><th>Papers</th><th>p95 of chance</th><th>Lift</th><th>Cosine</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>disease + health</td><td>84</td><td>80</td><td>1.32</td><td>0.57</td></tr>
                        <tr><td>disease + risk</td><td>82</td><td>58</td><td>1.90</td><td>0.62</td></tr>
                        <tr><td>health + risk</td><td>82</td><td>75</td><td>1.36</td><td>0.55</td></tr>
                        <tr><td>health + years</td><td>81</td><td>71</td><td>1.43</td><td>0.31</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Where they disagree</b></p>
                <table class="table">
                    <thead>
                        <tr><th>Pair</th><th>What happened</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>health + use</td><td>52 papers. Under chance the 95th percentile is 65. Not kept</td></tr>
                        <tr><td>food + nutrition</td><td>Cosine 0.63, above the random pair 95th percentile of 0.46. Only 9 papers together, below the support floor</td></tr>
                        <tr><td>background + methods</td><td>77 papers, lift 2.72. Abstract labels, removed in preparation</td></tr>
                        <tr><td>diabetes + obesity</td><td>19 papers, lift 3.7, cosine 0.78. All three agree</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
