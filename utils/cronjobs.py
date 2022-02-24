# Python
from collections import defaultdict
from datetime import timedelta
# Django
from django.utils import timezone
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
# app direccion
from apps.direccion.models import Objetivos

def deadline_reminder():
    today = timezone.now().date()
    tomorrow = (today + timedelta(days=1))
    subject, from_email = 'Recordatorio ControlSedec', 'controlsedec@tabasco.gob.mx'
    email_list = []
    objs = Objetivos.objects.filter((Q(end_date=today) | Q(end_date=tomorrow)), is_done=False).select_related('actividad__usuario__correos')
    print(objs)
    data = defaultdict(lambda: defaultdict(list))
    for o in objs:
        data[o.actividad.usuario][o.actividad].append(o)
    for k, v in dict(data.items()).items():
        if k.correos.correo_per or k.correos.correo_inst:
            html_content = render_to_string('email/reminders/deadline_obj.html', 
                {'user': k, 'acts': dict(v.items()).items()}
            )
            mails = [k.correos.correo_per, k.correos.correo_inst]
            message = EmailMultiAlternatives(subject, '', from_email, mails)
            message.attach_alternative(html_content, "text/html")
            # email_list.append(message)
    return get_connection().send_messages(email_list)