<!-- SLIDES: -->
<!-- Course piece (round 2, M10). The TF-IDF pipeline moved out of the shared classification-evaluation.md. These are the five-fold numbers of the comparison slide, on the training rows only (S2). -->

## Right and Wrong Counts

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 30%">
                <p><b>Five folds on the papers</b></p>
                <ul>
                    <li>TF-IDF inside the model, so word weights are learned in each fold</li>
                    <li>The encoder vectors do not learn from the marks, so they go in as they are</li>
                    <li>Training rows only, never the kept apart papers</li>
                    <li>First line: the kept apart intervals</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 70%">


```python
from sklearn.pipeline import make_pipeline

print(f1_interval(y_test, pred_lr), f1_interval(y_test, pred_encoder, pred_lr))

model_tfidf = make_pipeline(
    TfidfVectorizer(analyzer=lambda tokens: tokens, sublinear_tf=True),
    LogisticRegression(class_weight="balanced", C=C_REG, max_iter=1000))
model_encoder = LogisticRegression(class_weight="balanced", C=C_REG,
                                   max_iter=1000)

cv_tfidf = cross_val_predict(model_tfidf, train_tokens, y_train, cv=folds)
cv_encoder = cross_val_predict(model_encoder, V_train, y_train, cv=folds)
cv_keywords = [keyword_match(t) for t in train_texts]   # no training
for pred in (cv_keywords, cv_tfidf, cv_encoder):
    print(round(f1_score(y_train, pred), 2), round(accuracy_score(y_train, pred), 2))
```

            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
