---
layout: default
title: Students
description: "Current and past students under my supervision"
permalink: /students/
---

This page showcases the students I have supervised and am currently supervising, demonstrating my commitment to research mentorship and academic development.

**Debug**: Data loaded: {{ site.data.students != nil }}
**Debug**: Current students count: {{ site.data.students.current.size }}
**Debug**: Past students count: {{ site.data.students.past.size }}

{% include students_list.html %}
