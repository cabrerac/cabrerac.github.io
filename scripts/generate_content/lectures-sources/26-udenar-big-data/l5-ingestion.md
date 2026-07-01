---
course_code: 26-udenar-big-data
title: Data ingestion and workflow
description: Lecture 5 introduces batch and stream ingestion approaches. Once our data is harmonised on a lakehouse, we need to create data artefacts and views to feed our analytic tasks. These artefacts can be created and processed offline following a schedule (i.e., batch) or in real-time (i.e., streaming) depending on the data nature. This lecture introduces both concepts and the production platforms and tools that support them.
session: 5
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l5-ingestion
lecture_date: 20/06/2026
permalink: /teaching/26-udenar-big-data/l5-ingestion/
visible: true
group_notebook: week-3-group
notebook_language: es
notebook_title: Ingesta y flujos de trabajo
notebook_description: Práctica individual de la Lección 5. Pasamos de la ingesta batch sobre el lakehouse GEIH de la semana 2 a una fuente en streaming con Kafka. Registramos auditoría y contrato de esquema.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/last-time.md %}

<!-- SLIDES: -->

# Data Ingestion

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/ingestion.md %}

<!-- SLIDES: -->

# Batch and ETL

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/batch-etl.md %}

<!-- SLIDES: -->

# Streams

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/streams.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/conclusions.md %}

{% include _snippets/26-udenar-big-data/l5-ingestion/practical-slides.md %}

<!-- RENDER: -->

### Week 3 links

- [Week 3 hub](/teaching/26-udenar-big-data/week-3-hub-es/)

### Resources

- [Introductory Python course](https://www.youtube.com/watch?v=nKPbfIU442g) (optional video)
- [Apache Kafka documentation](https://kafka.apache.org/documentation/) (reference)

### References

- Zaharia, M., et al. (2016). [Apache Spark: a unified engine for big data processing](https://doi.org/10.1145/2934664). *CACM*, 59(11), 56–65.
- Jarrahi, M. H., et al. (2023). *The Principles of Data-Centric AI*. *(Course PDF.)*
- Kreps, J., Narkhede, N., & Rao, J. (2011). Kafka: a distributed messaging system for log processing. *(Recommended async.)*

<!-- end RENDER: -->

{% include _snippets/26-udenar-big-data/l5-ingestion/practical.md %}

