import os
import logging

from logging.handlers import SMTPHandler
from django.core.mail import send_mail
from django.conf import settings

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/home/greywater/Documents/Kirae/app/src/tmp/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(__name__)


# Add the SMTPHandler to the logger
mail_handler = SMTPHandler(
    mailhost=("smtp.gmail.com", 587),
    fromaddr="django_app@example.com",
    toaddrs=["lorene@kirae.io"],
    subject="Django Log",
    credentials=(os.environ["SMTP_EMAIL"], os.environ["SMTP_PASSWORD"]),
    secure=()
)

mail_handler.setLevel(logging.INFO)

# Add the handler to the logger
logger.addHandler(mail_handler)
