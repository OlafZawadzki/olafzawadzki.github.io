
---
layout: default
title: Strona Główna
---
# Witaj na blogu!

## Wszystkie wpisy:

<ul>
{% for post in site.pages %}
  {% if post.path contains 'blogs/' %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endif %}
{% endfor %}
</ul>
