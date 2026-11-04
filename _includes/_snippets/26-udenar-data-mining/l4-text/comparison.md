<!-- SLIDES: -->
<!-- 2 Nov 2026: the visible note "Numbers: box run on rebuilt data." was removed from these slides (critic brief r1, S4). The source notes stay in these comments. -->
<!-- Numbers: box run on rebuilt data, DRAFT. box-run/RESULTS.md section 4 (held-out 20%, bootstrap 2,000 resamples, seed 7), checked by the critic (checkpoint B review, OK list). The keyword cells come from the round 2 slide code run with the keyword list of the Python slide (critic, checkpoint B round 2, S-R2-1) and are rechecked on the L4 notebook run, like every L4 number here. The five-fold column is on the 253 training rows (S2). The 64 kept apart papers carry the OpenAlex topic label until Christian marks them (M5). If he marks before recording, re-run this slide from the notebook after the marking. Agricultura target approved 30 Oct 2026. -->

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 36%">
                <p><b>The nutrition papers</b></p>
                <ul style="font-size: 0.72em">
                    <li>320 papers in the file. 3 are dropped because the abstract is a fragment such as "Peer Reviewed". 317 kept</li>
                    <li>Target: OpenAlex topics that mention obesity, diet, nutrition, diabetes, cardiovascular, lipoproteins, blood pressure or hypertension</li>
                    <li>96 of 317 papers are positive (30%)</li>
                    <li>64 papers kept apart, labelled by their OpenAlex topics until Christian marks them (19 yes)</li>
                    <li>Abstracts cut at 512 tokens: 93 of 317</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 64%">
                <table class="table" style="font-size: 0.58em">
                    <thead>
                        <tr><th>Method</th><th>Kept apart F1 [95%]</th><th>Kept apart TP, FP, FN, TN</th><th>Five folds on the 253 training rows, F1 (accuracy)</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Majority baseline</td><td>0</td><td>0, 0, 19, 45</td><td>0 (0.70)</td></tr>
                        <tr><td>Keyword list</td><td>0.63 [0.43, 0.79]</td><td>12, 7, 7, 38</td><td>0.68 (0.81)</td></tr>
                        <tr><td>TF-IDF and logistic regression</td><td>0.91 [0.80, 1.00]</td><td>16, 0, 3, 45</td><td>0.77 (0.88)</td></tr>
                        <tr><td>Encoder and logistic regression</td><td>0.89 [0.76, 0.98]</td><td>16, 1, 3, 44</td><td>0.78 (0.86)</td></tr>
                    </tbody>
                </table>
                <p style="font-size: 0.8em">Encoder minus TF-IDF: [-0.09, 0.00]. No clear winner. With 19 yes papers, one paper moves F1 a lot.</p>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Kept apart F1 in every extract</b></p>
                <table class="table" style="font-size: 0.5em">
                    <thead>
                        <tr><th>Extract</th><th>Kept apart (yes)</th><th>Keyword*</th><th>TF-IDF [95%]</th><th>Encoder [95%]</th><th>Encoder minus TF-IDF</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Nutrition papers</td><td>64 (19)</td><td>0.63</td><td>0.91 [0.80, 1.00]</td><td>0.89 [0.76, 0.98]</td><td>[-0.09, 0.00]</td></tr>
                        <tr><td>Inclusión Social</td><td>60 (14)</td><td>0.85</td><td>0.97 [0.87, 1.00]</td><td>0.90 [0.77, 1.00]</td><td>[-0.17, 0.00]</td></tr>
                        <tr><td>Vivienda</td><td>65 (14)</td><td>0.48</td><td>0.70 [0.42, 0.89]</td><td>0.81 [0.62, 0.94]</td><td>[-0.11, 0.37]</td></tr>
                        <tr><td>Medio ambiente</td><td>67 (12)</td><td>0.52</td><td>0.80 [0.53, 0.95]</td><td>0.73 [0.52, 0.88]</td><td>[-0.32, 0.19]</td></tr>
                        <tr><td>Agricultura</td><td>63 (17)</td><td>0.67</td><td>0.90 [0.77, 1.00]</td><td>0.83 [0.68, 0.95]</td><td>[-0.20, 0.05]</td></tr>
                        <tr><td>Salud mental</td><td>67 (33)</td><td>0.68</td><td>0.77 [0.65, 0.87]</td><td>0.76 [0.63, 0.86]</td><td>[-0.11, 0.10]</td></tr>
                    </tbody>
                </table>
                <p style="font-size: 0.55em">* Papers: the keyword list above. Wikipedia extracts: a stand-in list, the stems of the target category names. Your group writes its own list from the question.</p>
            </div>
        </div>
    </div>
</div>

## Comparing the Methods

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Kept apart F1 in every extract</b></p>
                <ul>
                    <li>Every interval of the difference includes 0. No clear winner</li>
                    <li>Five folds on all rows: the encoder is higher on average in vivienda and medio ambiente, but those intervals include 0 too</li>
                    <li>The encoder may help where the target words vary. It adds nothing where a few words decide</li>
                    <li>Targets: agricultura is Agrarismo + Organizaciones agrícolas. Salud mental is Trastornos mentales + Psiquiatría (50% yes, judged against the majority, 0.51)</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
