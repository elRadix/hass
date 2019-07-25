import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_FROM, EMAIL_ATTR_BODY


_LOGGER = logging.getLogger(__name__)
EMAIL_ADDRESS = 'dhl'
ATTR_DHL = 'dhl'


def parse_dhl(emails):
    """Parse DHL tracking numbers."""
    tracking_numbers = []

    for email in emails:
        email_from = email[EMAIL_ATTR_FROM]
        if isinstance(email_from, (list, tuple)):
            email_from = list(email_from)
            email_from = ''.join(list(email_from[0]))
        if EMAIL_ADDRESS in email_from:
            matches = re.findall(r'idc=(.*?)"', email[EMAIL_ATTR_BODY])
            for tracking_number in matches:
                if tracking_number not in tracking_numbers:
                    tracking_numbers.append(tracking_number)
                
    return tracking_numbers
    
