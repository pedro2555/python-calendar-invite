#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8  
'''
@author: sats
'''
import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import Encoders
import os, datetime

def send_invite(param):
    """
    param = {
        'from': string
        'to': list or string of valid emails,
        'subject': string,
        'html_body': string,
        'body_plain': string if html_body not provided,
        'starts': datetime event start time GMT,
        'ends': datetime event end time GMT,
        'smtp_server': string,
        'smtp_port': integer,
        'smtp_user': string,
        'smtp_password': string,
        'ics_file': string TODO document properties,
        'mail_template': string TODO document properties
    }
    """
    CRLF = "\r\n"

    """to list"""
    to = ""
    if 'to' in param:
        if type(param['to']) == str:
            to = param['to']
        elif type(param['to']) == list:
            to = ", ".join(param['to'])

    """body"""
    is_html = False
    body = ""
    if param['body_html']:
        is_html = True
        body = param['body_html']
    else:
        body = param['body_plain']


    """generate ics"""
    ics = param['ics_file']
    ics = ics.replace('uid', datetime.datetime.now().strftime("%s"))
    ics = ics.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))
    ics = ics.replace('startDate', param['startDate'].strftime("%Y%m%dT%H%M%SZ"))
    ics = ics.replace('endDate', param['endDate'].strftime("%Y%m%dT%H%M%SZ"))
    ics = ics.replace('subject', param['subject'])


    """generate mail"""
    mail = MIMEMultipart('alternative')
    mail['From'] = param['from']
    mail['Reply-To'] = param['from']
    mail['To'] = to
    mail['Subject'] = param['subject']
    mail['Date'] = formatdate(localtime = False)
    if is_html:
        mail.attach(MIMEText(body, 'html'))
    else:
        mail.attach(MIMEText(body, 'plain'))
    mail.attach(MIMEText(ics, 'calendar;method=REQUEST'))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('vaccmonitor@gmail.com', '4vFLY6vOUJIK0imSgM89')
    mailServer.sendmail(param['from'], param['to'], mail.as_string())
    mailServer.close()