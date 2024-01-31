from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from appointments.models import Appointment
from user.models import User


@shared_task
def send_email(user_id, appointment_id):
    user = get_object_or_404(User, pk=user_id)
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    org = appointment.organization
    context = {
        'user_fio': user.first_name,
        'appoint_date_time': appointment.datetime_start,
        'org_address': org.factual_address,
        'org_name': org.short_name,
        'org_phone': org.phone
    }

    html = render_to_string('appointment_email.html', context)
    txt = render_to_string('appointment_email.txt', context)

    send_mail(
        subject="Поисклиник: уведомление о записи на прием",
        message=txt,
        from_email='vgolosyandriya@yandex.ru',
        recipient_list=[user.email],
        html_message=html
    )
