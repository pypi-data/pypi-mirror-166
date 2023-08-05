
Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'whatsapp_call',
    ]

2. python manage.py migrate

3. Add {% load whatsapp_tags %} in base.html or any html files.

4. Add {% whatsapp_widget %} in end of body tag in your template

5. Add whatsapp account in admin panel (Phone without 0 )

6. Enjoy this