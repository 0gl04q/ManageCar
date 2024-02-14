from django import template

register = template.Library()


@register.inclusion_tag('management/director/includes/tag_info.html')
def tag_info(info):
    return {
        'info': info
    }


@register.inclusion_tag('management/director/includes/row_table.html')
def row_table(name, info):
    return {
        'name': name,
        'info': info
    }


@register.inclusion_tag('management/director/includes/row_form.html')
def row_form(name, info):
    return {
        'name': name,
        'info': info
    }
