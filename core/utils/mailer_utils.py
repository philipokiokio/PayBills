from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from core.config import mail_settings
from pathlib import Path
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.mail_username,
    MAIL_PASSWORD = mail_settings.mail_password,
    MAIL_FROM = mail_settings.mail_from,
    MAIL_PORT = mail_settings.mail_port,
    MAIL_SERVER = mail_settings.mail_server,
    MAIL_FROM_NAME= mail_settings.mail_from_name,
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER=  Path(__file__).parent.parent/"templates"  
)




async def send_mail(mail_subject:str, recipient:List[EmailStr], data:dict ,template:str):
    
    mail_message = MessageSchema(
        subject = mail_subject,
        recipients = recipient,
        template_body = data,
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(mail_message, template_name=template)
        return True
    except:
        return False



        