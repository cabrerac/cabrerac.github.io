---
layout: default
title: Teaching
description: "Lecturing activities"
permalink: /teaching/
---

{% assign courses = site.courses | sort: 'start_date' | reverse %}
{% assign grouped_courses = courses | group_by: 'year' %}

<h1>Courses</h1><br>
{% for year in grouped_courses %}
  <h3>{{ year.name }}</h3>
  <ul>
    {% for course in year.items %}
      <li>
        <a href="{{ course.permalink }}"> <!-- Added link to course page -->
          <strong>{{ course.title }}</strong>
        </a>
        <br>
        <strong>Description:</strong> {{ course.description }}<br>
        <strong>Institution:</strong> {{ course.institution }}<br>
        <strong>Year:</strong> {{ course.year }}<br>
      </li>
    {% endfor %}
  </ul>
{% endfor %}