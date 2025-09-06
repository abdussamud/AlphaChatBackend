from utils.threads import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def send_email_notification(recipient, subject, template, context):
    """
    This function is used to send email notifications.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        template (str): The template of the email.
        context (dict): The context of the email.

    """

    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)
    send_mail(subject, text_content, [recipient])
