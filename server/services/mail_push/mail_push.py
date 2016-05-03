#coding=utf-8
from __future__ import absolute_import

import json, os
from jinja2 import Template

from utils.helpers import now, DottedImmutableDict

from .errors import MailQueuePushFailed


class MailQueuePusher(object):
    rds_queue_key = "mail_queue"
    default_subject = u"DO NOT REPLY"
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, 'templates')

    """
    smtp_server = {
        "server": "SMTP_SERVER",
        "user": "SMTP_USERNAME",
        "pwd": "SMTP_PASSWORD"
    }
    """
    def __init__(self, rds_conn, smtp_server, mail_from, enabled = False):
        self.rds_conn = rds_conn
        self.enabled = enabled
        self.mail_from = mail_from
        self.stmp_server = smtp_server
        return

    def _push_single_mail(self, mail):
        if self.enabled is not True:
            return False
        try:
            mail_data = json.dumps(mail)
            self.rds_conn.lpush(self.rds_queue_key, mail_data)
        except Exception as e:
            raise MailQueuePushFailed

        return True


    def _make_mail(self, recipients, subject, template_str, context):
        template = Template(template_str)
        content = template.render(meta=DottedImmutableDict(context))

        return {
            'from': self.mail_from,
            'to': recipients,
            'subject': subject or self.default_subject,
            'body': content,
            'smtp': self.stmp_server,
            'now': now()
        }


    def send_system_mail(self, recipients, subject, template_str, context):
        if not isinstance(context, dict):
            context = {}

        if not isinstance(template_str, (unicode, str)):
            temoplate_str = u''

        if isinstance(recipients, (unicode, str)):
            recipients = [recipients]
        elif not isinstance(recipients, list):
            recipients = list(recipients)

        send_mail = self._make_mail(recipients, subject, template_str, context)
        self._push_single_mail(send_mail)
        return