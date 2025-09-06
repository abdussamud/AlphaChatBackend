# Description: This file contains the EmailThread class which is used to send emails asynchronously.
import logging as loggers
from threading import Thread
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

loggers.basicConfig(level=loggers.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggers.getLogger(__name__)

# logger.setLevel(loggers.DEBUG)


class EmailThread(Thread):
    """
    This class is used to send emails asynchronously.

    Attributes:
        subject (str): The subject of the email.
        html_content (str): The content of the email.
        recipient_list (list): The list of recipients.

    """

    def __init__(self, subject, html_content, recipient_list, key, files=None):
        self.subject = subject
        self.key = key
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.files = files
        Thread.__init__(self)

    def run(self):
        try:

            message = get_template(self.html_content).render(self.key)
            msg = EmailMessage(self.subject, message,
                               settings.EMAIL_FROM, self.recipient_list)
            msg.content_subtype = "html"
            filename = "file"
            if self.files:
                msg.attach(filename, self.files, 'application/pdf')

            msg.send()
        except Exception as e:
            logger.error(e)


def send_mail(subject, recipient_list, html_content=None,  key=None, files=None):
    try:
        EmailThread(subject, html_content, recipient_list, key, files).start()

        logger.info('Email sent to: {}'.format(recipient_list))
    except Exception as e:
        logger.error(e)
