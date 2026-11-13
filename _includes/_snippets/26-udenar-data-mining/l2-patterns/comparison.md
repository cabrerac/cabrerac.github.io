<!-- SLIDES: -->

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Our question:</b> which word pairs repeat in the nutrition abstracts more often than chance would give?</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>The nutrition papers</b></p>
                <p>The same OpenAlex papers as in Lecture 1, one set of words per abstract.</p>
                <ul>
                    <li>317 papers with five words or more</li>
                    <li>A floor of 10 papers</li>
                    <li>16,271 candidate pairs at the floor</li>
                    <li>Lift at least 2, and cosine at least 0.5</li>
                </ul>
                <p>A pair is a stronger candidate when support, lift, and closeness all keep it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="{{ site.url }}/assets/media/images/openalex-mark.png" alt="OpenAlex mark" style="height: 300px">
                <div class="footnote">OpenAlex mark, OpenAlex</div>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
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
                <p>Fixed phrases come first: uncertainty intervals (UIs), sub Saharan, fasting plasma glucose, cross sectional.</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Kept pairs with 20 papers or more</b></p>
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
                <p>Global Burden of Disease terms come first, then plain topics such as blood + pressure. About 800 of the 16,271 candidates would pass by luck alone, so we read from the top.</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 32%">
                <p><b>Highest support</b></p>
                <p>Common words. Lift stays close to 1, and chance is high for them too.</p>
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

## The Question and the Data

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
                        <tr><td>health + years</td><td>81 papers, so support keeps it. Lift 1.43, under 2. Cosine 0.31, under 0.5. Counts only</td></tr>
                        <tr><td>food + nutrition</td><td>Cosine 0.63, above the cut of 0.5. Only 9 papers together, below the support floor</td></tr>
                        <tr><td>background + methods</td><td>77 papers, lift 2.72. Abstract labels, removed in preparation</td></tr>
                        <tr><td>diabetes + obesity</td><td>19 papers, lift 3.7, cosine 0.78. All three agree</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
