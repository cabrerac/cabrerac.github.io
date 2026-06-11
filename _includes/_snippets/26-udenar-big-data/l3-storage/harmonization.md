<!-- SLIDES: -->

## Harmonization

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Make the data comparable and readable</b></p>
                <ul>
                    <li>Join the labour and demographics tables per person</li>
                    <li>Rename DANE codes to readable names</li>
                    <li>Fix types, text to numbers where needed</li>
                    <li>Derive the partition keys, year and month</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p>The goal is a clean table that any teammate can read without the DANE codebook open.</p>
            </div>
        </div>
    </div>
</div>

## Harmonization

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 50%">
                <p><b>DANE code</b></p>
                <table class="table">
                    <tr><td>P6040</td><td>edad</td></tr>
                    <tr><td>P3271</td><td>sexo</td></tr>
                    <tr><td>P6240</td><td>actividad</td></tr>
                    <tr><td>FEX_C18</td><td>factor_expansion</td></tr>
                </table>
            </div>
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>Readable name</b></p>
                <p>The same value, now with a name a person understands. We keep <b>actividad</b> as the raw code and interpret it later, during processing.</p>
            </div>
        </div>
    </div>
</div>

## Harmonization

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-top text-left" style="width: 45%">
                <p><b>One function per month</b></p>
                <ul>
                    <li>Read two CSV tables</li>
                    <li>Join on the person keys</li>
                    <li>Return a clean typed table</li>
                </ul>
            </div>
            <div class="column vertical-middle text-left" style="width: 55%">

```python
merged = labour.merge(
    demog, on=PERSON_KEYS,
    how="left", validate="many_to_one",
)
return pd.DataFrame({
    "anio": anio, "mes": mes,
    "dpto": a_entero(merged["DPTO"]),        # Int64, admite faltantes
    "edad": a_entero(merged["P6040"]),
    "actividad": pd.to_numeric(merged["P6240"], errors="coerce"),  # float, se compara luego
    "factor_expansion": pd.to_numeric(merged["FEX_C18"], errors="coerce"),
})
```

</div>
        </div>
    </div>
</div>

## Harmonization

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Storage layer or processing layer?</b> We rename and fix types now, at storage time. We do not decide who counts as employed here. That interpretation belongs to processing in lecture 4, so the stored data stays neutral and reusable.</p>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
