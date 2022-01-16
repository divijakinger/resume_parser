import re

# Extracting Mobile Number
def extract_mobile_number(text):
    phone = re.findall(re.compile(
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'),
        text)

    if phone:
        number = ''.join(phone[0])
        if len(number) >= 10:
            return '' + number
        else:
            return number

