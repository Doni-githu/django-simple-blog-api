from django.core.mail import send_mail
import random
from django.conf import settings
import base64


async def send_email(subject, emails, message):
    await send_mail(
        subject=subject,
        message=message,
        from_email='ddonierov96@gmail.com',
        recipient_list=[emails],
    )
    return "Ok"


def generate_verification_code(id):
    user_id_bytes = str(id).encode('utf-8')
    encoded_user_id = base64.b64encode(user_id_bytes).decode('utf-8')
    return encoded_user_id


def decode_verification_code(verification_code):    
    decoded_user_id_bytes = base64.b64decode(verification_code.encode('utf-8'))
    decoded_user_id = decoded_user_id_bytes.decode('utf-8')
    return decoded_user_id

