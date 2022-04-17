'''
This module will contain helper functions.
'''

import secrets
from datetime import datetime, timedelta
from django.utils import timezone

def generate_hex_string(code_len=22):
    return secrets.token_urlsafe(code_len)

def is_expired(set_date_time, by_hour=1):
    current_date_time = timezone.now()
    print(set_date_time, current_date_time)

    if current_date_time - timedelta(by_hour) > set_date_time:
        return True

    return False
