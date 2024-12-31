---
layout: course
code: 25-udenar-ml-intro
title: "Introduction to Machine Learning"
description: "Course of Introduction to Machine Learning"
institution: "Universidad de Nariño"
department: "Centro de Estudios y Asesoría en Estadística (CEASE)"
start_date: 01/03/2025
end_date: 30/06/2025
year: 2025
lectures: 10
hours: 40
permalink: /teaching/25-udenar-ml-intro/
---

{% assign course_lectures = site.lectures | where: "course", page.code | sort: 'session' %}
<br>
<h2>Lectures</h2>
<ul>
{% for lecture in course_lectures %}
  <li>
    <a href="{{ lecture.permalink }}">
      <strong>{{ lecture.title }}</strong>
    </a><br>
    Date: {{ lecture.date | date: "%B %d, %Y" }}<br>
    Description: {{ lecture.description }}<br>
  </li>
{% endfor %}
</ul>