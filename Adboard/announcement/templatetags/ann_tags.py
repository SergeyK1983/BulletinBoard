from django import template


register = template.Library()


@register.simple_tag()
def get_last_page(page_links):
    count_pages = len(page_links)
    return page_links[count_pages-1]


@register.simple_tag()
def get_page_num(page_links, pages_count):
    current_page = 1

    for page in page_links:
        if page.is_active:
            current_page = page.number

    pages = {
        "current_page": current_page,
        "ellipsis_prefix": (current_page - page_links[0].number > 1),
        "ellipsis_suffix": (pages_count - current_page > 1)
    }
    return pages
