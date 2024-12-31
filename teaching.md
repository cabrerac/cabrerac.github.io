---
layout: default
title: Teaching
description: "Lecturing activities"
permalink: /teaching/
---

{% assign courses = site.courses | sort: 'start_date' | reverse %}
{% assign grouped_courses = courses | group_by: 'year' %}

<h1>Courses</h1>

{% for year in grouped_courses %}
  <h2>{{ year.name }}</h2>
  <ul>
    {% for course in year.items %}
      <li>
         <a href="{{ course.permalink }}"> <!-- Added link to course page -->
          <strong>{{ course.title }}</strong>
        </a><br>
        Institution: {{ course.institution }}<br>
        Date: {{ course.start_date | date: "%B %d, %Y" }}<br>
        Description: {{ course.description }}
      </li>
    {% endfor %}
  </ul>
{% endfor %}