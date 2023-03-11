---
layout: default
title: Research
permalink: /research/
---

<div id="gs_publications"></div>
<script src="//www.google.com/jsapi" type="text/javascript"></script>
<script type="text/javascript">
    google.load("jquery", "1.4.2");
    google.load("search", "1", {language: "en"});
    google.setOnLoadCallback(function() {
        var pubSearch = new google.search.PublicationSearch();
        //pubSearch.setResultSetSize(10);
        pubSearch.setUserDefinedLabel("Publication List");
        pubSearch.execute("Christian Cabrera Jojoa");
        google.search.Search.getBranding('branding');
        google.search.Search.generateCseBranding('branding');
        google.search.Search.parseOptions('pubSearch');
        pubSearch.setLinkTarget(google.search.Search.LINK_TARGET_SELF);
        pubSearch.draw(document.getElementById("gs_publications"));
    });
</script>
