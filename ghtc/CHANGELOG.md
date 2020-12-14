# {{ TITLE|default("CHANGELOG") }}

{% for TAG in TAGS %}

## {{ TAG.name }}{% if TAG.date != "unreleased" %} ({{ TAG.date }}){% endif %}

{% for CAT, ENTRIES in TAG.categories.items() %}

### {{ CAT }}

{% for ENTRY in ENTRIES %}
- {{ ENTRY.description }}
{%- endfor %}

{% endfor %}

{% endfor %}
