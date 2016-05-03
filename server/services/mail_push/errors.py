#coding=utf-8
from __future__ import absolute_import

import httplib

class MailQueueError(Exception):
    """
    Base class for mail queue exceptions.
    """
    status_code = httplib.INTERNAL_SERVER_ERROR
    response_code = 0
    status_message = 'error'
    affix_message = None

    def __init__(self, message=None):
        self.affix_message = message

    def __str__(self):
        return '{}:{}'.format(self.status_message, self.affix_message)


class MailQueuePushFailed(MailQueueError):
    response_code = 900001
    status_message = "MAIL_QUEUE_PUSH_FAILED"