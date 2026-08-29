"""
Notification helpers. Email sending uses Django's configured EMAIL_BACKEND,
which defaults to console output in development and is set via env vars
(EMAIL_HOST, EMAIL_HOST_USER, etc.) in production. No credentials are hardcoded.
"""
from django.conf import settings
from django.core.mail import send_mail


def _safe_send(subject: str, message: str, to: list[str]):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to, fail_silently=True)
    except Exception:
        # Never let a notification failure break the request/response cycle.
        pass


def notify_new_audit_request(audit):
    _safe_send(
        subject=f"New Free IT Audit request — {audit.company_name}",
        message=(
            f"Company: {audit.company_name}\n"
            f"Contact: {audit.contact_person}\n"
            f"Email: {audit.email}\n"
            f"Phone: {audit.phone}\n"
            f"Employees: {audit.employee_count}\n"
            f"Problems: {', '.join(audit.problems)}\n"
        ),
        to=[settings.COMPANY_NOTIFY_EMAIL],
    )


def notify_new_contact_request(contact):
    _safe_send(
        subject=f"New contact form submission — {contact.name}",
        message=f"Name: {contact.name}\nCompany: {contact.company}\nEmail: {contact.email}\nMessage: {contact.message}",
        to=[settings.COMPANY_NOTIFY_EMAIL],
    )


def notify_new_appointment(appointment):
    _safe_send(
        subject=f"New appointment request — {appointment.get_appointment_type_display()}",
        message=f"Name: {appointment.name}\nEmail: {appointment.email}\nPreferred date: {appointment.preferred_date}",
        to=[settings.COMPANY_NOTIFY_EMAIL],
    )


def notify_new_ticket(ticket):
    _safe_send(
        subject=f"New support ticket — {ticket.title}",
        message=f"Priority: {ticket.priority}\nCompany: {ticket.company}\n\n{ticket.description}",
        to=[settings.COMPANY_NOTIFY_EMAIL],
    )
