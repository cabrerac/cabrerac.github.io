<!-- SLIDES: -->

## The Label and the Attributes

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The label for the groups: a target category</b></p>
                <p>categoria_objetivo is 1 when the article's categoria is one of the group's target categories, TARGETS[GROUP], and 0 when it is not.</p>
                <p>The categories come from the people who edit Wikipedia, so the label is given, not found.</p>
                <p>Not read from the text, that was Lecture 4.</p>
                <p>Not a popularity count, which says how known an item is, not what it is.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>The five inputs for the Wikipedia groups</b></p>
                <ul>
                    <li><b>kind</b> - types with at least support_floor(n) articles, the rest Other</li>
                    <li><b>has_country</b></li>
                    <li><b>has_date</b>, with the imputed year</li>
                    <li><b>has_image</b></li>
                    <li><b>n_claims_without(...)</b> - P18, the image, comes out of n_claims only when it is the label</li>
                </ul>
                <p>The Lecture 6 notebook lists the inputs for the papers lab and the missing values per column.</p>
            </div>
        </div>
    </div>
</div>

## Overlap and Leakage

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Overlap with Lecture 4</b></p>
                <p>A label that repeats the text result is not a new result.</p>
                <p>How strong the overlap is, and what the course does about it.</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Leakage on our data</b></p>
                <p>Which input is built from the label, and what is taken out.</p>
                <p>The same model with and without it.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
