from django import template
from django.urls import reverse

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name) -> dict:
    request = context['request']
    current_path = request.path
    query = MenuItem.objects.filter(menu_main__menu_name=menu_name).select_related('menu_main', 'parent')
    query_val = query.values()
    items = [item for item in query_val.filter(parent=None)]
    target_item = select_target_item(query, current_path)
    selected_line = tree_line(target_item)

    for item in items:
        if item['id'] in selected_line:
            item['child_items'] = get_child(query_val, selected_line, item['id'])
    result_dict = {'items': items,
                   'request': context['request']}
    return result_dict


def get_child(items, selected_line, target_item) -> list:
    item_list = [item for item in items.filter(parent_id=target_item)]
    for item in item_list:
        if item['named_url']:
            item['URL'] = reverse(item['named_url'])
        if item['id'] in selected_line:
            item['child_items'] = get_child(items, selected_line, item['id'])
    return item_list


def tree_line(target_item) -> list:
    parent = target_item
    line_lst = []
    while parent:
        line_lst.append(parent.id)
        parent = parent.parent
    return line_lst


def select_target_item(queryset, current_path):
    for item in queryset:
        if item.URL and item.URL == current_path:
            return item
        elif item.named_url and item.named_url == current_path:
            return item
