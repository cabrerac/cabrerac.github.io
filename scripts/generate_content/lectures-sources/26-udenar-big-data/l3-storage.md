---
course_code: 26-udenar-big-data
title: Data storage and management
description: Lecture 3 introduces data storage and its evolution. We reflect about the storage need and move from relational and non-relational storage concepts to current data architectures that support big data processing. We present the lakehouse concept and how to build it.
session: 3
start_time: 07:00 am
end_time: 01:00 pm
hours: 5
author: Christian Cabrera Jojoa
email: chc79@cam.ac.uk
position: Assistant Research Professor
department: Department of Computer Science and Technology
institution: University of Cambridge
layout: lecture
lecture_code: l3-storage
lecture_date: 13/06/2026
permalink: /teaching/26-udenar-big-data/l3-storage/
visible: true
group_notebook: week-2-group
notebook_language: es
notebook_title: Almacenamiento y gestión de datos
notebook_description: Práctica individual de la Lección 3. Construimos un lakehouse GEIH para 2024 (tabla harmonizada particionada en Parquet bajo data/processed/geih-spine/). Comparamos leer el lakehouse frente a CSV crudo y documentamos gobernanza al almacenar.
---

<!-- SLIDES: -->

# Last Time

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l3-storage/last-time.md %}

<!-- SLIDES: -->

# The Need to Store

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l3-storage/storage-need.md %}

<!-- SLIDES: -->

# Databases

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l3-storage/databases.md %}

<!-- SLIDES: -->

# Big Data Storage

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l3-storage/big-data-storage.md %}

<!-- SLIDES: -->

# Conclusions

<!-- end SLIDES: -->

{% include _snippets/26-udenar-big-data/l3-storage/conclusions.md %}

{% include _snippets/26-udenar-big-data/l3-storage/practical-slides.md %}

<!-- RENDER: -->

### Week 2 links

- [Week 2 hub](/teaching/26-udenar-big-data/week-2-hub-es/)

### Resources

- [Introductory Python course](https://www.youtube.com/watch?v=nKPbfIU442g) (optional video)
- [Introduction to data management](https://www.youtube.com/watch?v=9P2oNqRbdyI) (optional video)

### References

- Zuboff, S. (2019). *The age of surveillance capitalism* (Chapter 3). PublicAffairs. *(Course PDF — same as week 1.)*
- Dwork, C. (2006). [Differential privacy](https://doi.org/10.1007/11787006_1). *ICALP 2006* (LNCS 4052).
- Armbrust, M., et al. (2021). [Lakehouse: A new generation of open platforms](https://people.eecs.berkeley.edu/~matei/papers/2021/cidr_lakehouse.pdf). *CIDR ’21*.
- Stonebraker, M., & Çetintemel, U. (2010). [“One size fits all”: An idea whose time has come and gone](https://doi.org/10.1145/1661412.1661413). *DEABS*.

<!-- end RENDER: -->

{% include _snippets/26-udenar-big-data/l3-storage/practical.md %}

