from django import template

register = template.Library()


@register.filter
def change_favorite_button(recipe, user_id):
    return recipe.is_favorite(user_id)


@register.filter
def is_in_cart(recipe, user_id):
    return recipe.is_in_cart(user_id)


@register.filter
def is_following(user, author_id):
    return user.following.model.is_following(user, author_id)


@register.filter
def get_filter_values(value):
    return value.getlist('filter')


@register.filter
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.slug)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.slug)

    return new_request.urlencode()
