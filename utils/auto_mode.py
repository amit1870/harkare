'''
Script will send a public to all registered shrota.
'''

import argparse
import django

django.setup()

from accounts.models import Manushya
from utils import send_email, helper
from harkare import settings

def get_all_manushya():
    all_manushya = Manushya.objects.all()
    return [manushya.email for manushya in all_manushya]


def send_link(link):
    emails = get_all_manushya()
    emails = ','.join(emails)

    service = send_email.create_service(
        settings.GOOGLE_API['token_path'],
        settings.GOOGLE_API['pickle_path'],
        settings.GOOGLE_API['name'],
        settings.GOOGLE_API['version'],
        settings.GOOGLE_API['scope']
    )
    message_list = []
    EMAIL = {
        'from': 'amitxvf@gmail.com',
        'to': emails + ",amitxvf@gmail.com",
        'subject': 'Link to Harkare',
        'content': f'{link}'
    }
    message = send_email.create_plain_html_message(EMAIL['from'],
                EMAIL['to'],
                EMAIL['subject'],
                EMAIL['content'],
                html=True)
    message_list.append(message)

    message_response = send_email.send_message(service, EMAIL['from'], message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--link', required=True, help='Link')
    args = parser.parse_args()
    if args.link:
        send_link(args.link)
