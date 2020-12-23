from django.template import Library

register = Library()

@register.filter
def filter_phone(phone):
	return phone[:3] + '*'*4 + phone[-4:]