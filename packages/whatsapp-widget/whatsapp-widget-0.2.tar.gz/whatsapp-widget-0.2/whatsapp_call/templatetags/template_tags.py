from django.template import Library
from whatsapp_call.models import Whatsapp

register = Library()

@register.inclusion_tag('whatsapp_call/whatsapp_call_btn.html')
def whatsapp_widget():
    whatsapp = Whatsapp.objects.all()
    return {'wa_accounts': whatsapp}
