import os
import base64
import argparse
import mimetypes
import pickle

from time import sleep
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests.exceptions import HTTPError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

def create_plain_html_message(sender, to, subject, message_text, html=False):
    """Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    Returns:
    An object containing a base64url encoded email object.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    if not html:
        msg.attach(MIMEText(message_text, 'plain'))
    else:
        msg.attach(MIMEText(message_text, 'html'))

    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def create_message_with_attachment(
    sender,
    to,
    subject,
    message_text,
    attachment_file_path,
    html=False
    ):
    """Create a message for an email.
    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: Html or plain text message to be sent         
      attachment_file_path: The path to the file to be attached.
    Returns:
      An object containing a base64url encoded email object.
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    if not html:
        msg.attach(MIMEText(message_text, 'plain'))
    else:
        msg.attach(MIMEText(message_text, 'html'))

    content_type, encoding = mimetypes.guess_type(attachment_file_path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
        fp = open(attachment_file_path, 'r')
        attachment_msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()

    elif main_type == 'image':
        fp = open(attachment_file_path, 'rb')
        attachment_msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()

    elif main_type == 'audio':
        fp = open(attachment_file_path, 'rb')
        attachment_msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()

    else:
        fp = open(attachment_file_path, 'rb')
        attachment_msg = MIMEBase(main_type, sub_type)
        attachment_msg.set_payload(fp.read())
        fp.close()

    filename = os.path.basename(attachment_file_path)
    attachment_msg.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(attachment_msg)

    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def create_service(client_secrets_file_path, token_pickle_file_path, api_name, api_version, scopes):
    creds = None
    service = None

    if os.path.exists(token_pickle_file_path):
        with open(token_pickle_file_path, 'rb') as token:
            creds = pickle.load(token)

    # if no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file_path,scopes)
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open(token_pickle_file_path, 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build(api_name, api_version, credentials=creds)
    except Exception as e:
        print(e)

    return service

def send_message(service, user_id, message):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        return message
    except HTTPError as  error:
        print ('Error {}'.format(error))
