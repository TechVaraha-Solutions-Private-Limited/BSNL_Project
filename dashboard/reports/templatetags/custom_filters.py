from django import template

register = template.Library()

@register.filter(name='application_fee')
def application_fee(items):
    i=0

    for i in items:
        if i.paymentname == "DownPayment" :
            i=200
    return i
