# {{ TITLE|default("CHANGELOG") }}
{%
    set TYPE_MAPPINGS = {
        "OTHER": "Other",
        "PERFORMANCE": "Performance",
        "SECURITY": "Security",
        "DEPRECATED": "Deprecated",
        "REMOVED": "Removed",
        "CHANGED": "Changed",
        "FIXED": "Bug Fixes",
        "ADDED": "New Features"
    }
%}
{% for section in CHANGELOG.sections|sort(attribute="tag.date", reverse=True) -%}
## {% if section.tag.name != "__head" %}{{section.tag.name}} ({{ section.tag.date }}){% else %}{{UNRELEASED_TITLE}}{% endif %}

{% if section.subsections|length == 0 -%}
- No interesting change

{% endif -%}
{% for subsection in section.subsections -%}
### {{ TYPE_MAPPINGS.get(subsection.type.name, subsection.type.name) }}

{% for LINE in subsection.lines|sort(attribute='commit_date', reverse=False) -%}
- {{ LINE.message }}{% if DEBUG %} { commit_hash: {{LINE.commit_sha}}, commit_date: {{LINE.commit_date}} }{% endif %}
{% endfor %}
{% endfor -%}
{% endfor -%}
