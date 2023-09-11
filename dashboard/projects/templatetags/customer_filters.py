from django import template

register = template.Library()

@register.filter
def lower(value):
    return value.lower()

# @register.filter
# def split_and_multiply(value):
#     parts = value.split("X")
#     if len(parts) == 2:
#         try:
#             num1 = float(parts[0])
#             num2 = float(parts[1])
#             return num1 * num2
#         except (ValueError, TypeError):
#             pass
#     return None