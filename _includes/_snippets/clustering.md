<!-- SLIDES: -->

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>What is a group</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"The aim of clustering is to find structure in data and is therefore exploratory in nature."</p>
                            <p><a href="https://doi.org/10.1016/j.patrec.2009.09.011" target="_blank" rel="noopener noreferrer">(Jain, 2010, abstract, p. 651)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li>Items inside a group are close to each other</li>
                    <li>Items in different groups are far apart</li>
                    <li>No one tells the method what the groups are</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/cluster-analysis-mouse.svg" alt="Three groups of points" style="height: 380px">
                <div class="footnote">ClusterAnalysis Mouse - Chire, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>A group needs a reader</b></p>
                <table class="table">
                    <tr>
                        <td>
                            <p>"In reality, a cluster is a subjective entity that is in the eye of the beholder and whose significance and interpretation requires domain knowledge."</p>
                            <p><a href="https://doi.org/10.1016/j.patrec.2009.09.011" target="_blank" rel="noopener noreferrer">(Jain, 2010, section 2)</a></p>
                        </td>
                    </tr>
                </table>
                <ul>
                    <li>A method returns labels, not meanings</li>
                    <li>Someone who knows the field reads each group</li>
                    <li>Then decides what the group is for</li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-center" style="width: 100%">
                <p><b>Similarity and distance</b></p>
                <p>Each item is a vector $\mathbf{x}$, for example the word counts of one text.</p>
                <p>$$\cos(\mathbf{x}, \mathbf{y}) = \frac{\mathbf{x} \cdot \mathbf{y}}{\lVert \mathbf{x} \rVert \, \lVert \mathbf{y} \rVert}$$</p>
                <p>$$d(\mathbf{x}, \mathbf{y}) = 1 - \cos(\mathbf{x}, \mathbf{y})$$</p>
                <p>Two texts with the same words in the same shares have distance 0.</p>
            </div>
        </div>
    </div>
</div>

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>Scale each item to length 1</b></p>
                <p>$$\hat{\mathbf{x}} = \frac{\mathbf{x}}{\lVert \mathbf{x} \rVert}$$</p>
                <ul>
                    <li><p>A long text has big counts, a short one has small counts</p></li>
                    <li><p>After scaling, only the mix of words matters</p></li>
                    <li><p>Then $\cos(\hat{\mathbf{x}}, \hat{\mathbf{y}}) = \hat{\mathbf{x}} \cdot \hat{\mathbf{y}}$</p></li>
                    <li><p>And $\lVert \hat{\mathbf{x}} - \hat{\mathbf{y}} \rVert^2 = 2\,(1 - \cos)$, so plain distance follows cosine</p></li>
                </ul>
            </div>
        </div>
    </div>
</div>

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 50%">
                <p><b>An item that fits no group</b></p>
                <ul>
                    <li>Some methods put every item in a group</li>
                    <li>Others can say an item fits nowhere</li>
                    <li>An item far from every group is worth a human look</li>
                    <li>It can be an error, a rare case, or a new topic</li>
                </ul>
            </div>
            <div class="column vertical-middle text-center" style="width: 50%">
                <img class="external-svg" src="{{ site.url }}/assets/media/images/clusters-with-noise.svg" alt="Groups with points around them" style="height: 380px">
                <div class="footnote">Cluster-2 - hellisp and Wgabrie, Public domain, via Wikimedia Commons</div>
            </div>
        </div>
    </div>
</div>

## Groups of Similar Items

<div class="rows" style="height: 100%">
    <div class="row" style="height: 100%">
        <div class="columns" style="width: 100%">
            <div class="column vertical-middle text-left" style="width: 100%">
                <p><b>A short history</b></p>
                <ul>
                    <li><b>1956, Steinhaus</b> - split a body into parts around centres</li>
                    <li><b>1957, Lloyd</b> - the k-means steps, published in 1982 <a href="https://doi.org/10.1109/TIT.1982.1056489" target="_blank" rel="noopener noreferrer">(Lloyd, 1982)</a></li>
                    <li><b>1967, MacQueen</b> - the name k-means</li>
                    <li><b>1977, EM</b> - fit a mixture when the group of each item is unknown <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer">(Dempster et al., 1977)</a></li>
                    <li><b>1996, DBSCAN</b> - groups as dense regions, with noise <a href="https://cdn.aaai.org/KDD/1996/KDD96-037.pdf" target="_blank" rel="noopener noreferrer">(Ester et al., 1996)</a></li>
                    <li><b>1999, OPTICS</b> - an order of points for many densities <a href="https://doi.org/10.1145/304181.304187" target="_blank" rel="noopener noreferrer">(Ankerst et al., 1999)</a></li>
                    <li><b>2013, HDBSCAN</b> - a tree of densities, keep the stable groups <a href="https://doi.org/10.1007/978-3-642-37456-2_14" target="_blank" rel="noopener noreferrer">(Campello et al., 2013)</a></li>
                </ul>
            </div>
        </div>
    </div>
</div>

<!-- end SLIDES: -->
