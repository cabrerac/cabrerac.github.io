---
layout: default
title: Teaching
description: "Lecturing activities"
permalink: /teaching/
---

{% assign courses = site.courses | sort: 'start_date' | reverse %}
{% assign grouped_courses = courses | group_by: 'year' %}

<h2>Courses: {{ courses | size }}</h2>

{% for year in grouped_courses %}
  <h2>{{ year.name }}</h2>
  <ul>
    {% for course in year.items %}
      <li>
        <strong>{{ course.title }}</strong><br>
        Date: {{ course.date | date: "%B %d, %Y" }}<br>
        Description: {{ course.description }}
      </li>
    {% endfor %}
  </ul>
{% endfor %}