from django import template

register = template.Library()

@register.filter
def sec_to_hhmmss(seconds):
    seconds = int(seconds)
    rem = seconds % 3600
    HH = seconds // 3600
    MM = rem // 60
    SS = rem % 60
    if HH != 0:
        return f'{HH:02}:{MM:02}:{SS:02}'
    else:
        return f'{MM:02}:{SS:02}'

