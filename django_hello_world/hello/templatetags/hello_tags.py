from django import template
from django.core.urlresolvers import reverse
from django.utils.html import escape

register = template.Library()


def url_to_edit_object(obj):
    url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.module_name), args=[obj.id])
    return url


@register.simple_tag
def edit_link(value):
    try:
        return '<a href="%s">(%s)</a>' % (
            url_to_edit_object(value),
            escape(value)
        )
    except (Exception):
        return '()'