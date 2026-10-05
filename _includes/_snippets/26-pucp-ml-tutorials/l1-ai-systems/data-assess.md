<!-- SLIDES: -->

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 75%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/images/data-science-process.png" alt="Data Science Process" style="height: 450px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 25%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>With the data in hand we move to <b>assess</b>: deciding whether it is fit for the question.</p>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p>After collecting the data (i.e., data access), we need to perform <b>a data assessment process to understand the data</b>, identify and mitigate data quality issues, uncover patterns, and gain insights.</p>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 60%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <img src="{{ site.url }}/assets/media/diagrams/data-assess-pipeline.svg" alt="Data Assess Pipeline" style="height: 500px">
            </div>
        </div>
    </div>
    <div class="row" style="height: 40%">
        <div class="columns" style="width: 95%">
            <div class="column vertical-middle text-center" style="width: 100%">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Data quality refers to <b>the state of data</b> in terms of its <b>fitness for a purpose</b></p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <img src="{{ site.url }}/assets/media/images/data-quality.jpg" alt="Data Quality" style="height: 400px">
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>Data quality refers to <b>the state of data</b> in terms of its <b>fitness for a purpose</b></p>
                <p>This is a multi-dimensional concept</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <ul>
                    <li><b>Accuracy</b></li>
                    <li><b>Completeness</b></li>
                    <li><b>Uniqueness</b></li>
                    <li><b>Consistency</b></li>
                    <li><b>Timeliness</b></li>
                    <li><b>Validity</b></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Accuracy</b> does the value match the event?</p>
                <p><b>Completeness</b> are the fields we need present?</p>
                <p><b>Uniqueness</b> is each event listed once?</p>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Consistency</b> do units and scales agree?</p>
                <p><b>Timeliness</b> is the record current enough for the decision?</p>
                <p><b>Validity</b> does the value obey the declared format?</p>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
               <img src="{{ site.url }}/assets/media/images/data-usability.jpg" alt="Data Usability" style="height: 400px">
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
               <p><b>Poor data quality can lead to:</b></p>
                <ul>
                    <li>Inaccurate predictions</li>
                    <li>Biased results</li>
                    <li>Over-trust in a table that is not fit</li>
                    <li>Intellectual debt</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Data Assess

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p>For a post-earthquake review, ask of each row:</p>
                <ul>
                    <li>Do we know <b>where</b> it was, and with what uncertainty?</li>
                    <li>Do we know <b>how large</b> it was, and on which scale?</li>
                    <li>What risk remains if we still train a first model?</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
