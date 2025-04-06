---
layout: page
title: Teaching
permalink: /teaching/
---
<h1>Courses</h1><br>
{% assign visible_courses = site.courses | where: "visible", true | sort: "start_date" | reverse %}
{% if visible_courses.size > 0 %}
  <div class="courses-list">
    {% for course in visible_courses %}
      <div class="course-item">
        <a href="{{ course.url | relative_url }}" class="course-title">{{ course.title }}</a>
        <div class="course-meta">
          {% if course.institution %}
            <span class="course-institution">{{ course.institution }}</span>
          {% endif %}
          {% if course.start_date %}
            <span class="course-date">{{ course.start_date | date: "%B %Y" }}</span>
          {% endif %}
        </div>
        {% if course.description %}
          <p class="course-description">{{ course.description }}</p>
        {% endif %}
      </div>
    {% endfor %}
  </div>
{% else %}
  <p>No courses available at the moment.</p>
{% endif %}