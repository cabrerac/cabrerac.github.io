<!-- SLIDES: -->

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Our question:</b> can the attributes of a paper predict an international collaboration, with authors from at least two countries?</p>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 60%">
                <p><b>The label and the attributes for the lab</b></p>
                <ul>
                    <li><b>Label:</b> internacional, n_countries of 2 or more</li>
                    <li>276 papers with a label, 145 of them international (53%)</li>
                    <li>Papers with no affiliation data are left out as missing</li>
                    <li><b>Inputs:</b> year, number of authors, venue type, open access and work type</li>
                    <li>Not the abstract, the citations or the links, which earlier lectures used</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 40%">
                <img src="{{ site.url }}/assets/media/images/openalex-mark.png" alt="OpenAlex mark" style="height: 280px">
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
                <p><b>The label for the groups: a target category</b></p>
                <p>categoria_objetivo is 1 when the article's categoria is one of the group's target categories, TARGETS[GROUP], and 0 when it is not.</p>
                <ul>
                    <li>The categories come from the people who edit Wikipedia, so the label is given, not found.</li>
                    <li>Not read from the text, that was Lecture 4.</li>
                    <li>Not a popularity count, which says how known an item is, not what it is.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>The five inputs for the Wikipedia groups</b></p>
                <ul>
                    <li><b>kind:</b> types with at least support_floor(n) articles, the rest Other</li>
                    <li><b>has_country</b></li>
                    <li><b>has_date</b>, with the imputed year</li>
                    <li><b>has_image</b></li>
                    <li><b>n_claims_without(...):</b> P18, the image, comes out of n_claims only when it is the label</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Overlap with Lecture 4</b></p>
                <p>A label that repeats the text result is not a new result.</p>
                <ul>
                    <li>phi measures how the label follows text_says_read</li>
                    <li>At 0.30 or more, both count as one result, text_or_prediction</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## The Question and the Data

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Leakage on our data</b></p>
                <p>An input built from the label gives the answer away.</p>
                <ul>
                    <li>n_countries defines the lab label, so it is not an input</li>
                    <li>For the groups, P18, the image, comes out of n_claims when it is the label</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
