from django import template
from django.urls import resolve, Resolver404

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, *url_names):
    """
    Usage:
        class="nav-link{% active 'pages:home' %}"
        class="nav-link{% active 'catalog:community_list' 'catalog:community_detail' %}"

    Returns " active" if the current resolved view name matches any of the given names.
    """
    request = context.get("request")
    if not request:
        return ""
    try:
        match = resolve(request.path_info)
    except Resolver404:
        return ""
    current_name = match.view_name or ""
    return " active" if current_name in url_names else ""
