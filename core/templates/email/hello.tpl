{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ name }}
{% endblock subject %}

{% block html %}
This is a <strong>simple</strong> message from <b>smtp4dev</b>
{% endblock html %}