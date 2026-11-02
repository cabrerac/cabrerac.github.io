<!-- RENDER: -->

**Saturday 14 Nov 2026, 07:00 to 13:00 (Colombia)**. Lectures **L3** (Groups, outliers, and what a group means) and **L4** (Text extraction and marked examples).

---

### Lectures and Saturday plan

| Resource | Link |
|---------|--------|
| Lecture 3 - Groups, outliers, and what a group means | [l3-groups](/teaching/26-udenar-data-mining/l3-groups/) |
| Lecture 4 - Text extraction and marked examples | [l4-text](/teaching/26-udenar-data-mining/l4-text/) |
| Recording L3 | link added when recorded |
| Recording L4 | link added when recorded |
| Saturday plan (PDF, Spanish) | [week-2-session-plan-es.pdf](/assets/documents/26-udenar-data-mining/week-2-session-plan-es.pdf) |
| Course home | [/teaching/26-udenar-data-mining/](/teaching/26-udenar-data-mining/) |

Watch both recordings before Saturday. Each recording has the theory and a step-by-step pass through that lecture's notebook. The recording links are in the table above.

---

### Colabs

| Notebook | Colab |
|----------|-------|
| L3 individual | [l3-groups](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l3-groups.ipynb) |
| L4 individual | [l4-text](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/l4-text.ipynb) |
| Week 2 group | [week-2-group](https://colab.research.google.com/github/cabrerac/cabrerac.github.io/blob/gh-pages/assets/notebooks/26-udenar-data-mining/week-2-group.ipynb) |

The L4 and group notebooks download a text encoder of about 470 MB. Run that cell first.

---

### Local installation

To run locally, install each notebook's dependencies from:

| Notebook | Requirements |
|----------|--------------------|
| L3 individual | [l3-groups-requirements.txt](/assets/notebooks/26-udenar-data-mining/l3-groups-requirements.txt) |
| L4 individual | [l4-text-requirements.txt](/assets/notebooks/26-udenar-data-mining/l4-text-requirements.txt) |
| Week 2 group | [week-2-group-requirements.txt](/assets/notebooks/26-udenar-data-mining/week-2-group-requirements.txt) |

The notebooks download the course data themselves. The files are also listed below.

---

### Course data

| Data | File |
|------|------|
| Papers on nutrition (labs) | [nutricion-papers.csv](/assets/data/26-udenar-data-mining/nutricion-papers.csv) |
| G1 Pobreza | [pobreza.csv](/assets/data/26-udenar-data-mining/pobreza.csv) |
| G2 Vivienda | [vivienda.csv](/assets/data/26-udenar-data-mining/vivienda.csv) |
| G3 Medio ambiente | [medio-ambiente.csv](/assets/data/26-udenar-data-mining/medio-ambiente.csv) |
| G4 Agricultura | [agricultura.csv](/assets/data/26-udenar-data-mining/agricultura.csv) |
| G5 Salud mental | [salud-mental.csv](/assets/data/26-udenar-data-mining/salud-mental.csv) |
| Sources and credit | [README](https://github.com/cabrerac/cabrerac.github.io/blob/gh-pages/assets/data/26-udenar-data-mining/README.md) |

---

### Readings and journal

| Resource | Link |
|---------|--------|
| Jain, A. K. (2010). Data clustering: 50 years beyond K-means | [DOI](https://doi.org/10.1016/j.patrec.2009.09.011) |
| Devlin, J., Chang, M.-W., Lee, K. and Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding | [PDF (ACL Anthology)](https://aclanthology.org/N19-1423.pdf) |
| Learning journal week 2 (Word) | [learning-journal-week-2.docx](/assets/documents/26-udenar-data-mining/learning-journal-week-2.docx) |

Fill in the journal before Saturday and bring it to the reading discussion. It is not graded. Both readings are also attached to the course email.

---

### Templates and deliverables

| Resource | Link |
|---------|--------|
| Week 2 reflection (Word) | [reflection-week-2-template.docx](/assets/documents/26-udenar-data-mining/reflection-week-2-template.docx) |
| Project requirements (Word) | [project-requirements-template.docx](/assets/documents/26-udenar-data-mining/project-requirements-template.docx) |

| Deliverable | Due (Colombia) |
|-------------|----------------|
| Group zip `week-2-<group_id>.zip` with `week-2-group-<group_id>.ipynb`, `pregunta.json`, `marcas.csv`, `outputs/grupos.csv`, `outputs/texto.csv` and `outputs/en_vista.csv` | Tue 17 Nov 2026, 23:59 |
| Reflection `week-2-reflection-<surname>-<initial>.pdf` (first surname and first initial) | Wed 18 Nov 2026, 23:59 |
| Project requirements document | Handed in with the project zip on Tue 1 Dec 2026 |

`outputs/grupos.csv` and `outputs/texto.csv` give two of the five supports for the starter list (groups and text). `outputs/en_vista.csv` keeps the three supports so far, and week 3 reads it. An article stays in view with two supports. The list to read has at most `max_articles` from your `pregunta.json`. The rest stay in the file with `recortado`. If fewer than `min_articles` qualify, the list is not padded. It is read in full and reported as a weak result.

Submissions go through Moodle. Your group's Teams link is in Moodle.

---

<!-- end RENDER: -->
