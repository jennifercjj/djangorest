from django import template
from cart.utlis import get_or_set_or_session

register = template.Library()

@register.filter
def cart_iten_count(request):
    orden=get_or_set_or_session(request)
    count= orden.items.count()
    return count