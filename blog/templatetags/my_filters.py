from django.template import Library

register = Library()

@register.filter(name='times') 
def times(number):
    return range(number)

""" in template
{% load my_filters %}
{% for i in 2|times %}

"""
